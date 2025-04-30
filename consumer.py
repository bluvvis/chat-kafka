import asyncio
import json
from kafka import KafkaConsumer
import websockets

# Kafka Consumer для чата
consumer = KafkaConsumer(
    'chat',
    bootstrap_servers=['localhost:9092'],
    group_id='chat-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Множество активных WebSocket подключений
active_connections = set()

# WebSocket-обработчик для новых подключений
async def websocket_handler(websocket, path):
    # Добавляем подключение в список активных
    active_connections.add(websocket)
    try:
        # Ожидаем сообщений от клиента (необязательно для чата, но может быть полезно)
        while True:
            message = await websocket.recv()
            print(f"Получено сообщение от клиента: {message}")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Убираем подключение из списка активных, когда оно закрывается
        active_connections.remove(websocket)

# Запуск WebSocket сервера на порту 8001
async def start_websocket_server():
    server = await websockets.serve(websocket_handler, "localhost", 8001)
    print("WebSocket сервер запущен на ws://localhost:8001")
    await server.wait_closed()

# Основной цикл для прослушивания сообщений из Kafka
async def consume_messages():
    # Запуск WebSocket сервера
    websocket_task = asyncio.create_task(start_websocket_server())
    
    for message in consumer:
        data = message.value
        # Проверяем, что сообщение содержит поля 'user' и 'message'
        if 'user' in data and 'message' in data:
            print(f"[{data['user']}]: {data['message']}")
            # Отправляем сообщение всем подключённым WebSocket клиентам
            for ws in active_connections:
                await ws.send(f"[{data['user']}]: {data['message']}")
        else:
            print("⚠️ Получено сообщение без user/message:", data)

# Запуск основного асинхронного процесса
if __name__ == "__main__":
    asyncio.run(consume_messages())
