# 💬 Chat Application with Kafka

A distributed chat application using Apache Kafka for message processing.
Implemented **Feature A**: all users exchange messages in **one shared topic**, seeing each other's messages in real time.
---

## 📌 Feature A: Single Kafka topic

Within Feature A:
- All users connect to a **single Kafka topic `chat`**
- All sent messages are visible to all users
- No separation by chat rooms (unlike Feature B)
- No message filtering (unlike Feature C)

---

## 🚀 Launching a Project (Universal Instructions)

### 🧩 Requirements

- Python 3.8+
- Apache Kafka (installed and configured)
- `zsh` (macOS default), `bash` or `cmd` (for Windows) installed
- Git

---

### 🔧 Installation

1. **Clone repository**

   ```bash
   git clone https://github.com/bluvvis/chat-kafka.git
   cd chat-kafka
   ```

2. **Create and activate a virtual environment**

   **macOS / Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows (cmd):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

### ⚙️ Launching Kafka

#### macOS (installed via Homebrew):

Open a separate terminal window and run:

```bash
zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties
```

Then in a new terminal window:

```bash
kafka-server-start /opt/homebrew/etc/kafka/server.properties
```

#### Linux (Kafka downloaded manually):

In the Kafka directory:

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

New window:

```bash
bin/kafka-server-start.sh config/server.properties
```

---

### 🧪 Creating a Kafka topic

Open a new terminal and run:

```bash
kafka-topics --create \
  --topic chat \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

Check the topic availability:

```bash
kafka-topics --list --bootstrap-server localhost:9092
```

---

#### Windows (Kafka downloaded manually):

In the Kafka directory:

```bash
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

New window:

```bash
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

---

### 🧪 Creating a Kafka topic

Open a new terminal and run:

```bash
kafka-topics.bat --create --bootstrap-server localhost:9092 --topic chat --partitions 1 --replication-factor 1
```

Check the topic availability:

```bash
kafka-topics.bat --list --bootstrap-server localhost:9092
```

---

### 💬 Starting a chat

1. **Window 1 - Consumer:**

   ```bash
   python3 consumer.py
   ```

   You should see:
   ```
   Kafka Chat Consumer started. Listening for messages...
   ```

2. **Window 2 - Producer (sender):**

   ```bash
   python3 producer.py
   ```

   Enter a username, such as `bluvvis`, and send messages.
They will appear in all running consumers.

3. **Multiple windows:**
    You can run multiple `producer.py` in separate terminals to emulate multiple users.
---

## ✅ Validation

- ✅ **General topic:** All users are connected to one topic `chat`
- ✅ **Real time:** Messages are instantly delivered and displayed
- ✅ **Verification:** Testing was carried out manually through several terminals (producer and consumer)
- ❌ **Isolation and filtering:** Not applicable - **Feature A** was selected according to the technical specifications
- ✅ **Message order:** The sending order is preserved
---

## 📁 Project structure

```bash
chat-kafka/
├── consumer.py         # Message recipient
├── producer.py         # Message Sender
├── requirements.txt    # Python Dependencies
├── README.md           # Project Description
└── venv/               # Virtual environment (add to .gitignore)
```

---

## 🧑‍💻 Authors

Grigorij Belaev, Farit Sharafutdinov, Batraz Dzesov, Stanislav Delyukov  
GitHub: [@bluvvis](https://github.com/bluvvis)
