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

const initialCode = `::java
// Outermost Block (Java): Receives the final sorted array and prints it.
String input = args.length > 0 ? args[0] : "{}";

System.out.println("--- Array Sort & Print Program ---");
System.out.println("DEBUG - Java received input: " + input);

// Check if we have sorted_array (from Python) or unsorted_array (from C)
if (input.contains("sorted_array")) {
    // Parse sorted array from Python - be more precise with the search
    String searchKey = "\\\"sorted_array\\\":";
    int sortedArrayIndex = input.indexOf(searchKey);
    if (sortedArrayIndex != -1) {
        // Find the [ that comes AFTER "sorted_array":
        int arrayStart = input.indexOf('[', sortedArrayIndex);
        int arrayEnd = input.indexOf(']', arrayStart);
        
        if (arrayStart != -1 && arrayEnd != -1) {
            String arrayData = input.substring(arrayStart + 1, arrayEnd);
            System.out.println("Final sorted array: [" + arrayData + "]");
        } else {
            System.out.println("Could not parse sorted array from input");
        }
    } else {
        System.out.println("Could not find sorted_array key in input");
    }
} else if (input.contains("unsorted_array")) {
    // We got unsorted array directly - something went wrong with the pipeline
    System.out.println("WARNING: Received unsorted array instead of sorted array!");
    int startIndex = input.indexOf("unsorted_array");
    int arrayStart = input.indexOf('[', startIndex);
    int arrayEnd = input.indexOf(']', arrayStart);
    
    if (arrayStart != -1 && arrayEnd != -1) {
        String arrayData = input.substring(arrayStart + 1, arrayEnd);
        System.out.println("Unsorted array (not processed by Python): [" + arrayData + "]");
    }
} else {
    System.out.println("No array data found in input: " + input);
}

  ::py
  # Middle Block (Python): Receives the unsorted array and sorts it.
  import json, sys
  
  state = json.loads(sys.argv[1])
  unsorted_list = state.get("unsorted_array", [])
  
  unsorted_list.sort()
  
  # Pass the new, sorted array to the parent (Java)
  print(json.dumps({"sorted_array": unsorted_list}))

    ::c
    // Innermost Block (C): Generates the initial, unsorted data.
    printf("{\\"unsorted_array\\": [99, 12, 5, 87, 34, 62]}");
`;

