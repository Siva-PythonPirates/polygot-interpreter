# 📁 Project Structure

Clean, organized workspace for the Polyglot Interpreter project.

## 🏗️ Root Directory

```
polygot-interpreter/
├── 📄 README.md              # Comprehensive project documentation
├── 📄 CHANGELOG.md           # Version history and updates  
├── 📄 LICENSE.md             # MIT license
├── 📁 backend/               # Python FastAPI backend
├── 📁 frontend/              # React + Vite frontend
└── 🔧 .gitignore            # Git ignore rules
```

## 🐍 Backend Structure

```
backend/
├── 🎯 server.py                    # FastAPI WebSocket server (main entry)
├── 🧠 advanced_orchestrator.py     # SharedStateOrchestrator (core engine)
├── ⚙️ engine.py                   # Docker execution engine
├── 📦 requirements.txt            # Python dependencies
├── 🐳 *.Dockerfile              # Docker containers (py, c, java)
├── 📁 tests/                    # All test files (organized)
│   ├── test_nested_debug.py      # Simple nested execution tests
│   ├── test_websocket_nested.py  # WebSocket integration tests
│   ├── test_your_websocket.py    # Custom nested tests
│   ├── test_enhanced_nested.py   # Advanced features
│   └── ... (30+ comprehensive tests)
└── 📁 __pycache__/              # Python cache (auto-generated)
```

## ⚛️ Frontend Structure

```
frontend/
├── 📦 package.json              # Node.js dependencies
├── ⚙️ vite.config.js           # Vite build configuration
├── 🌐 vercel.json              # Vercel deployment config
├── 📄 index.html               # Main HTML template
├── 📁 src/                     # React source code
│   ├── 🎯 main.jsx              # React app entry point
│   ├── 🏠 App.jsx               # Main React component
│   ├── 🎨 App.css               # Component styles
│   └── 🎨 index.css             # Global styles
├── 📁 public/                  # Static assets
│   └── 🖼️ vite.svg             # Vite logo
└── 📁 node_modules/            # Dependencies (auto-generated)
```

## 🧪 Tests Organization

All temporary and test files are organized in `backend/tests/` for a clean workspace:

### **Core Functionality Tests**
- `test_nested_debug.py` - Simple nested execution (your code)
- `test_websocket_nested.py` - WebSocket streaming integration
- `test_enhanced_nested.py` - Advanced nested features
- `test_debug_toggle.py` - Debug mode functionality

### **Integration Tests** 
- `test_backend_integration.py` - Backend API testing
- `test_frontend_example.py` - Frontend compatibility
- `test_server_behavior.py` - WebSocket server behavior

### **Execution Mode Tests**
- `test_c_only.py` - Single language execution
- `test_multi_type.py` - Cross-language type conversion  
- `test_array_sort.py` - Complex data processing

### **Legacy & Backup Files**
- `*_backup.py` - Backup versions
- `working_*.py` - Development iterations
- `debug_*.py` - Debug utilities

## 🛡️ Clean Workspace Benefits

### ✅ **Organized Structure**
- Main code separated from test files
- Clear separation of concerns
- Easy to navigate and understand

### ✅ **Development Friendly**
- Tests easily runnable: `python tests/test_name.py`  
- No clutter in main directories
- Git history remains clean

### ✅ **Production Ready**
- Only essential files in root
- Clean deployment structure
- Professional project organization

### ✅ **Maintainable**
- Easy to find specific functionality
- Clear file naming conventions
- Logical grouping by purpose

## 🚀 Quick Navigation

### **Main Development Files**
- **Backend Logic**: `backend/advanced_orchestrator.py`
- **API Server**: `backend/server.py`  
- **Frontend App**: `frontend/src/App.jsx`
- **Styling**: `frontend/src/index.css`

### **Testing & Debug**
- **Run Your Code**: `python backend/tests/test_nested_debug.py`
- **WebSocket Test**: `python backend/tests/test_websocket_nested.py`
- **All Tests**: `cd backend/tests && python test_*.py`

### **Configuration**
- **Backend Setup**: `backend/requirements.txt`
- **Frontend Setup**: `frontend/package.json`  
- **Deployment**: `frontend/vercel.json`

---

**Clean, organized, and ready for development! 🎯**