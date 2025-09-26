````markdown
# 👽 The Polyglot Interpreter Project

> ⚡ A cutting-edge, experimental **polyglot development environment** that executes code written in multiple languages (C, Python, Java) seamlessly within a single pipeline.

This project isn’t just a tool — it’s a story of evolution. Starting as a simple proof-of-concept, it grew into a recursive, stack-based interpreter, and finally transformed into a compiler-like intelligent orchestrator that **automates state management across languages**.

![Screenshot of the Final Polyglot Interpreter UI](https://i.imgur.com/32ecb0.png)

---

## 🌌 Project Journey

### **Phase 1: Proof of Concept — Sequential Pipeline**
The first milestone was to see if C, Python, and Java could be executed in a row. While trivial at first, the **JSON contract** emerged as the universal bridge for state sharing.

**Contract:**
1. Input state is passed as a JSON string (CLI arg).
2. Block performs its logic.
3. Output state is serialized as JSON to `stdout`.

```poly
::c
int a[] = {50, 25, 75, 100, 10};
printf("{\"a\": [%d, %d, %d, %d, %d]}", a[0], a[1], a[2], a[3], a[4]);
::/c

::py
import json, sys
state = json.loads(sys.argv[1])
my_list = state.get("a", [])
my_list.sort()
print(json.dumps({"a": my_list}))
::/py

::java
String input = args.length > 0 ? args[0] : "{}";
String arrayData = input.substring(input.indexOf('[') + 1, input.indexOf(']'));
System.out.println("Final sorted array: [" + arrayData + "]");
::/java
````

🚨 **Challenge:** Every block needed manual JSON handling, which was clunky and inelegant.

---

### **Phase 2: Nested Execution & Call Stack**

We asked: *What if we could write code inside code?*

```poly
::c
  ::py
    ::java
```

This leap introduced a **call stack model**, executing code **inside-out**. Each nested block’s result became the input for its parent.

```poly
::c
printf("--- FINAL REPORT ---\\n");
printf("Analysis Complete.\\n");
printf("Top Product Found: %s\\n", top_product_name);
printf("Price: $%d\\n", top_product_price);

  ::java
  String input = args[0];
  String name = input.split(",")[0].split(":")[1].replace("\"", "");
  int price = Integer.parseInt(input.split(",")[1].split(":")[1].replace("}", "").trim());
  System.out.println("{\"top_product_name\": \"" + name + "\", \"top_product_price\": " + price + "}");

    ::py
    import json
    products = [
      {"name": "Laptop", "price": 1200, "category": "Electronics"},
      {"name": "Gaming Mouse", "price": 75, "category": "Electronics"}
    ]
    top_product = max(
        (p for p in products if p['category'] == 'Electronics'),
        key=lambda x: x['price']
    )
    print(json.dumps(top_product))
```

🚨 **Challenge:** Parsing nested syntax was fragile due to whitespace and regex limitations.

---

### **Phase 3: The Intelligent Engine**

The final orchestrator freed developers from JSON micromanagement by performing **automatic static analysis**:

✅ Detect variable declarations & modifications
✅ Inject JSON capture/serialization automatically
✅ Pass state across languages seamlessly
✅ Provide **debug mode** with professional logs

```poly
::c
int nums[] = {50, 25, 75, 100, 10};
float pi = 3.14f;
char grade = 'A';
char name[] = "Polyglot";
::/c

::py
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
::/java
```

**Sample Debug Log:**

```
==================================================
🔄 POLYGLOT EXECUTION PIPELINE STARTED
==================================================

🏗️ === BLOCK 1/3: C ===
🏁 Starting fresh (first block)
✏️ Variables created: ['nums', 'name', 'pi', 'grade']
📤 Passing to PY: ['nums', 'name', 'pi', 'grade']

🏗️ === BLOCK 2/3: PY ===
📥 Receiving vars: ['nums', 'name', 'pi', 'grade']
✏️ Modified: nums, Created: [message, pi_doubled, stats]
📤 Passing to JAVA: ['nums', 'message', 'pi_doubled']

🏗️ === BLOCK 3/3: JAVA ===
📥 Receiving vars: ['nums', 'message', 'pi_doubled']
---
=== Multi-Type Data Demo ===
Sorted numbers: 10 25 50 75 100 
Pi doubled: 6.28
Message: Student Polyglot got grade A

==================================================
✅ Pipeline completed successfully
```

---

## 🛠️ Tech Stack

| Layer           | Technology                          |
| --------------- | ----------------------------------- |
| **Backend API** | FastAPI (Python)                    |
| **Execution**   | Python `subprocess`                 |
| **Sandboxing**  | Docker (C, Python, Java)            |
| **Frontend**    | React (Vite)                        |
| **State Mgmt**  | Zustand                             |
| **Editor**      | React Simple Code Editor + Prism.js |

---

## 🚀 Getting Started

### Prerequisites

* Docker Desktop (running)
* Node.js (v18+)
* Python (v3.8+)
* Git

### Local Development

```bash
# Clone repo
git clone https://github.com/Siva-PythonPirates/polygot-interpreter.git
cd polyglot-interpreter

# Backend
cd backend
pip install -r requirements.txt
python server.py

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

🌐 Open: **[http://localhost:5173](http://localhost:5173)**

### Production Deployment

#### Frontend (Vercel)
- **Live Demo**: [https://polygot-interpreter-zcom.vercel.app/](https://polygot-interpreter-zcom.vercel.app/)
- Auto-deploys from `main` branch
- Environment variables configured for production backend

#### Backend (GitHub Codespaces)
- **API Endpoint**: `https://musical-waddle-rxwr97j7567cpjgw-8000.app.github.dev/`
- Docker containers for C, Python, Java execution
- WebSocket support for real-time communication

```bash
# Run in Codespaces
cd backend
python server.py
```

### Environment Configuration

The frontend automatically detects the environment:
- **Development**: Uses `http://localhost:8000`
- **Production**: Uses Codespaces URL or environment variable

**Environment Variables** (`.env`):
```bash
VITE_BACKEND_URL=https://your-codespace-url.app.github.dev
```

---

## 📊 Architecture

```mermaid
graph TD
    subgraph Browser
        A[React Web IDE] -- Polyglot Code (WebSocket) --> B
    end

    subgraph Server
        B(Python Orchestrator)
        B -- 1. C Code --> C{Docker (GCC)}
        C -- JSON State --> B
        B -- 2. Python Code --> D{Docker (Python)}
        D -- JSON State --> B
        B -- 3. Java Code --> E{Docker (OpenJDK)}
        E -- Final Output --> B
    end

    B -- Real-time Logs --> A
```

---

## 🤝 Contributing

Pull requests and feature suggestions are welcome! Feel free to open an issue and start the conversation.

---

## 📜 License

This project is licensed under the MIT License — free to use, modify, and distribute.

```
```