// --- SIMPLIFIED INDENTATION-AWARE HIGHLIGHTING ---
const highlightCode = (code) => {
  const lines = code.split('\n');
  let result = [];
  
  const getIndentLevel = (line) => {
    const match = line.match(/^(\s*)/);
    return match ? match[1].length : 0;
  };
  
  const getDepthColor = (indentLevel) => {
    const depth = Math.floor(indentLevel / 2); // 2 spaces = 1 depth
    const colors = ['blue', 'orange', 'green', 'purple', 'red'];
    return colors[depth % colors.length];
  };
  
  let currentLang = null;
  let currentLangLineIndex = -1;
  let blockContent = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    const indentLevel = getIndentLevel(line);
    
    // Check for language tag
    const langMatch = trimmed.match(/^::(c|py|java)$/);
    
    if (langMatch) {
      // Process previous block if exists
      if (currentLang && blockContent.length > 0) {
        const blockCode = blockContent.join('\n');
        let highlighted = '';
        
        try {
          switch (currentLang) {
            case 'c':
              highlighted = Prism.highlight(blockCode, Prism.languages.c, 'c');
              break;
            case 'py':
              highlighted = Prism.highlight(blockCode, Prism.languages.python, 'python');
              break;
            case 'java':
              highlighted = Prism.highlight(blockCode, Prism.languages.java, 'java');
              break;
            default:
              highlighted = Prism.highlight(blockCode, Prism.languages.clike, 'clike');
          }
        } catch (e) {
          highlighted = blockCode;
        }
        
        // Get the CURRENT indentation of the previous lang tag line
        const prevLangLineIndent = getIndentLevel(lines[currentLangLineIndex]);
        const colorScheme = getDepthColor(prevLangLineIndent);
        result.push(`<span class="lang-block depth-${Math.floor(prevLangLineIndent/2)}" data-lang="${currentLang}">${highlighted}</span>`);
      }
      
      // Start new block
      currentLang = langMatch[1];
      currentLangLineIndex = i; // Remember which line has the ::lang tag
      blockContent = [];
      
      // Add language tag with proper indentation and color based on CURRENT indentation
      const spaces = ' '.repeat(indentLevel);
      const colorScheme = getDepthColor(indentLevel);
      result.push(`${spaces}<span class="lang-tag color-${colorScheme}">::${currentLang}</span>`);
      
    } else if (currentLang) {
      // Add line to current block
      blockContent.push(line);
      
    } else {
      // Regular line outside blocks
      if (trimmed) {
        try {
          const highlighted = Prism.highlight(line, Prism.languages.clike, 'clike');
          result.push(highlighted);
        } catch (e) {
          result.push(line);
        }
      } else {
        result.push(line);
      }
    }
  }
  
  // Process last block
  if (currentLang && blockContent.length > 0) {
    const blockCode = blockContent.join('\n');
    let highlighted = '';
    
    try {
      switch (currentLang) {
        case 'c':
          highlighted = Prism.highlight(blockCode, Prism.languages.c, 'c');
          break;
        case 'py':
          highlighted = Prism.highlight(blockCode, Prism.languages.python, 'python');
          break;
        case 'java':
          highlighted = Prism.highlight(blockCode, Prism.languages.java, 'java');
          break;
        default:
          highlighted = Prism.highlight(blockCode, Prism.languages.clike, 'clike');
      }
    } catch (e) {
      highlighted = blockCode;
    }
    
    // Get the CURRENT indentation of the last lang tag line
    const lastLangLineIndent = getIndentLevel(lines[currentLangLineIndex]);
    const colorScheme = getDepthColor(lastLangLineIndent);
    result.push(`<span class="lang-block depth-${Math.floor(lastLangLineIndent/2)}" data-lang="${currentLang}">${highlighted}</span>`);
  }
  
  return result.join('\n');
};

const useStore = create((set, get) => ({
  code: initialCode,
  outputLog: [],
  isRunning: false,
  socket: null,
  setCode: (newCode) => set({ code: newCode }),
  clearLog: () => set({ outputLog: [] }),
  connect: () => {
    if (get().socket) return;
    const newSocket = new WebSocket('ws://localhost:8000/ws');
    newSocket.onopen = () => set({ socket: newSocket });
    newSocket.onmessage = (event) => {
      const log = event.data;
      if (log.includes('--- Pipeline Finished ---')) set({ isRunning: false });
      set((state) => ({ outputLog: [...state.outputLog, log] }));
    };
    newSocket.onclose = () => set({ socket: null });
  },
  runCode: () => {
    const { socket, code } = get();
    if (socket && socket.readyState === WebSocket.OPEN) {
      set({ outputLog: ["🚀 Starting pipeline..."], isRunning: true });
      socket.send(code);
    }
  },
}));

const App = () => {
  const fileInputRef = useRef(null);
  const { code, setCode, outputLog, isRunning, socket, connect, runCode, clearLog } = useStore();

  useEffect(() => { if (!socket) connect(); }, [socket, connect]);
  
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.poly')) {
      const reader = new FileReader();
      reader.onload = (e) => setCode(e.target.result);
      reader.readAsText(file);
    } else { alert('Please select a valid .poly file'); }
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
          <button className="upload-button" onClick={() => fileInputRef.current.click()}>
            <svg viewBox="0 0 24 24" width="20" height="20"><path d="M9 16h6v-6h4l-7-7-7 7h4zm-4 2h14v2H5z"/></svg>
            Upload .poly File
          </button>
          <input type="file" ref={fileInputRef} onChange={handleFileChange} style={{ display: 'none' }} accept=".poly"/>
          <div className="instructions">
            <h2>How It Works</h2>
            <ol>
              <li>Write code in nested blocks using indentation.</li>
              <li>Execution starts from the innermost block.</li>
              <li>A block's `stdout` (JSON) becomes state for its parent.</li>
            </ol>
          </div>
        </div>
        <div className="editor-pane">
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
          <pre className="output-log">{outputLog.join('\n')}</pre>
        </div>
      </div>
    </div>
  );
};
export default App;