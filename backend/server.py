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
        from advanced_orchestrator import parse_nested_structure
        nested_available = True
    except ImportError:
        nested_available = False
    
    return {
        "version": "3.0-nested",
        "build_date": "2025-09-26", 
        "features": {
            "sequential_execution": True,
            "nested_blocks": nested_available,
            "cross_language_variables": True,
            "debug_mode": True
        },
        "status": "ready"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            polyglot_code = await websocket.receive_text()
            
            # Parse the polyglot code into blocks
            blocks = parse_code_to_tree(polyglot_code)
            if blocks:
                # Execute the blocks sequentially
                for log_entry in execute_tree_generator(blocks):
                    await websocket.send_text(log_entry)
            else:
                await websocket.send_text("❌ Error: Could not parse any code blocks.")
            
            await websocket.send_text("--- Pipeline Finished ---")

    except WebSocketDisconnect:
        print("Client disconnected.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)