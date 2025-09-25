# 🌟 Polyglot Interpreter - Phase 2

A sophisticated, web-based development environment that executes code in multiple languages (C, Python, Java) within a single, sequential pipeline. **Phase 2** introduces advanced syntax highlighting, indentation-aware visual coding, and a fully refined user experience that makes multi-language programming intuitive and powerful.

This project demonstrates cutting-edge concepts in containerization, state serialization, and modern web development, creating a unique tool for education, experimentation, and rapid prototyping.

![Polyglot Interpreter Phase 2](https://via.placeholder.com/800x400/282c34/61dafb?text=Polyglot+Interpreter+Phase+2)

## 🎨 Phase 2 Features - Visual Excellence

**Phase 2** takes the polyglot concept to the next level with a completely redesigned interface and enhanced developer experience:

### 🌈 Advanced Syntax Highlighting
- **Multi-language Prism.js integration** - Full syntax highlighting for C, Python, and Java
- **Depth-based color coding** - Visual indentation levels with distinct color schemes
- **Dynamic language detection** - Automatic syntax highlighting based on `::lang` tags
- **Perfect text alignment** - Overlay system ensures highlighting matches exactly with cursor position

### 📐 Indentation-Aware Visual System
- **Smart depth detection** - Automatically calculates nesting levels based on whitespace
- **Color-coded blocks** - Each indentation level gets a unique color (Blue → Orange → Green → Purple → Red)
- **Real-time updates** - Colors change dynamically as you modify indentation
- **Visual block structure** - Clear visual separation of nested code blocks

### 💡 Enhanced Editor Experience
- **Professional code editor** - Built with react-simple-code-editor for smooth typing
- **Transparent overlay system** - Syntax highlighting without interfering with text input
- **Monospace font rendering** - Consistent character spacing for perfect alignment
- **Dark theme optimized** - Eye-friendly color scheme for extended coding sessions

---

## 🏗️ Technical Architecture

### Frontend Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| **UI Framework** | **React 18** | Modern, component-based interface |
| **Build Tool** | **Vite** | Lightning-fast development and builds |
| **State Management** | **Zustand** | Lightweight, performant global state |
| **Code Editor** | **react-simple-code-editor** | Professional code editing experience |
| **Syntax Highlighting** | **Prism.js** | Multi-language syntax highlighting |
| **WebSocket Client** | **Native WebSocket API** | Real-time communication with backend |

### Backend Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| **API Server** | **FastAPI** | High-performance async web framework |
| **Container Runtime** | **Docker** | Isolated execution environments |
| **Process Management** | **Python asyncio** | Concurrent container orchestration |
| **WebSocket Server** | **FastAPI WebSocket** | Real-time bidirectional communication |

### System Architecture

```mermaid
graph TB
    subgraph "Frontend (React + Vite)"
        A[Code Editor with Syntax Highlighting] --> B[WebSocket Client]
        A --> C[Zustand State Store]
        C --> D[Real-time Output Display]
    end
    
    subgraph "Backend (FastAPI)"
        E[WebSocket Server] --> F[Code Parser]
        F --> G[Container Orchestrator]
        G --> H[Docker Runtime]
    end
    
    subgraph "Execution Environment"
        H --> I[C Container (GCC)]
        H --> J[Python Container]
        H --> K[Java Container (OpenJDK)]
    end
    
    B <--> E
    I --> G
    J --> G
    K --> G
    G --> E
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Docker Desktop** - Must be installed and running
- **Node.js 18+** - For the frontend development environment  
- **Python 3.8+** - For the backend server
- **Git** - For cloning the repository

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Siva-PythonPirates/polygot-interpreter.git
   cd polygot-interpreter
   ```

2. **Start the Backend** (Terminal 1)
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn server:app --reload
   ```
   Backend runs at: `http://localhost:8000`

3. **Start the Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend runs at: `http://localhost:5173`

4. **Open Your Browser**
   Navigate to `http://localhost:5173` and start coding!

---

## 📝 How to Write Polyglot Programs

The polyglot interpreter uses a simple but powerful syntax that allows multiple languages to work together:

### Basic Syntax Rules

1. **Language Tags**: Use `::lang` to specify the language (e.g., `::c`, `::py`, `::java`)
2. **Indentation**: Use spaces to create nested blocks (2 spaces = 1 level)
3. **Execution Order**: Execution starts from the innermost (most indented) block
4. **State Passing**: Each block's stdout becomes input for its parent block

### Example Program: Array Sorting Pipeline

```polyglot
::java
// Outermost Block: Final output and display
String input = args.length > 0 ? args[0] : "{}";
String searchKey = "\"sorted_array\":";
int sortedArrayIndex = input.indexOf(searchKey);
if (sortedArrayIndex != -1) {
    int arrayStart = input.indexOf('[', sortedArrayIndex);
    int arrayEnd = input.indexOf(']', arrayStart);
    String arrayData = input.substring(arrayStart + 1, arrayEnd);
    System.out.println("Final sorted array: [" + arrayData + "]");
}

  ::py
  # Middle Block: Data processing and sorting
  import json, sys
  state = json.loads(sys.argv[1])
  unsorted_list = state.get("unsorted_array", [])
  unsorted_list.sort()
  print(json.dumps({"sorted_array": unsorted_list}))

    ::c
    // Innermost Block: Data generation
    printf("{\"unsorted_array\": [99, 12, 5, 87, 34, 62]}");
```

### Execution Flow

1. **C Block** generates initial data: `{"unsorted_array": [99, 12, 5, 87, 34, 62]}`
2. **Python Block** receives C's output, sorts the array, outputs: `{"sorted_array": [5, 12, 34, 62, 87, 99]}`
3. **Java Block** receives Python's output, formats and displays the final result

---

## 🎨 Visual Highlighting System

### Depth-Based Color Coding

The editor automatically applies color coding based on indentation levels:

| Depth Level | Color | Usage |
|-------------|-------|--------|
| **Level 0** | 🔵 **Blue** | Outermost blocks (no indentation) |
| **Level 1** | 🟠 **Orange** | First level of nesting (2 spaces) |
| **Level 2** | 🟢 **Green** | Second level of nesting (4 spaces) |
| **Level 3** | 🟣 **Purple** | Third level of nesting (6 spaces) |
| **Level 4** | 🔴 **Red** | Fourth level of nesting (8+ spaces) |

### Language Tags

Each `::lang` tag is highlighted with its corresponding depth color, making it easy to identify the structure and execution order of your polyglot programs.

---

## 🛠️ Development Features

### Real-Time Execution
- **WebSocket Integration** - Instant feedback during code execution
- **Live Output Streaming** - See results as they happen
- **Error Reporting** - Detailed error messages with context
- **Pipeline Visualization** - Track execution flow through multiple languages

### File Management
- **Upload Support** - Load `.poly` files directly into the editor
- **Auto-Save** - Your code persists across browser sessions
- **Export Functionality** - Save your polyglot programs locally

### Developer Experience
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Keyboard Shortcuts** - Standard editor shortcuts supported
- **Connection Status** - Real-time WebSocket connection indicator
- **Clear Output** - Easy output log management

---

## 🎯 Use Cases & Applications

### Educational
- **Computer Science Courses** - Demonstrate inter-process communication
- **Language Comparison** - Show strengths of different programming languages
- **Algorithm Teaching** - Visualize data flow through processing stages
- **Systems Programming** - Understand containerization and process isolation

### Professional
- **Rapid Prototyping** - Quick proof-of-concepts using multiple languages
- **Microservice Simulation** - Test inter-service communication patterns
- **Data Pipeline Development** - Build and test data transformation workflows
- **Cross-Platform Development** - Leverage language-specific libraries together

### Experimental
- **Language Integration Research** - Explore polyglot programming patterns
- **Performance Benchmarking** - Compare language performance in real scenarios
- **Educational Tool Development** - Build interactive coding experiences
- **Code Golf** - Create complex programs with minimal syntax

---

## 🔮 Future Roadmap

### Phase 3 Enhancements
- [ ] **Additional Languages** - Go, Rust, JavaScript (Node.js), TypeScript
- [ ] **Advanced Error Handling** - Syntax error highlighting in editor
- [ ] **State Inspector** - Visual JSON state viewer with diff highlighting
- [ ] **Performance Metrics** - Execution time and memory usage tracking
- [ ] **Collaborative Editing** - Multi-user real-time coding sessions

### Advanced Features
- [ ] **Custom Containers** - User-defined Docker environments
- [ ] **Package Management** - Install libraries within language blocks
- [ ] **Version Control** - Git integration for polyglot programs
- [ ] **API Integration** - HTTP requests within language blocks
- [ ] **Database Connections** - Persistent data storage across executions

### Platform Extensions
- [ ] **Cloud Deployment** - Host and share polyglot programs online
- [ ] **Mobile App** - Native mobile interface for coding on-the-go
- [ ] **VS Code Extension** - Integrate polyglot capabilities into popular IDEs
- [ ] **Educational Platform** - Structured courses and tutorials

---

## 🤝 Contributing

We welcome contributions! Here are some ways you can help:

### Code Contributions
- **Frontend Improvements** - Enhance the React interface
- **Backend Optimization** - Improve container orchestration
- **New Language Support** - Add runners for additional languages
- **Testing** - Expand test coverage and reliability

### Documentation
- **Tutorial Creation** - Write guides for specific use cases
- **API Documentation** - Document WebSocket protocols and APIs
- **Example Programs** - Create interesting polyglot program examples

### Community
- **Bug Reports** - Help us identify and fix issues
- **Feature Requests** - Suggest new capabilities
- **User Feedback** - Share your experience and suggestions

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **React Team** - For the powerful UI framework
- **FastAPI** - For the excellent async web framework  
- **Docker** - For containerization technology
- **Prism.js** - For syntax highlighting capabilities
- **Vite** - For lightning-fast development experience

---

## 📧 Contact & Support

- **GitHub Issues** - For bug reports and feature requests
- **Discussions** - For questions and community interaction
- **Email** - [your-email@domain.com] for direct communication

---

**Built with ❤️ by the Python Pirates crew**

*Making multi-language programming accessible, visual, and fun!*