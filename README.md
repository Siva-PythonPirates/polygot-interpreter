# 🚀 The Polyglot Interpreter Project

> ⚡ A revolutionary **cross-language development environment** that seamlessly executes C, Python, and Java code in a single pipeline with **automatic variable sharing**, **nested language blocks**, and **intelligent cross-language conversion**.

This isn't just another code runner — it's a paradigm shift. What started as a proof-of-concept evolved into an intelligent orchestrator that breaks down language barriers, enabling developers to leverage the best features of each language in a unified workflow.

## 🏗️ **Architecture 2.0: SharedStateOrchestrator**

**Major architectural breakthrough**: We've completely rewritten the execution engine with a clean, maintainable OOP design that makes the system incredibly robust and extensible.

### **What's New:**
- **🎯 Centralized State Management**: Single global state dictionary for all cross-language variables
- **🔄 Placeholder-Based Processing**: Elegant nested block handling without complex position tracking
- **📦 Modular Design**: Clear separation of concerns across specialized methods
- **🛡️ Type Safety**: Full TypeScript-style type hints throughout the codebase
- **🔧 Enhanced Maintainability**: Easy to understand, modify, and extend

The new `SharedStateOrchestrator` class replaces the previous 900+ line monolithic approach with clean, testable methods while preserving 100% backward compatibility.

