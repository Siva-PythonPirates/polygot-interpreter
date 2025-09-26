# 🚀 The Polyglot Interpreter Project

> ⚡ A revolutionary **cross-language development environment** that seamlessly executes C, Python, and Java code in a single pipeline with **automatic variable sharing**, **nested language blocks**, and **intelligent cross-language conversion**.

This isn't just another code runner — it's a paradigm shift. What started as a proof-of-concept evolved into an intelligent orchestrator that breaks down language barriers, enabling developers to leverage the best features of each language in a unified workflow.

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

### 🎯 **Nested Language Blocks with Cross-Language Conversion**

**World's first** nested language execution: embed Python code inside C loops with **automatic syntax conversion**!

```poly
::c
int numbers[] = {1, 2, 3, 4, 5};
printf("Square calculations:\n");
for(int i = 0; i < 5; i++) {
    printf("Number %d squared = ", numbers[i]);
    ::py print(numbers[i] * numbers[i]) ::/py
}
::/c
```

✨ Magic happens: The Python `print()` statement automatically converts to C `printf()` calls during execution!

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

## 📊 What Makes This Special?

### 🌟 Innovation Highlights

* **First-ever** nested language execution with automatic conversion
* **Zero boilerplate** - no manual JSON state management
* **Production-ready** - full deployment pipeline included
* **Developer experience** - professional debugging and clean output modes
* **Cross-platform** - works in browser, no local setup required

### 🔬 Technical Achievements

* **Advanced AST parsing** for variable detection across languages
* **Intelligent type conversion** (C arrays ↔ Python lists ↔ Java arrays)
* **Real-time WebSocket pipeline** with proper error handling
* **Docker containerization** for secure, isolated execution
* **Professional logging system** with emoji-enhanced debug output

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

### Development Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

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
