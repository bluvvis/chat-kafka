from kafka import KafkaProducer
import json
import atexit

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Kafka Chat Producer started.")
username = input("Enter your username: ")

producer.send('chat', value={'user': 'system', 'message': f'{username} joined the chat.'})
producer.flush()


def send_leave_message():
    producer.send('chat', value={'user': 'system', 'message': f'{username} left the chat.'})
    producer.flush()
    producer.close()


atexit.register(send_leave_message)
try:
    while True:
        message = input("Message: ")
        data = {'user': username, 'message': message}
        producer.send('chat', value=data)
        print("Message sent.")
except KeyboardInterrupt:
    print("\nExiting...")
    send_leave_message()
