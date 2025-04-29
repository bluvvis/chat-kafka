from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'chat',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='chat-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Kafka Chat Consumer started. Listening for messages...\n")

for msg in consumer:
    data = msg.value
    print(f"[{data['user']}]: {data['message']}")

