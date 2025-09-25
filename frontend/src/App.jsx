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

const initialCode = `::c
// Outermost Block (C): Formats the final report.
printf("--- FINAL REPORT ---\\n");
printf("Analysis Complete.\\n");
printf("Top Product Found: %s\\n", top_product_name);
printf("Price: $%d\\n", top_product_price);

  ::java
  // Middle Block (Java): Receives a simple JSON object from Python.
  String input = args.length > 0 ? args[0] : "{}";
  String name = input.split(",")[0].split(":")[1].replace("\\"", "");
  int price = Integer.parseInt(input.split(",")[1].split(":")[1].replace("}", "").trim());
  System.out.println("{\\"top_product_name\\": \\"" + name + "\\", \\"top_product_price\\": " + price + "}");

    ::py
    # Innermost Block (Python): Generates and processes data.
    import json
    products = [
      {"name": "Laptop", "price": 1200, "category": "Electronics"},
      {"name": "Coffee Mug", "price": 15, "category": "Kitchenware"},
      {"name": "Gaming Mouse", "price": 75, "category": "Electronics"},
      {"name": "Desk Chair", "price": 250, "category": "Furniture"}
    ]
    top_electronic_product = max(
        (p for p in products if p['category'] == 'Electronics'),
        key=lambda x: x['price']
    )
    print(json.dumps(top_electronic_product))
`;

// --- THIS IS THE FINAL, WORKING HIGHLIGHTING FUNCTION ---
const highlightCode = (code) => {
  const placeholders = {
    c: '___POLYGLOT_C_TAG___',
    py: '___POLYGLOT_PY_TAG___',
    java: '___POLYGLOT_JAVA_TAG___',
  };

  let tempCode = code;
  for (const lang in placeholders) {
    // THIS REGEX IS THE FIX: '\\s*' allows for leading whitespace.
    const regex = new RegExp(`^\\s*(::${lang})`, 'gm');
    tempCode = tempCode.replace(regex, (match, tag) => {
      // Keep the original indentation, but replace the tag with the placeholder
      return match.replace(tag, placeholders[lang]);
    });
  }

  const prismHighlighted = Prism.highlight(tempCode, Prism.languages.clike, 'clike');

  let finalHtml = prismHighlighted;
  for (const lang in placeholders) {
    finalHtml = finalHtml.replace(
      placeholders[lang],
      `<span class="lang-tag-open" data-lang="${lang}">::${lang}</span>`
    );
  }
  
  return finalHtml;
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