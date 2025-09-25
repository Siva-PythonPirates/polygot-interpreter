from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from advanced_orchestrator import parse_code_to_tree, execute_tree_generator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            polyglot_code = await websocket.receive_text()
            
            tree = parse_code_to_tree(polyglot_code)
            if tree:
                for log_entry in execute_tree_generator(tree):
                    await websocket.send_text(log_entry)
            else:
                await websocket.send_text("❌ Error: Could not parse any code blocks.")
            
            await websocket.send_text("--- Pipeline Finished ---")

    except WebSocketDisconnect:
        print("Client disconnected.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)