from fastapi import WebSocket
from typing import List
import json
from services.crypto_service import CryptoService

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.crypto_service = CryptoService()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_price_updates(self, websocket: WebSocket):
        """Send price updates for top cryptocurrencies"""
        try:
            # Get prices for popular cryptocurrencies
            symbols = ["BTC", "ETH", "BNB", "SOL", "ADA"]
            prices = await self.crypto_service.get_multiple_prices(symbols)

            message = json.dumps({
                "type": "price_update",
                "data": prices
            })

            await self.send_personal_message(message, websocket)
        except Exception as e:
            print(f"Error sending price updates: {e}")

manager = ConnectionManager()
