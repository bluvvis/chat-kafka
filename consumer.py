import asyncio
import json
from kafka import KafkaConsumer
import websockets

consumer = KafkaConsumer(
    'chat',  # Убедитесь, что тема совпадает
    bootstrap_servers=['localhost:9092'],
    group_id='chat-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

active_connections = set()

async def websocket_handler(websocket, path):
    active_connections.add(websocket)
    print(f"Новое WebSocket-подключение: {websocket.remote_address}")
    try:
        while True:
            message = await websocket.recv()
            print(f"Получено от клиента: {message}")
    except websockets.exceptions.ConnectionClosed:
        print(f"Подключение закрыто: {websocket.remote_address}")
    finally:
        active_connections.remove(websocket)

async def start_websocket_server():
    server = await websockets.serve(websocket_handler, "localhost", 8001)
    print("WebSocket сервер запущен на ws://localhost:8001")
    await server.wait_closed()

async def consume_messages():
    websocket_task = asyncio.create_task(start_websocket_server())
    
    for message in consumer:
        data = message.value
        if 'user' in data and 'message' in data:
            print(f"Получено из Kafka: [{data['user']}]: {data['message']}")
            for ws in list(active_connections):  # Копируем список для безопасности
                try:
                    await ws.send(f"[{data['user']}]: {data['message']}")
                except websockets.exceptions.ConnectionClosed:
                    active_connections.remove(ws)
        else:
            print("⚠️ Неверный формат сообщения:", data)

if __name__ == "__main__":
    asyncio.run(consume_messages())
