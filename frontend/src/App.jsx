import React, { useState, useEffect, useRef } from 'react';
import Editor from 'react-simple-code-editor';
import { create } from 'zustand';
import Prism from 'prismjs';
import 'prismjs/themes/prism-okaidia.css'; 
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-c';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-python';
import './index.css';

// Enhanced polyglot code supporting all data types!
const initialCode = `::c
int nums[] = {50, 25, 75, 100, 10};
float pi = 3.14f;
char grade = 'A';
char name[] = "Polyglot";
::/c

::py
# Work with all data types seamlessly
nums.sort()
pi_doubled = pi * 2
message = f"Student {name} got grade {grade}"
stats = {"count": len(nums), "max": max(nums)}
::/py

::java
System.out.println("=== Multi-Type Data Demo ===");
System.out.println("Sorted numbers: ");
for (int i = 0; i < nums.length; i++) {
    System.out.print(nums[i] + " ");
}
System.out.println();
System.out.println("Pi doubled: " + pi_doubled);
System.out.println("Message: " + message);
::/java`;

// Simplified highlighting - just basic syntax highlighting
const highlightCode = (code) => {
  return Prism.highlight(code, Prism.languages.clike, 'clike');
};

// Backend URL configuration
const getBackendUrl = () => {
  // Debug: log environment variables
  console.log('Environment variables:', {
    VITE_BACKEND_URL: import.meta.env.VITE_BACKEND_URL,
    NODE_ENV: import.meta.env.NODE_ENV,
    MODE: import.meta.env.MODE
  });
  
  // Check for environment variable first, then check if we're on production domain
  if (import.meta.env.VITE_BACKEND_URL) {
    console.log('Using environment variable:', import.meta.env.VITE_BACKEND_URL);
    return import.meta.env.VITE_BACKEND_URL;
  }
  
  // If we're on Vercel (production), use the Codespaces URL
  if (window.location.hostname.includes('vercel.app')) {
    console.log('Detected Vercel deployment, using Codespaces URL');
    return 'https://musical-waddle-rxwr97j7567cpjgw-8000.app.github.dev';
  }
  
  // Default to localhost for development
  console.log('Using localhost for development');
  return 'http://localhost:8000';
};

const getWebSocketUrl = () => {
  const backendUrl = getBackendUrl();
  const wsUrl = backendUrl.replace('http://', 'ws://').replace('https://', 'wss://') + '/ws';
  console.log('WebSocket URL:', wsUrl);
  return wsUrl;
};

