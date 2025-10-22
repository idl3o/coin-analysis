from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import asyncio
import uvicorn

from api.routes import crypto_router
from services.websocket_manager import manager

app = FastAPI(title="Crypto Analysis API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(crypto_router, prefix="/api/crypto", tags=["crypto"])

@app.get("/")
async def root():
    return {"message": "Crypto Analysis API", "status": "running"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            # Send price updates every 10 seconds
            await asyncio.sleep(10)
            await manager.send_price_updates(websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
