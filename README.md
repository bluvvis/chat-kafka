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
```


```markdown
## 🚀 Как запустить проект

### 📦 Требования

- Python 3.8+
- Установленный [Apache Kafka](https://kafka.apache.org/quickstart) (включая Zookeeper, если используется классическая установка)
- Git

---

### 🔧 Установка

1. **Клонируй репозиторий:**

   ```bash
   git clone https://github.com/bluvvis/chat-kafka.git
   cd chat-kafka
   ```

2. **Создай виртуальное окружение и активируй его:**

   **macOS / Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows (cmd):**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Установи зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

---

### ⚙️ Запуск Kafka

Убедись, что Kafka и Zookeeper установлены и настроены.

**Если установлен через Homebrew (macOS):**

```bash
zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties
```

(в новом окне терминала)

```bash
kafka-server-start /opt/homebrew/etc/kafka/server.properties
```

**Если Kafka скачан вручную (Linux, Windows):**

В каталоге Kafka:

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

(новое окно)

```bash
bin/kafka-server-start.sh config/server.properties
```

---

### 💬 Запуск чата

1. **Открой одно окно терминала – это будет получатель (consumer):**

   ```bash
   python3 consumer.py
   ```

2. **Открой другое окно – это будет отправитель (producer):**

   ```bash
   python3 producer.py
   ```

Можно открыть несколько окон с `producer.py` и `consumer.py`, чтобы симулировать разных пользователей.

---

### ✅ Проверка

- Все пользователи отправляют и получают сообщения в одном Kafka-топике: `chat`
- Все сообщения видны всем пользователям
- Последовательность сообщений сохраняется
```

Можешь вставить это прямо в `README.md` — всё будет выглядеть красиво и понятно. Хочешь потом добавить ещё раздел о структуре проекта?
