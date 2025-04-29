```markdown
# 💬 Chat Application with Kafka

Реализация распределённого чата с использованием Apache Kafka.  
**Feature A**: все пользователи общаются в одном Kafka-топике — каждый видит все сообщения в реальном времени.

---

## 🚀 Как запустить проект

### 📦 Требования

- Python 3.8+
- Установленный [Apache Kafka](https://kafka.apache.org/quickstart) (включая Zookeeper)
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

#### Если установлен через Homebrew (macOS):

```bash
zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties
```

(в новом окне терминала)

```bash
kafka-server-start /opt/homebrew/etc/kafka/server.properties
```

#### Если Kafka скачан вручную (Linux, Windows):

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

(новое окно)

```bash
bin/kafka-server-start.sh config/server.properties
```

---

### 💬 Запуск чата

1. Открой **одно окно терминала** — это будет **получатель**:

   ```bash
   python3 consumer.py
   ```

2. Открой **другое окно терминала** — это будет **отправитель**:

   ```bash
   python3 producer.py
   ```

Можно открыть несколько окон `producer.py` и `consumer.py` — это будет имитация нескольких пользователей.

---

## ✅ Validation

- ✅ Все сообщения отправляются в Kafka-топик `chat`
- ✅ Все пользователи получают все сообщения (общий канал)
- ✅ Проверка происходила через два окна терминала (producer и consumer)
- ❌ Изоляция и фильтрация сообщений не реализованы — **это не требуется в Feature A**
- 📄 Сообщения отображаются в порядке отправки

---

## 📁 Структура проекта

```bash
chat-kafka/
├── consumer.py         # Получатель сообщений
├── producer.py         # Отправитель сообщений
├── requirements.txt    # Зависимости проекта
├── README.md           # Инструкция и описание
```

---

## 📌 Выбранная фича

**Feature A**: Все пользователи обмениваются сообщениями в одном общем топике Kafka.  
Это означает:

- Нет разделения по комнатам (в отличие от Feature B)
- Нет фильтрации сообщений (в отличие от Feature C)

---

## 📤 Автор

Grigorij Belaev, Farit Sharafutdinov, Batraz Dzesov, Stanislav Delyukov  
GitHub: [@bluvvis](https://github.com/bluvvis)
```

