import asyncio
import json
from kafka import KafkaConsumer
import websockets
from websockets.exceptions import ConnectionClosed

consumer = KafkaConsumer(
    'chat',
    bootstrap_servers=['localhost:9092'],
    group_id='chat-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

active_connections = set()

async def websocket_handler(websocket, path):
    active_connections.add(websocket)
    print(f"Новое WebSocket-подключение: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Получено от клиента: {message}")
    except ConnectionClosed:
        print(f"Подключение закрыто: {websocket.remote_address}")
    finally:
        active_connections.remove(websocket)

async def start_websocket_server():
    try:
        server = await websockets.serve(websocket_handler, "localhost", 8001)
        print("WebSocket сервер запущен на ws://localhost:8001")
        await server.wait_closed()
    except Exception as e:
        print(f"Ошибка запуска WebSocket-сервера: {e}")

async def consume_messages():
    while True:
        for message in consumer.poll(timeout_ms=1000).values():
            for msg in message:
                data = msg.value
                if 'user' in data and 'message' in data:
                    print(f"Получено из Kafka: [{data['user']}]: {data['message']}")
                    for ws in list(active_connections):
                        try:
                            await ws.send(json.dumps({"user": data['user'], "message": data['message']}))
                        except ConnectionClosed:
                            active_connections.remove(ws)
                else:
                    print("⚠️ Неверный формат сообщения:", data)
        await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(start_websocket_server(), consume_messages(), return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())
