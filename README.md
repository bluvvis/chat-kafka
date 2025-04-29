# DNP_Project_3

# Chat Application with Kafka — Feature A

This is a simple distributed chat application using Apache Kafka, implementing **Feature A**:
> All users chat in a **single Kafka topic** and receive each other’s messages in real-time.

## ✅ Features

- All messages go to one Kafka topic: `chat`
- Every user can send and receive messages
- Simple terminal-based producer and consumer

## 📦 Requirements

- Python 3.x
- Apache Kafka (KRaft mode — no Zookeeper)
- `kafka-python` library

Install dependencies:
```bash
pip install -r requirements.txt

