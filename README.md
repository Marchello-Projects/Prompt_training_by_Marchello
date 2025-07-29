![logo](./app/imgs/202507282312.gif)

From beginner to AI whisperer — learn to craft powerful prompts and unlock the true potential of artificial intelligence. Your journey to prompt mastery starts here.

> [!CAUTION]
> To run the bot properly, at least 16 GB of RAM is recommended, since Mistral AI requires approximately 5 GB on its own.

# Aiogram, SQLite, Ollama (Mistral AI)

This project was built with the Aiogram framework, a powerful and modern tool for creating Telegram bots using Python.

<p align="center"><img src="./app/imgs/logo.webp"/></p>

SQLite serves as the primary database for this project, storing key information including user ID, prompt type, user-submitted prompts, and timestamps.

<p align="center"><img src="./app/imgs/Screenshot%20From%202025-07-28%2023-44-50.png" width="800" /></p>

The bot integrates Ollama to run the Mistral language model locally, allowing it to generate intelligent responses. Additionally, the bot can analyze and evaluate user prompts, providing feedback on their quality to help users improve their prompting skills

```python
try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": templates[mode].format(text=text),
            "stream": False,
        },
    )
    return response.json().get("response", "⚠️ No response returned.")
except Exception as e:
    return f"⚠️ Failed to connect to the AI model: {str(e)}"
```

## Getting Started

Follow these steps to run the Telegram bot locally:

### 1. Clone the repository

```bash
git clone https://github.com/Marchello-Projects/Prompt_training_by_Marchello
```

### 2. Create and activate virtual environment (optional but recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory with the following content:

```env
BOT_API_KEY=your_telegram_bot_token
```

> [!TIP]
> You can get the bot token from [BotFather](https://t.me/BotFather)

### 5. Set up the SQLite database

If it doesn't exist yet, create the table manually:

```sql
CREATE TABLE IF NOT EXISTS History (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	mode TEXT NOT NULL,
	prompt TEXT NOT NULL,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```
> [!NOTE]
> Before executing SQL query. Create date.db in app/database/ folder.

### 6. Install and run Ollama with Mistral

Make sure [Ollama](https://ollama.com) is installed on your system.

#### Install the Mistral model:

```bash
ollama pull mistral
```

#### Run Ollama in the background:

```bash
ollama serve &
```

You can test if it's working by sending a test request:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Hello!"
}'
```

### 7. Start the bot

```bash
python3 bot.py
```

---

✅ Your bot should now be running! Open Telegram and send a message to your bot to test it.
