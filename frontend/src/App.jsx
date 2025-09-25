import React, { useState, useEffect, useRef } from 'react';
import Editor from 'react-simple-code-editor';
import { create } from 'zustand';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css'; // Dark theme for syntax highlighting
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-c';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-python';
import './index.css'; // Our new styles

// --- 1. Enhanced State Management (Zustand) ---
const useStore = create((set, get) => ({
  code: `::c
#include <stdio.h>
int main() {
    int a[] = {50, 25, 75, 100};
    int n = sizeof(a)/sizeof(a[0]);
    printf("[");
    for (int i = 0; i < n; i++) {
        printf("%d", a[i]);
        if (i < n - 1) printf(", ");
    }
    printf("]");
    return 0;
}

::py
import json, sys
state_str = sys.argv[1] if len(sys.argv) > 1 else "{}"
state = json.loads(state_str)
a = state.get('a', [])
a.sort()
state['a'] = a
print(json.dumps(state))

::java
import java.util.Arrays;
public class Main {
    public static void main(String[] args) {
        String input = "{}";
        if(args.length > 0) input = args[0];

        String arrayStr = input.substring(input.indexOf('[') + 1, input.indexOf(']'));
        String[] items = arrayStr.split(",");
        int[] a = new int[items.length];
        for(int i = 0; i < items.length; i++) {
            a[i] = Integer.parseInt(items[i].trim());
        }
        System.out.println("Sorted array : " + Arrays.toString(a));
    }
}`,
  outputLog: [],
  isRunning: false,
  socket: null,
  
  // Actions
  setCode: (newCode) => set({ code: newCode }),
  clearLog: () => set({ outputLog: [] }),
  
  connect: () => {
    if (get().socket) return;
    const newSocket = new WebSocket('ws://localhost:8000/ws');
    newSocket.onopen = () => set({ socket: newSocket });
    newSocket.onmessage = (event) => {
      const log = event.data;
      if (log.includes('--- Pipeline Finished ---')) {
        set({ isRunning: false });
      }
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

// --- 2. Custom Syntax Highlighting Logic ---
const highlightWithBlocks = (code) => {
  // Regex to find language blocks
  const pattern = /(::\w+\n)([\s\S]*?)(?=\n::|$)/g;
  const langMap = { c: 'c', py: 'python', java: 'java' };
  let lastIndex = 0;
  const result = [];

  for (const match of code.matchAll(pattern)) {
    const [fullMatch, tag, codeBlock] = match;
    const { index } = match;

    // Add uncolored text before the match
    if (index > lastIndex) {
      result.push(<span key={`pre-${lastIndex}`}>{code.substring(lastIndex, index)}</span>);
    }
    
    const lang = tag.trim().substring(2);
    const prismLang = langMap[lang] || 'clike';
    
    result.push(
      <div key={index} className={`lang-block lang-${lang}`}>
        <span className="lang-tag">{tag}</span>
        <span
          dangerouslySetInnerHTML={{
            __html: Prism.highlight(codeBlock, Prism.languages[prismLang], prismLang),
          }}
        />
      </div>
    );
    lastIndex = index + fullMatch.length;
  }
  
  // Add any remaining text after the last match
  if (lastIndex < code.length) {
    result.push(<span key={`post-${lastIndex}`}>{code.substring(lastIndex)}</span>);
  }

  return <>{result}</>;
};

// --- 3. UI Components ---
const App = () => {
  const fileInputRef = useRef(null);
  const { code, setCode, outputLog, isRunning, socket, connect, runCode, clearLog } = useStore();

  useEffect(() => {
    if (!socket) connect();
  }, [socket, connect]);
  
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.poly')) {
      const reader = new FileReader();
      reader.onload = (e) => setCode(e.target.result);
      reader.readAsText(file);
    } else {
      alert('Please select a valid .poly file');
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Polyglot Interpreter</h1>
        <div className={`status ${socket ? 'connected' : ''}`}>
          {socket ? 'Connected' : 'Disconnected'}
        </div>
      </header>
      <div className="main-layout">
        
        {/* Left Pane: Controls & Instructions */}
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
              <li>Write code in blocks, starting each with `::lang` (e.g., `::c`, `::py`).</li>
              <li>The first block (usually C) must print a JSON array to `stdout` (e.g., `[1, 2, 3]`).</li>
              <li>Subsequent Python blocks receive state via `sys.argv[1]` and must print a JSON object to `stdout` to pass state along.</li>
              <li>The final block (usually Java) receives the state and prints the final output.</li>
            </ol>
          </div>
        </div>
        
        {/* Middle Pane: Editor */}
        <div className="editor-pane">
          <Editor
            value={code}
            onValueChange={setCode}
            highlight={highlightWithBlocks}
            padding={15}
            className="code-editor"
          />
        </div>
        
        {/* Right Pane: Output */}
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
}

export default App;