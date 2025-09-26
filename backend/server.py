from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from advanced_orchestrator import parse_code_to_tree, execute_tree_generator, set_debug_mode, get_debug_mode

class DebugToggle(BaseModel):
    enabled: bool

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://polygot-interpreter-zcom.vercel.app",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/debug/toggle")
async def toggle_debug(debug_toggle: DebugToggle):
    """Toggle debug mode on/off"""
    set_debug_mode(debug_toggle.enabled)
    return {"debug_mode": get_debug_mode(), "message": f"Debug mode {'enabled' if debug_toggle.enabled else 'disabled'}"}

@app.get("/debug/status")
async def get_debug_status():
    """Get current debug mode status"""
    return {"debug_mode": get_debug_mode()}

@app.get("/version")
async def get_version():
    """Get backend version and features"""
    # Test if nested functionality is available
    try:
        from advanced_orchestrator import SharedStateOrchestrator
        # Test if orchestrator has nested methods
        orchestrator = SharedStateOrchestrator()
        nested_available = hasattr(orchestrator, 'execute_nested_blocks')
    except ImportError:
        nested_available = False
    
    return {
        "version": "4.0-revolutionary",
        "build_date": "2025-09-27", 
        "features": {
            "sequential_execution": True,
            "nested_blocks": nested_available,
            "cross_language_conversion": nested_available,
            "cross_language_variables": True,
            "debug_mode": True,
            "single_language_execution": True,
            "docker_containerized": True
        },
        "orchestrator": "SharedStateOrchestrator" if nested_available else "Legacy",
        "status": "ready"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("INFO:     connection open")
    try:
        while True:
            polyglot_code = await websocket.receive_text()
            print(f"Received code for execution:\n{polyglot_code}")
            
            await websocket.send_text("🚀 Starting pipeline...")
            
            try:
                # Use SharedStateOrchestrator directly
                from advanced_orchestrator import SharedStateOrchestrator
                orchestrator = SharedStateOrchestrator()
                
                # Capture all output by temporarily redirecting print
                import sys
                from io import StringIO
                
                # Create string buffer to capture output
                output_buffer = StringIO()
                original_stdout = sys.stdout
                
                try:
                    # Redirect stdout to capture print statements
                    sys.stdout = output_buffer
                    
                    # Execute the code
                    orchestrator.parse_and_execute(polyglot_code)
                    
                finally:
                    # Restore original stdout
                    sys.stdout = original_stdout
                
                # Send captured output to WebSocket
                output = output_buffer.getvalue()
                if output.strip():
                    for line in output.strip().split('\n'):
                        if line.strip():
                            await websocket.send_text(line)
                
            except Exception as e:
                await websocket.send_text(f"❌ Error: {e}")
                print(f"Execution error: {e}")
            
            await websocket.send_text("--- Pipeline Finished ---")

    except WebSocketDisconnect:
        print("Client disconnected.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)