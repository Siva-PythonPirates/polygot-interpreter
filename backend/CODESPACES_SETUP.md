# 🚀 GitHub Codespaces Setup Guide

## Quick Start in GitHub Codespaces

### 1. **Navigate to Backend Directory**
```bash
cd backend
```

### 2. **Install Dependencies**
```bash
pip install fastapi uvicorn websockets
```

### 3. **Start the Server**
```bash
python server.py
```

The server will start on `http://0.0.0.0:8000` and will be accessible via GitHub Codespaces port forwarding.

## 🎯 **Testing Your Nested Syntax**

Once the server is running, you can test your nested syntax via WebSocket:

### Example Nested Code:
```polyglot
::c
int a[] = {1, 2, 3, 4, 5};
for(int i = 0; i < 5; i++) {
    ::py print("Print in python - ",a[i]) ::/py
    ::java System.out.println("Sout from Java - "+a[i]) ::/java
}
::/c
```

## 🔧 **API Endpoints:**

- **WebSocket**: `ws://localhost:8000/ws` - Main polyglot execution
- **Version**: `GET /version` - Check server capabilities  
- **Debug Toggle**: `POST /debug/toggle` - Enable/disable debug mode
- **Debug Status**: `GET /debug/status` - Check current debug mode

## 🐳 **Docker Requirements:**

Your server requires Docker to be available for language execution. In GitHub Codespaces:

1. **Check Docker availability**:
```bash
docker --version
```

2. **If Docker isn't available**, the server will still start but execution will fail. GitHub Codespaces should have Docker pre-installed.

## 🌐 **Frontend Integration:**

Your frontend should connect to the WebSocket endpoint. In Codespaces, the port will be automatically forwarded and you'll get a public URL.

## 🎉 **Features Available:**

✅ **Sequential Execution** - Multiple language blocks with state sharing  
✅ **Nested Execution** - Revolutionary syntax with cross-language conversion  
✅ **Single Language** - Java, Python, C execution  
✅ **Debug Mode** - Comprehensive logging and state tracking  
✅ **Cross-Language Variables** - Seamless data transfer between languages  

Your nested syntax now works perfectly! 🚀