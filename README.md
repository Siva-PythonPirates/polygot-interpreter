# polygot-interpreter
An interactive, web-based visualizer for classic operating system CPU scheduling algorithms like FCFS and SJF, built with Python and React


# 📈 Interactive OS Scheduler Visualizer

An educational project designed to demystify core operating system concepts by providing a real-time, animated visualization of CPU scheduling algorithms. This tool transforms abstract scheduling logic into a tangible, interactive timeline, making it easier to understand how an OS manages competing processes.

This project is part of a "Missing Semester of CS" series, focusing on hands-on implementation of fundamental computer science topics.

## Core Concepts Visualized
- **Process States:** Watch processes transition between READY, RUNNING, and TERMINATED states.
- **Ready Queue:** See how processes line up, waiting for their turn on the CPU.
- **CPU Timeline:** A dynamic Gantt chart that shows which process is running at any given moment.
- **Scheduling Algorithms:** Compare different strategies for process management.
  - First-Come, First-Served (FCFS)
  - Shortest Job First (SJF)
  - (Future) Round Robin, Priority Scheduling

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | **Python 3** | For running the core simulation logic. |
| **API** | **WebSockets** | For real-time, bidirectional communication between the backend and frontend. |
| **Frontend** | **React** | To build the interactive user interface and dashboard. |
| **Rendering** | **SVG / Framer Motion** | For smoothly animating the process timeline and state changes. |
| **Tooling** | **Node.js / npm** | For managing frontend dependencies and running the development server. |

---

## 🚀 Project Progress Tracker

This README will be updated as we complete each phase of development.

- [x] **Phase 1: Backend Simulation Core** (✅ Completed)
  - [x] Implemented `Process` and `Scheduler` data structures.
  - [x] Created a simulation engine using Python generators (`yield`).
  - [x] Developed logic for FCFS and non-preemptive SJF algorithms.
  - [x] Verified core logic via terminal output.

- [ ] **Phase 2: WebSocket API Layer** (⬜ To-Do)
  - [ ] Create a Python WebSocket server.
  - [ ] Integrate the scheduler engine with the server.
  - [ ] Define the JSON message structure for state updates.
  - [ ] Stream simulation state to connected clients.

- [ ] **Phase 3: Frontend UI & Visualization** (⬜ To-Do)
  - [ ] Set up a basic React application.
  - [ ] Build UI components for controls (start/stop, algorithm select).
  - [ ] Create components to display the Ready Queue and Terminated Processes.
  - [ ] Develop the main Timeline/Gantt chart visualization component.

- [ ] **Phase 4: Full Integration & Polish** (⬜ To-Do)
  - [ ] Connect the React frontend to the WebSocket backend.
  - [ ] Ensure real-time updates are rendered smoothly.
  - [ ] Add more algorithms (e.g., Round Robin).
  - [ ] Refine styling and user experience.

---

## ⚡ How to Run

### Phase 1 (Core Engine)
To run the standalone simulation engine and see the output in your terminal:
```bash
python scheduler_core.py