// The Zustand store and App component are mostly the same
const useStore = create((set, get) => ({
  code: initialCode,
  outputLog: [],
  isRunning: false,
  socket: null,
  debugMode: true,
  setCode: (newCode) => set({ code: newCode }),
  clearLog: () => set({ outputLog: [] }),
  toggleDebug: async () => {
    const { debugMode } = get();
    const newDebugMode = !debugMode;
    
    try {
      const response = await fetch(`${getBackendUrl()}/debug/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled: newDebugMode })
      });
      
      if (response.ok) {
        set({ debugMode: newDebugMode });
      } else {
        // If backend not available, just toggle locally
        console.warn('Backend not available, toggling debug mode locally only');
        set({ debugMode: newDebugMode });
      }
    } catch (error) {
      console.warn('Backend not available for debug toggle, using local toggle only:', error.message);
      // Still allow local debug toggle even if backend is down
      set({ debugMode: newDebugMode });
    }
  },
  fetchDebugStatus: async () => {
    try {
      const response = await fetch(`${getBackendUrl()}/debug/status`);
      if (response.ok) {
        const data = await response.json();
        set({ debugMode: data.debug_mode });
      } else {
        console.warn('Backend not available, using default debug mode');
      }
    } catch (error) {
      console.warn('Backend not available for debug status, using default debug mode:', error.message);
      // Don't throw error, just use default debug mode
    }
  },
  connect: () => {
    if (get().socket) return;
    const newSocket = new WebSocket(getWebSocketUrl());
    newSocket.onopen = () => set({ socket: newSocket });
    newSocket.onmessage = (event) => {
      const log = event.data;
      if (log.includes('--- Pipeline Finished ---') || log.includes('Error in')) {
        set({ isRunning: false });
      }
      set((state) => ({ outputLog: [...state.outputLog, log] }));
    };
    newSocket.onclose = () => set({ socket: null, isRunning: false });
    newSocket.onerror = () => set({ isRunning: false });
  },
  runCode: () => {
    const { socket, code, debugMode } = get();
    if (socket && socket.readyState === WebSocket.OPEN) {
      const initialMessage = debugMode ? ["🚀 Starting pipeline...\n"] : [];
      set({ outputLog: initialMessage, isRunning: true });
      socket.send(code);
    }
  },
}));

const App = () => {
  const fileInputRef = useRef(null);
  const [isDragOver, setIsDragOver] = React.useState(false);
  const { 
    code, setCode, outputLog, isRunning, socket, debugMode, 
    connect, runCode, clearLog, toggleDebug, fetchDebugStatus 
  } = useStore();

  useEffect(() => { 
    if (!socket) connect(); 
    fetchDebugStatus();
  }, [socket, connect, fetchDebugStatus]);

  // Drag and drop functionality
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
    
    const files = e.dataTransfer.files;
    console.log('Files dropped:', files);
    
    if (files.length > 0) {
      const file = files[0];
      console.log('Processing dropped file:', file.name);
      
      // Simulate file input change event
      handleFileChange({ target: { files: [file], value: '' } });
    }
  };
  
  const handleFileChange = (event) => {
    console.log('File input triggered:', event.target.files);
    
    const file = event.target.files[0];
    if (!file) {
      console.log('No file selected');
      return;
    }
    
    console.log('Selected file:', file.name, 'Type:', file.type, 'Size:', file.size);
    
    // Accept .poly files or any text file
    if (file.name.endsWith('.poly') || file.type === 'text/plain' || file.type === '') {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        console.log('File loaded successfully, content length:', e.target.result.length);
        setCode(e.target.result);
        // Reset file input to allow selecting the same file again
        event.target.value = '';
      };
      
      reader.onerror = (e) => {
        console.error('Error reading file:', e);
        alert('Error reading file. Please try again.');
      };
      
      reader.readAsText(file);
    } else { 
      console.log('Invalid file type:', file.type);
      alert('Please select a valid .poly file or text file'); 
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Polyglot Interpreter</h1>
        <div className={`status ${socket ? 'connected' : ''}`}>{socket ? 'Connected' : 'Disconnected'}</div>
      </header>
      <div className="main-layout">
        <div className="controls-pane">
          <h2>Controls</h2>
          <button className="run-button" onClick={runCode} disabled={isRunning || !socket}>
            <svg viewBox="0 0 24 24" width="20" height="20"><path d="M8 5v14l11-7z"/></svg>
            {isRunning ? 'Running...' : 'Run Pipeline'}
          </button>
          <button className="upload-button" onClick={() => {
            console.log('Upload button clicked, triggering file input');
            fileInputRef.current?.click();
          }}>
            <svg viewBox="0 0 24 24" width="20" height="20"><path d="M9 16h6v-6h4l-7-7-7 7h4zm-4 2h14v2H5z"/></svg>
            Upload File (.poly/.txt)
          </button>
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
            style={{ display: 'none' }} 
            accept=".poly,.txt,text/plain"
          />
          
          <button className={`debug-button ${debugMode ? 'active' : ''}`} onClick={toggleDebug}>
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            {debugMode ? 'Hide Debug' : 'Show Debug'}
          </button>
                    <div className="instructions">
            <h2>How It Works</h2>
            <ol>
              <li>Write code in sequential blocks: <code>::lang</code> to <code>::/lang</code>.</li>
              <li>Variables are automatically passed between languages.</li>
              <li>No need for manual JSON parsing - just use variables directly!</li>
              <li>Languages execute in order: C → Python → Java.</li>
            </ol>
          </div>
        </div>
        <div 
          className={`editor-pane ${isDragOver ? 'drag-over' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <Editor
            value={code}
            onValueChange={setCode}
            highlight={highlightCode}
            padding={15}
            className="code-editor"
          />
        </div>
        <div className="output-pane">
          <div className="output-header">
            <h2>Output Log</h2>
            <button onClick={clearLog} disabled={outputLog.length === 0}>Clear</button>
          </div>
          <pre className="output-log">
            {outputLog
              .filter(line => {
                if (debugMode) return true;
                
                // When debug mode is off, only hide specific debug messages, not all output
                const debugPatterns = [
                  '🚀 Starting pipeline', '🏗️', '📥', '✏️', '➕', '🔄', '📤', 
                  '🏁', '===== POLYGLOT', '📊 Final variable', '📊 No variables persisted',
                  '✅ Pipeline completed', 'Starting fresh', 'Receiving variables',
                  'Variables being modified', 'Created:', 'Modified:', 'Passing to',
                  'Pipeline Finished', '==================================================',
                  'DEBUG Java modified vars:', 'DEBUG Java code:', '---',
                  'PIPELINE EXECUTION SUMMARY', 'POLYGLOT EXECUTION PIPELINE'
                ];
                
                return !debugPatterns.some(pattern => line.includes(pattern));
              })
              .join('\n')}
          </pre>
        </div>
      </div>
    </div>
  );
};
export default App;