# 💬 Chat Application with Kafka

Распределённое чат-приложение, использующее Apache Kafka для обработки сообщений.  
Реализована **Feature A**: все пользователи обмениваются сообщениями в **одном общем топике**, видя сообщения друг друга в реальном времени.

---

## 📌 Feature A: Общий Kafka-топик

В рамках фичи A:
- Все пользователи подключаются к **единому Kafka-топику `chat`**
- Все отправленные сообщения видны всем пользователям
- Нет разделения по чат-комнатам (в отличие от Feature B)
- Нет фильтрации сообщений (в отличие от Feature C)

---

## 🚀 Запуск проекта (универсальная инструкция)

### 🧩 Требования

- Python 3.8+
- Apache Kafka (установлен и настроен)
- Установленный `zsh` (macOS по умолчанию), `bash` или `cmd` (для Windows)
- Git

---

### 🔧 Установка

1. **Клонировать репозиторий**

   ```bash
   git clone https://github.com/bluvvis/chat-kafka.git
   cd chat-kafka
   ```

2. **Создать и активировать виртуальное окружение**

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

3. **Установить зависимости**

   ```bash
   pip install -r requirements.txt
   ```

---

### ⚙️ Запуск Kafka

#### macOS (установлено через Homebrew):

Открой отдельное окно терминала и выполни:

```bash
zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties
```

Затем в новом окне терминала:

```bash
kafka-server-start /opt/homebrew/etc/kafka/server.properties
```

#### Linux / Windows (Kafka скачан вручную):

В каталоге Kafka:

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Новое окно:

```bash
bin/kafka-server-start.sh config/server.properties
```

---

### 🧪 Создание Kafka-топика

Открой новый терминал и выполни:

```bash
kafka-topics --create \
  --topic chat \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

Проверь наличие топика:

```bash
kafka-topics --list --bootstrap-server localhost:9092
```

---

### 💬 Запуск чата

1. **Окно 1 — Consumer (получатель):**

   ```bash
   python3 consumer.py
   ```

   Должно появиться:
   ```
   Kafka Chat Consumer started. Listening for messages...
   ```

2. **Окно 2 — Producer (отправитель):**

   ```bash
   python3 producer.py
   ```

   Введи имя пользователя, например `bluvvis`, и отправляй сообщения.  
   Они появятся у всех запущенных consumer'ов.

3. **Множественные окна:**
   Можешь запустить несколько `producer.py` в отдельных терминалах, чтобы эмулировать нескольких пользователей.

---

## ✅ Validation

- ✅ **Общий топик:** Все пользователи подключены к одному топику `chat`
- ✅ **Реальное время:** Сообщения моментально доставляются и отображаются
- ✅ **Проверка:** Тестирование проводилось вручную через несколько терминалов (producer и consumer)
- ❌ **Изоляция и фильтрация:** Не применимы — по ТЗ выбрана **Feature A**
- ✅ **Порядок сообщений:** Сохраняется порядок отправки

---

## 📁 Структура проекта

```bash
chat-kafka/
├── consumer.py         # Получатель сообщений
├── producer.py         # Отправитель сообщений
├── requirements.txt    # Зависимости Python
├── README.md           # Описание проекта
└── venv/               # Виртуальное окружение (добавить в .gitignore)
```

---

## 🧑‍💻 Авторы

Grigorij Belaev, Farit Sharafutdinov, Batraz Dzesov, Stanislav Delyukov  
GitHub: [@bluvvis](https://github.com/bluvvis)