🌐 **[Live Demo](https://polygot-interpreter-zcom.vercel.app/)** | 📚 **[GitHub Repo](https://github.com/Siva-PythonPirates/polygot-interpreter)**

---

## ✨ Revolutionary Features

### 🔄 **Sequential Multi-Language Execution**

Write C, Python, and Java code in sequence with **automatic variable sharing** - no manual JSON handling required!

```poly
::c
int nums[] = {50, 25, 75, 100, 10};
float pi = 3.14f;
char name[] = "Polyglot";
::/c

::py
# Variables from C are automatically available!
nums.sort()
pi_doubled = pi * 2
message = f"Hello from {name}! Pi doubled = {pi_doubled}"
::/py

::java
// All variables seamlessly passed to Java
System.out.println("Sorted numbers: " + Arrays.toString(nums));
System.out.println("Message: " + message);
::/java
```

---

### 🎯 **Revolutionary Nested Language Blocks**

**World's first** nested language execution with **two powerful modes**:

#### **🔄 Loop-Based Nested Execution**
Embed multiple languages inside C loops with automatic iteration:

```poly
::py
results = []
::/py

::c
int numbers[] = {1, 2, 3, 4, 5};
for(int i = 0; i < 5; i++) {
    ::py 
    print(f"Processing number {numbers[i]}")
    results.append(numbers[i] ** 2)
    ::/py
    
    ::java 
    System.out.println("Java says: " + numbers[i] + " squared!");
    ::/java
}
::/c

::py
print("Final results:", results)
::/py
```

#### **⚡ Simple Nested Execution**
Cross-language variable sharing within single blocks:

```poly
::c
int a = 5;
int b = 10;

::py
result = a * b * 2
print("Python calculated:", result)
::/py

printf("C result: %d\n", a + b + result);
::/c
```

✨ **Magic Features:**
- **Automatic variable extraction**: C variables (`a`, `b`) automatically available in Python
- **Bidirectional communication**: Python results (`result`) automatically available in C
- **Cross-language type conversion**: Seamless int, float, string, array conversions
- **Real-time execution**: WebSocket streaming shows each step

---

### 🎛️ **Smart Debug Mode Toggle**

Perfect for both development and production use:

* **🔍 Debug ON**: Detailed execution pipeline, variable tracking, state transitions
* **✨ Debug OFF**: Clean output showing only your program results

---

### 🌐 **Professional Web Interface**

* **🖥️ Live code editor** with multi-language syntax highlighting
* **⚡ Real-time WebSocket execution** for instant feedback
* **📁 File upload/download** for `.poly` files
* **📱 Responsive design** that works everywhere
* **🎨 Dark theme** optimized for coding

---

### 🏗️ **Intelligent Variable Management**

* **🔍 Static analysis** detects variable declarations and modifications
* **🔄 Automatic type conversion** between languages (int[], List, int[])
* **📊 Cross-language data structures** (arrays, strings, objects)
* **🎯 Smart variable injection** eliminates manual JSON handling

---

## 🎯 Advanced Examples

### **Complex Data Processing Pipeline**

```poly
::c
int sales_data[] = {150, 200, 175, 300, 250};
char region[] = "North America";
float tax_rate = 0.08f;
::/c

::py
import statistics
total_sales = sum(sales_data)
avg_sales = statistics.mean(sales_data)
tax_amount = total_sales * tax_rate
report = {
    "region": region,
    "total": total_sales,
    "average": round(avg_sales, 2),
    "tax_due": round(tax_amount, 2)
}
::/py

::java
System.out.println("=== SALES ANALYSIS REPORT ===");
System.out.println("Region: " + report.get("region"));
System.out.println("Total Sales: $" + report.get("total"));
System.out.println("Tax Due: $" + report.get("tax_due"));
::/java
```

---

### **Nested Language Loops**

```poly
::c
int matrix[3][3] = {{1,2,3}, {4,5,6}, {7,8,9}};
printf("Processing matrix:\n");
for(int i = 0; i < 3; i++) {
    for(int j = 0; j < 3; j++) {
        printf("Element [%d][%d] = ", i, j);
        ::py print(matrix[i][j] ** 2) ::/py
        printf(" ");
    }
    printf("\n");
}
::/c
```

---

## 🛠️ Tech Stack & Architecture

### **Backend (Python)**

* **FastAPI** - High-performance async API framework
* **Docker** - Containerized execution environments for each language
* **WebSockets** - Real-time bidirectional communication
* **Advanced AST parsing** - Intelligent variable detection and injection

### **Frontend (React)**

* **Vite** - Lightning-fast build tool and dev server
* **Zustand** - Lightweight state management
* **React Simple Code Editor** - Syntax-highlighted code editing
* **Prism.js** - Multi-language syntax highlighting

### **Infrastructure**

* **Vercel** - Frontend deployment with auto-deployment from Git
* **GitHub Codespaces** - Backend hosting with Docker support
* **Cross-origin configured** - Seamless production communication

---

## 🚀 Getting Started

### 🎮 Try it Online (Recommended)

Visit **[https://polygot-interpreter-zcom.vercel.app/](https://polygot-interpreter-zcom.vercel.app/)** and start coding immediately!

### 💻 Local Development Setup

#### Prerequisites

* Docker Desktop (running)
* Node.js (v18+)
* Python (v3.8+)
* Git

#### Quick Start

```bash
# Clone the repository
git clone https://github.com/Siva-PythonPirates/polygot-interpreter.git
cd polygot-interpreter

# Backend setup
cd backend
pip install -r requirements.txt
python server.py

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

🌐 Open **[http://localhost:5173](http://localhost:5173)** to start coding!

---

### 🚀 Production Deployment

#### Frontend (Vercel)

1. Fork the repository
2. Connect to Vercel
3. Set environment variable: `VITE_BACKEND_URL=your-backend-url`
4. Deploy automatically on push to main

#### Backend (GitHub Codespaces)

1. Open repository in Codespaces
2. Run: `cd backend && python server.py`
3. Copy the Codespaces URL for frontend configuration

---

## 🧪 Testing & Development

### **Test Suite Organization**

All test files are organized in `backend/tests/` for a clean workspace:

```
backend/tests/
├── test_nested_debug.py          # Your simple nested code tests
├── test_websocket_nested.py      # WebSocket integration tests  
├── test_your_websocket.py        # Custom nested execution tests
├── test_enhanced_nested.py       # Advanced nested features
├── test_debug_toggle.py          # Debug mode functionality
└── ... (30+ comprehensive tests)
```

### **Run Tests**

```bash
cd backend

# Test simple nested execution
python tests/test_nested_debug.py

# Test WebSocket integration  
python tests/test_websocket_nested.py

# Test your custom code
python tests/test_your_websocket.py
```

### **Expected Output**

**Simple Nested Execution:**
```
=== Testing NESTED with DEBUG_MODE = True ===
🔄 No loop found - executing simple nested blocks
🔄 Extracted C variables: {'a': 5, 'b': 10}
Python calculated: 100
C result: 115

=== Testing NESTED with DEBUG_MODE = False ===
Python calculated: 100
C result: 115
```

---

## 📊 What Makes This Special?

### 🌟 Innovation Highlights

* **🎯 Dual nested execution modes** - Loop-based iteration + simple cross-language blocks  
* **⚡ Zero boilerplate** - Automatic variable extraction and injection
* **🔄 Bidirectional communication** - Variables flow seamlessly between languages
* **🌐 Production-ready** - Full Vercel + Codespaces deployment pipeline
* **🎛️ Professional developer experience** - Debug toggle, WebSocket streaming, clean UI
* **📱 Cross-platform** - Works in any browser, no local setup required
* **🧪 Comprehensive testing** - 30+ test cases covering all execution modes

### 🔬 Technical Achievements

* **🧠 Advanced nested block parsing** - Detects loop vs simple nested structures
* **🔄 Smart variable extraction** - C int declarations automatically parsed and injected  
* **⚡ Bidirectional state management** - Python results automatically available in C
* **🌊 Real-time WebSocket streaming** - Live execution feedback with debug toggle
* **🐳 Secure Docker execution** - Isolated containers for each language
* **🎨 Professional UI/UX** - Syntax highlighting, file upload, responsive design
* **🧪 Comprehensive test suite** - 30+ test cases in organized structure

### 🏗️ **SharedStateOrchestrator Architecture**

The heart of the system is the new `SharedStateOrchestrator` class that provides:

```python
class SharedStateOrchestrator:
    def __init__(self):
        self.global_state = {}  # Centralized variable storage
        self.language_contexts = {}  # Language-specific contexts
    
    def parse_mixed_structure(code_str) -> List[Dict]  # Smart parsing
    def execute_blocks(blocks) -> None                  # Unified execution
    def extract_variable_references(code, lang) -> set  # Variable analysis
    def inject_variable_declarations(lang, vars) -> str # Code generation
```

**Key Benefits:**
- **🎯 Single Source of Truth**: All variables managed in `global_state`
- **🔄 Smart Parsing**: Handles sequential, nested, and mixed structures
- **🛡️ Type Safety**: Full typing support for better development experience
- **📦 Modular Methods**: Each concern handled by specialized methods
- **🔧 Easy Extension**: Adding new languages is straightforward

---

## 🎯 Use Cases

* **Algorithm prototyping** - leverage each language's strengths
* **Educational tool** - learn multiple languages simultaneously
* **Cross-language integration** - bridge existing codebases
* **Performance comparison** - implement same logic in different languages
* **Polyglot development** - unified workflow for multi-language projects

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

* **🐛 Bug reports** - Found an issue? Let us know!
* **💡 Feature requests** - Have ideas? We'd love to hear them!
* **🔧 Pull requests** - Code improvements are always welcome!
* **📖 Documentation** - Help improve our docs!

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE.md](LICENSE.md) file for details.

**Free to use, modify, and distribute. Build something awesome!** 🚀

---

## 🙏 Acknowledgments

* **Docker** - For containerization technology
* **FastAPI** - For the excellent async Python framework
* **React ecosystem** - For powerful frontend tooling
* **Prism.js** - For beautiful syntax highlighting
* **Vercel & GitHub** - For seamless deployment platforms

---

**Built with ❤️ by [Siva-PythonPirates](https://github.com/Siva-PythonPirates)**

*"Breaking down language barriers, one line of code at a time."* 🌟
