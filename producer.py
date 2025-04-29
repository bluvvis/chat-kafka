from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Kafka Chat Producer started.")
username = input("Enter your username: ")

while True:
    message = input("Message: ")
    data = {'user': username, 'message': message}
    producer.send('chat', value=data)
    print("Message sent.")

