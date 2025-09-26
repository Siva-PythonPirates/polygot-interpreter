# 🚀 The Polyglot Interpreter Project`# 🚀 The Polyglot Interpreter Project



> ⚡ A revolutionary **cross-language development environment** that seamlessly executes C, Python, and Java code in a single pipeline with **automatic variable sharing**, **nested language blocks**, and **intelligent cross-language conversion**.> ⚡ A revolutionary **cross-language development environment** that seamlessly executes C, Python, and Java code in a single pipeline with **automatic variable sharing**, **nested language blocks**, and **intelligent cross-language conversion**.



This isn't just another code runner — it's a paradigm shift. What started as a proof-of-concept evolved into an intelligent orchestrator that breaks down language barriers, enabling developers to leverage the best features of each language in a unified workflow.This isn't just another code runner — it's a paradigm shift. What started as a proof-of-concept evolved into an intelligent orchestrator that breaks down language barriers, enabling developers to leverage the best features of each language in a unified workflow.



🌐 **[Live Demo](https://polygot-interpreter-zcom.vercel.app/)** | 📚 **[GitHub Repo](https://github.com/Siva-PythonPirates/polygot-interpreter)**🌐 **[Live Demo](https://polygot-interpreter-zcom.vercel.app/)** | 📚 **[GitHub Repo](https://github.com/Siva-PythonPirates/polygot-interpreter)**



![Polyglot Interpreter Demo](https://via.placeholder.com/800x400/1a1a1a/00ff88?text=🚀+Polyglot+Interpreter+Demo)![Polyglot Interpreter Demo](https://via.placeholder.com/800x400/1a1a1a/00ff88?text=🚀+Polyglot+Interpreter+Demo)down

# 👽 The Polyglot Interpreter Project

---

> ⚡ A cutting-edge, experimental **polyglot development environment** that executes code written in multiple languages (C, Python, Java) seamlessly within a single pipeline.

## ✨ Revolutionary Features

This project isn’t just a tool — it’s a story of evolution. Starting as a simple proof-of-concept, it grew into a recursive, stack-based interpreter, and finally transformed into a compiler-like intelligent orchestrator that **automates state management across languages**.

### 🔄 **Sequential Multi-Language Execution**

Write C, Python, and Java code in sequence with **automatic variable sharing** - no manual JSON handling required!![Screenshot of the Final Polyglot Interpreter UI](https://i.imgur.com/32ecb0.png)



```poly---

::c

int nums[] = {50, 25, 75, 100, 10};## ✨ Key Features

float pi = 3.14f;

char name[] = "Polyglot";### 🔄 **Sequential Multi-Language Execution**

::/cWrite C, Python, and Java code in sequence with **automatic variable sharing** - no manual JSON handling required!



::py```poly

# Variables from C are automatically available!::c

nums.sort()int nums[] = {50, 25, 75, 100, 10};

pi_doubled = pi * 2float pi = 3.14f;

message = f"Hello from {name}! Pi doubled = {pi_doubled}"char name[] = "Polyglot";

::/py::/c



::java::py

// All variables seamlessly passed to Java# Variables from C are automatically available!

System.out.println("Sorted numbers: " + Arrays.toString(nums));nums.sort()

System.out.println("Message: " + message);pi_doubled = pi * 2

::/javamessage = f"Hello from {name}! Pi doubled = {pi_doubled}"

```::/py



### 🎯 **Nested Language Blocks with Cross-Language Conversion**::java

**World's first** nested language execution: embed Python code inside C loops with **automatic syntax conversion**!// All variables seamlessly passed to Java

System.out.println("Sorted numbers: " + Arrays.toString(nums));

```polySystem.out.println("Message: " + message);

::c::/java

int numbers[] = {1, 2, 3, 4, 5};```

printf("Square calculations:\n");

for(int i = 0; i < 5; i++) {### 🎯 **Nested Language Blocks with Cross-Language Conversion**

    printf("Number %d squared = ", numbers[i]);Revolutionary feature: embed Python code inside C loops with **automatic syntax conversion**!

    ::py print(numbers[i] * numbers[i]) ::/py

}```poly

::/c::c

```int numbers[] = {1, 2, 3, 4, 5};

printf("Square calculations:\n");

**✨ Magic happens:** The Python `print()` statement automatically converts to C `printf()` calls during execution!for(int i = 0; i < 5; i++) {

    printf("Number %d squared = ", numbers[i]);

### 🎛️ **Smart Debug Mode Toggle**    ::py print(numbers[i] * numbers[i]) ::/py

Perfect for both development and production use:    printf("\n");

}

- **🔍 Debug ON**: Detailed execution pipeline, variable tracking, state transitions::/c

- **✨ Debug OFF**: Clean output showing only your program results```



**Debug Mode Example:****Magic happens:** `::py print(numbers[i] * numbers[i]) ::/py` automatically converts to `printf("%d\n", numbers[i] * numbers[i]);`

```

🏗️ === BLOCK 1/3: C ===### 🎛️ **Smart Debug Mode Toggle**

✏️ Variables created: ['nums', 'pi', 'name']- **Debug ON**: See detailed execution pipeline, variable tracking, and state transitions

📤 Passing to PY: ['nums', 'pi', 'name']- **Debug OFF**: Clean output with only your program results



🏗️ === BLOCK 2/3: PY ===### 🌐 **Real-Time Web Interface**

📥 Receiving vars: ['nums', 'pi', 'name']- **Live code editor** with syntax highlighting

🔄 Modified: nums, Created: [pi_doubled, message]- **WebSocket execution** for instant feedback

```- **File upload/download** for `.poly` files

- **Responsive design** that works everywhere

### 🌐 **Professional Web Interface**

- **🖥️ Live code editor** with multi-language syntax highlighting### � **Production-Ready Deployment**

- **⚡ Real-time WebSocket execution** for instant feedback- **Frontend**: Deployed on Vercel with auto-deployment

- **📁 File upload/download** for `.poly` files- **Backend**: Running on GitHub Codespaces with Docker containers

- **📱 Responsive design** that works on desktop, tablet, and mobile- **Cross-origin configured** for seamless communication

- **🎨 Dark theme** optimized for long coding sessions

---

### 🏗️ **Intelligent Variable Management**

- **🔍 Static analysis** detects variable declarations and modifications### **Phase 2: Nested Execution & Call Stack**

- **🔄 Automatic type conversion** between languages (int[], List, int[])

- **📊 Cross-language data structures** (arrays, strings, objects)We asked: *What if we could write code inside code?*

- **🎯 Smart variable injection** eliminates manual JSON handling

```poly

---::c

  ::py

## 🎯 Advanced Examples    ::java

```

### **Complex Data Processing Pipeline**

```polyThis leap introduced a **call stack model**, executing code **inside-out**. Each nested block’s result became the input for its parent.

::c

// Initialize dataset```poly

int sales_data[] = {150, 200, 175, 300, 250};::c

int num_records = 5;printf("--- FINAL REPORT ---\\n");

char region[] = "North America";printf("Analysis Complete.\\n");

float tax_rate = 0.08f;printf("Top Product Found: %s\\n", top_product_name);

::/cprintf("Price: $%d\\n", top_product_price);



::py  ::java

# Advanced analytics with Python  String input = args[0];

import statistics  String name = input.split(",")[0].split(":")[1].replace("\"", "");

total_sales = sum(sales_data)  int price = Integer.parseInt(input.split(",")[1].split(":")[1].replace("}", "").trim());

avg_sales = statistics.mean(sales_data)  System.out.println("{\"top_product_name\": \"" + name + "\", \"top_product_price\": " + price + "}");

max_sale = max(sales_data)

tax_amount = total_sales * tax_rate    ::py

report = {    import json

    "region": region,    products = [

    "total": total_sales,      {"name": "Laptop", "price": 1200, "category": "Electronics"},

    "average": round(avg_sales, 2),      {"name": "Gaming Mouse", "price": 75, "category": "Electronics"}

    "max_sale": max_sale,    ]

    "tax_due": round(tax_amount, 2)    top_product = max(

}        (p for p in products if p['category'] == 'Electronics'),

::/py        key=lambda x: x['price']

    )

::java    print(json.dumps(top_product))

// Professional reporting with Java```

System.out.println("=== SALES ANALYSIS REPORT ===");

System.out.println("Region: " + report.get("region"));🚨 **Challenge:** Parsing nested syntax was fragile due to whitespace and regex limitations.

System.out.println("Total Sales: $" + report.get("total"));

System.out.println("Average Sale: $" + report.get("average"));---

System.out.println("Best Sale: $" + report.get("max_sale"));

System.out.println("Tax Due: $" + report.get("tax_due"));### **Phase 3: The Intelligent Engine**

::/java

```The final orchestrator freed developers from JSON micromanagement by performing **automatic static analysis**:



### **Nested Language Loops**✅ Detect variable declarations & modifications

```poly✅ Inject JSON capture/serialization automatically

::c✅ Pass state across languages seamlessly

int matrix[3][3] = {{1,2,3}, {4,5,6}, {7,8,9}};✅ Provide **debug mode** with professional logs

printf("Processing matrix:\n");

for(int i = 0; i < 3; i++) {```poly

    for(int j = 0; j < 3; j++) {::c

        printf("Element [%d][%d] = ", i, j);int nums[] = {50, 25, 75, 100, 10};

        ::py print(matrix[i][j] ** 2) ::/pyfloat pi = 3.14f;

        printf(" ");char grade = 'A';

    }char name[] = "Polyglot";

    printf("\n");::/c

}

::/c::py

```nums.sort()

pi_doubled = pi * 2

---message = f"Student {name} got grade {grade}"

stats = {"count": len(nums), "max": max(nums)}

## 🛠️ Tech Stack & Architecture::/py



### **Backend (Python)**::java

- **FastAPI** - High-performance async API frameworkSystem.out.println("=== Multi-Type Data Demo ===");

- **Docker** - Containerized execution environments for each languageSystem.out.println("Sorted numbers: ");

- **WebSockets** - Real-time bidirectional communicationfor (int i = 0; i < nums.length; i++) {

- **Advanced AST parsing** - Intelligent variable detection and injection    System.out.print(nums[i] + " ");

}

### **Frontend (React)**System.out.println();

- **Vite** - Lightning-fast build tool and dev serverSystem.out.println("Pi doubled: " + pi_doubled);

- **Zustand** - Lightweight state managementSystem.out.println("Message: " + message);

- **React Simple Code Editor** - Syntax-highlighted code editing::/java

- **Prism.js** - Multi-language syntax highlighting```



### **Infrastructure****Sample Debug Log:**

- **Vercel** - Frontend deployment with auto-deployment from Git

- **GitHub Codespaces** - Backend hosting with Docker support```

- **Cross-origin configured** - Seamless production communication==================================================

🔄 POLYGLOT EXECUTION PIPELINE STARTED

```mermaid==================================================

graph TD

    subgraph "🌐 Frontend (Vercel)"🏗️ === BLOCK 1/3: C ===

        A[React Web IDE] 🏁 Starting fresh (first block)

        A1[Code Editor]✏️ Variables created: ['nums', 'name', 'pi', 'grade']

        A2[Debug Toggle]📤 Passing to PY: ['nums', 'name', 'pi', 'grade']

        A3[File Manager]

    end🏗️ === BLOCK 2/3: PY ===

📥 Receiving vars: ['nums', 'name', 'pi', 'grade']

    subgraph "🚀 Backend (Codespaces)"✏️ Modified: nums, Created: [message, pi_doubled, stats]

        B[FastAPI Server]📤 Passing to JAVA: ['nums', 'message', 'pi_doubled']

        C[Advanced Orchestrator]

        D[Variable Analyzer]🏗️ === BLOCK 3/3: JAVA ===

        E[Nested Parser]📥 Receiving vars: ['nums', 'message', 'pi_doubled']

    end---

=== Multi-Type Data Demo ===

    subgraph "🐳 Docker Containers"Sorted numbers: 10 25 50 75 100 

        F[GCC Container]Pi doubled: 6.28

        G[Python Container] Message: Student Polyglot got grade A

        H[OpenJDK Container]

    end==================================================

✅ Pipeline completed successfully

    A --> |WebSocket| B```

    B --> C

    C --> D---

    C --> E

    C --> |Execute C| F## 🛠️ Tech Stack

    C --> |Execute Python| G

    C --> |Execute Java| H| Layer           | Technology                          |

```| --------------- | ----------------------------------- |

| **Backend API** | FastAPI (Python)                    |

---| **Execution**   | Python `subprocess`                 |

| **Sandboxing**  | Docker (C, Python, Java)            |

## 🚀 Getting Started| **Frontend**    | React (Vite)                        |

| **State Mgmt**  | Zustand                             |

### **🎮 Try it Online (Recommended)**| **Editor**      | React Simple Code Editor + Prism.js |

Visit **[https://polygot-interpreter-zcom.vercel.app/](https://polygot-interpreter-zcom.vercel.app/)** and start coding immediately!

---

### **💻 Local Development Setup**

## 🚀 Getting Started

#### Prerequisites

- Docker Desktop (running)### Prerequisites

- Node.js (v18+)

- Python (v3.8+)* Docker Desktop (running)

- Git* Node.js (v18+)

* Python (v3.8+)

#### Quick Start* Git

```bash

# Clone the repository### Local Development

git clone https://github.com/Siva-PythonPirates/polygot-interpreter.git

cd polygot-interpreter```bash

# Clone repo

# Backend setupgit clone https://github.com/Siva-PythonPirates/polygot-interpreter.git

cd backendcd polyglot-interpreter

pip install -r requirements.txt

python server.py# Backend

cd backend

# Frontend setup (new terminal)pip install -r requirements.txt

cd frontendpython server.py

npm install

npm run dev# Frontend (in new terminal)

```cd frontend

npm install

🌐 Open **[http://localhost:5173](http://localhost:5173)** to start coding!npm run dev

```

### **🚀 Production Deployment**

🌐 Open: **[http://localhost:5173](http://localhost:5173)**

#### Frontend (Auto-deploy to Vercel)

1. Fork the repository### Production Deployment

2. Connect to Vercel

3. Set environment variable: `VITE_BACKEND_URL=your-backend-url`#### Frontend (Vercel)

4. Deploy automatically on push to main- **Live Demo**: [https://polygot-interpreter-zcom.vercel.app/](https://polygot-interpreter-zcom.vercel.app/)

- Auto-deploys from `main` branch

#### Backend (GitHub Codespaces)- Environment variables configured for production backend

1. Open repository in Codespaces

2. Run: `cd backend && python server.py`#### Backend (GitHub Codespaces)

3. Copy the Codespaces URL for frontend configuration- **API Endpoint**: `https://musical-waddle-rxwr97j7567cpjgw-8000.app.github.dev/`

- Docker containers for C, Python, Java execution

---- WebSocket support for real-time communication



## 📊 What Makes This Special?```bash

# Run in Codespaces

### **🌟 Innovation Highlights**cd backend

- **First-ever** nested language execution with automatic conversionpython server.py

- **Zero boilerplate** - no manual JSON state management```

- **Production-ready** - full deployment pipeline included

- **Developer experience** - professional debugging and clean output modes### Environment Configuration

- **Cross-platform** - works in browser, no local setup required

The frontend automatically detects the environment:

### **🔬 Technical Achievements**- **Development**: Uses `http://localhost:8000`

- **Advanced AST parsing** for variable detection across languages- **Production**: Uses Codespaces URL or environment variable

- **Intelligent type conversion** (C arrays ↔ Python lists ↔ Java arrays)

- **Real-time WebSocket pipeline** with proper error handling**Environment Variables** (`.env`):

- **Docker containerization** for secure, isolated execution```bash

- **Professional logging system** with emoji-enhanced debug outputVITE_BACKEND_URL=https://your-codespace-url.app.github.dev

```

### **🎯 Use Cases**

- **Algorithm prototyping** - leverage each language's strengths---

- **Educational tool** - learn multiple languages simultaneously

- **Cross-language integration** - bridge existing codebases## 📊 Architecture

- **Performance comparison** - implement same logic in different languages

- **Polyglot development** - unified workflow for multi-language projects```mermaid

graph TD

---    subgraph Browser

        A[React Web IDE] -- Polyglot Code (WebSocket) --> B

## 🤝 Contributing    end



We welcome contributions! Here's how you can help:    subgraph Server

        B(Python Orchestrator)

- **🐛 Bug reports** - Found an issue? Let us know!        B -- 1. C Code --> C{Docker (GCC)}

- **💡 Feature requests** - Have ideas? We'd love to hear them!        C -- JSON State --> B

- **🔧 Pull requests** - Code improvements are always welcome!        B -- 2. Python Code --> D{Docker (Python)}

- **📖 Documentation** - Help improve our docs!        D -- JSON State --> B

        B -- 3. Java Code --> E{Docker (OpenJDK)}

### Development Guidelines        E -- Final Output --> B

1. Fork the repository    end

2. Create a feature branch: `git checkout -b feature/amazing-feature`

3. Commit changes: `git commit -m 'Add amazing feature'`    B -- Real-time Logs --> A

4. Push to branch: `git push origin feature/amazing-feature````

5. Open a Pull Request

---

---

## 🤝 Contributing

## 📜 License

Pull requests and feature suggestions are welcome! Feel free to open an issue and start the conversation.

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

**Free to use, modify, and distribute. Build something awesome!** 🚀

## 📜 License

---

This project is licensed under the MIT License — free to use, modify, and distribute.

## 🙏 Acknowledgments

```

- **Docker** - For containerization technology```

- **FastAPI** - For the excellent async Python framework  
- **React ecosystem** - For powerful frontend tooling
- **Prism.js** - For beautiful syntax highlighting
- **Vercel & GitHub** - For seamless deployment platforms

---

**Built with ❤️ by [Siva-PythonPirates](https://github.com/Siva-PythonPirates)**

*"Breaking down language barriers, one line of code at a time."* 🌟