# 👽 Polyglot Interpreter

An experimental, web-based development environment that executes code written in multiple languages (C, Python, Java) within a single, sequential pipeline. This project proves that it's possible to pass program state between completely isolated, containerized language runtimes, creating a powerful tool for both learning and experimentation.

This project was built as a "Missing Semester of CS" exercise to explore deep concepts in compilers, containerization, and systems architecture.

![Screenshot of the Polyglot Interpreter UI](https://i.imgur.com/7s1tP8v.png)

## ✨ Core Features & Concepts

This project isn't just a tool; it's a hands-on demonstration of several crucial computer science principles.

| Feature / Concept | Description |
| :--- | :--- |
| **Multi-Language Execution** | Write and run C, Python, and Java code in a single program flow. |
| **State Serialization** | See how program state is converted to a universal format (JSON) to be passed between processes. |
| **Container Sandboxing** | Every code block is executed in a secure, isolated Docker container, preventing side effects. |
| **Web-Based IDE** | A modern, responsive frontend built with React provides a user-friendly coding experience. |
| **Microservice Pattern** | This project is a miniature simulation of a microservice architecture, where small, independent services (our language runners) cooperate to perform a larger task. |

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend API** | **FastAPI (Python)** | A modern, high-performance web framework for the WebSocket server. |
| **Orchestrator** | **Python `subprocess`** | Manages the Docker build/run lifecycle for each code block. |
| **Sandboxing** | **Docker** | Provides isolated, reproducible environments for C, Python, and Java. |
| **Frontend** | **React (with Vite)** | A fast, modern library for building the interactive user interface. |
| **State Management** | **Zustand** | A minimal, fast state management library for React. |
| **Code Editor** | **React Simple Code Editor & Prism.js** | For a lightweight yet powerful in-browser code editing experience with syntax highlighting. |

<details>
<summary>Click to view System Architecture Diagram</summary>

```mermaid
graph TD
    subgraph Browser
        A[React Web IDE] -- Polyglot Code (WebSocket) --> B;
    end

    subgraph Server
        B(Python Orchestrator);
        B -- 1. C Code --> C{Docker Container (GCC)};
        C -- 2. JSON State (stdout) --> B;
        B -- 3. Python Code + JSON State --> D{Docker Container (Python)};
        D -- 4. JSON State (stdout) --> B;
        B -- 5. Java Code + JSON State --> E{Docker Container (OpenJDK)};
        E -- 6. Final Output (stdout) --> B;
    end

    B -- Real-time Logs (WebSocket) --> A;
</details>
Of course. Here is the complete and detailed README in a single markdown block for you to copy and paste.

Markdown

# 👽 Polyglot Interpreter

An experimental, web-based development environment that executes code written in multiple languages (C, Python, Java) within a single, sequential pipeline. This project proves that it's possible to pass program state between completely isolated, containerized language runtimes, creating a powerful tool for both learning and experimentation.

This project was built as a "Missing Semester of CS" exercise to explore deep concepts in compilers, containerization, and systems architecture.

![Screenshot of the Polyglot Interpreter UI](https://i.imgur.com/7s1tP8v.png)

## ✨ Core Features & Concepts

This project isn't just a tool; it's a hands-on demonstration of several crucial computer science principles.

| Feature / Concept | Description |
| :--- | :--- |
| **Multi-Language Execution** | Write and run C, Python, and Java code in a single program flow. |
| **State Serialization** | See how program state is converted to a universal format (JSON) to be passed between processes. |
| **Container Sandboxing** | Every code block is executed in a secure, isolated Docker container, preventing side effects. |
| **Web-Based IDE** | A modern, responsive frontend built with React provides a user-friendly coding experience. |
| **Microservice Pattern** | This project is a miniature simulation of a microservice architecture, where small, independent services (our language runners) cooperate to perform a larger task. |

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend API** | **FastAPI (Python)** | A modern, high-performance web framework for the WebSocket server. |
| **Orchestrator** | **Python `subprocess`** | Manages the Docker build/run lifecycle for each code block. |
| **Sandboxing** | **Docker** | Provides isolated, reproducible environments for C, Python, and Java. |
| **Frontend** | **React (with Vite)** | A fast, modern library for building the interactive user interface. |
| **State Management** | **Zustand** | A minimal, fast state management library for React. |
| **Code Editor** | **React Simple Code Editor & Prism.js** | For a lightweight yet powerful in-browser code editing experience with syntax highlighting. |

<details>
<summary>Click to view System Architecture Diagram</summary>

```mermaid
graph TD
    subgraph Browser
        A[React Web IDE] -- Polyglot Code (WebSocket) --> B;
    end

    subgraph Server
        B(Python Orchestrator);
        B -- 1. C Code --> C{Docker Container (GCC)};
        C -- 2. JSON State (stdout) --> B;
        B -- 3. Python Code + JSON State --> D{Docker Container (Python)};
        D -- 4. JSON State (stdout) --> B;
        B -- 5. Java Code + JSON State --> E{Docker Container (OpenJDK)};
        E -- 6. Final Output (stdout) --> B;
    end

    B -- Real-time Logs (WebSocket) --> A;
</details>

🚀 Getting Started
Follow these instructions to get the project running on your local machine.

Prerequisites
Docker Desktop: Must be installed and running.

Node.js & npm: v18 or later.

Python: v3.8 or later.

Git: For cloning the repository.

Installation & Setup
Clone the repository:

Bash

git clone [https://github.com/YOUR_USERNAME/polyglot-interpreter.git](https://github.com/YOUR_USERNAME/polyglot-interpreter.git)
cd polyglot-interpreter
Setup the Backend (Terminal 1):

Bash

cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn server:app --reload
The backend will be running at http://localhost:8000.

Setup the Frontend (Terminal 2):

Bash

cd frontend

# Install Node.js dependencies
npm install

# Run the Vite development server
npm run dev
The frontend will be available at http://localhost:5173.

Launch the App!
Open your web browser and navigate to http://localhost:5173.

📝 How It Works: The Polyglot Contract
To write your own programs, your code must follow a simple contract:

Language Blocks: Each block must start with ::lang (e.g., ::c, ::py, ::java).

Initial State: The first block (usually C) is responsible for creating the initial state and printing it to standard output (stdout) as a JSON-compatible string.

State Passing: Subsequent blocks receive the state from the previous block as a single command-line argument (argv). They must perform their logic and print the new state to stdout as a complete JSON string to pass it to the next block.

🌟 Future Enhancements
Add More Languages: Incorporate runners for Go, Rust, and JavaScript (Node.js).

Error Highlighting: Improve the editor to show syntax errors.

State Inspector: A UI panel to visualize the JSON state object as it changes between steps.

User Accounts: Allow users to save and share their polyglot scripts.