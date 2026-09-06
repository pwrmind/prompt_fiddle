## STAGE 0: Decomposition of the Task

**Goal:** Create a Telegram bot in Python.  
**Approach:** Break the task into logical stages, from planning to deployment, with specific steps and defined expert roles for each stage.

---

## STAGE 1: Planning & Requirements Gathering

**Expert Role:** Solution Architect / Requirements Analyst  
**Goal:** Define what the bot should do, its core features, and technical constraints to avoid rework later.

### Steps:
1.  **Define Core Functionality:** Identify the primary purpose (e.g., echo bot, calculator, news aggregator, admin tool). *For this generic guide, we will build a modular "Echo + Help" bot as a foundation.*
2.  **Identify Key Features:** List specific interactions (commands like `/start`, `/help`; inline keyboards; file handling).
3.  **Select Technical Stack:** Choose the Python library (`python-telegram-bot` is industry standard for async/sync; `aiogram` for high-performance async). *Decision: Use `python-telegram-bot` v20+ (async) for its robustness and clear structure.*
4.  **Determine Deployment Environment:** Decide where the bot will run (local machine for testing, Docker container, cloud server like AWS/GCP/Heroku, or serverless). *Decision: Local development first, ready for Docker.*
5.  **Security & Credentials:** Plan how to store the Bot Token (environment variables, not hardcoded).

**Output of STAGE 1:**
*   **Bot Purpose:** A responsive Telegram bot that greets users, provides help info, and echoes messages.
*   **Tech Stack:** Python 3.9+, `python-telegram-bot` (v20+).
*   **Architecture:** Event-driven, async/await pattern.
*   **Security:** Token stored in `.env` file.

---

## STAGE 2: Environment Setup & Project Structure

**Expert Role:** DevOps Engineer / Build Specialist  
**Goal:** Prepare the local environment and establish a clean, scalable project structure.

### Steps:
1.  **Install Python & Virtual Environment:** Ensure Python is installed; create and activate a virtual environment (`venv`).
2.  **Create Project Directory:** Initialize folders for code, configs, and tests.
3.  **Set Up Dependency Management:** Create `requirements.txt` or `pyproject.toml`.
4.  **Configure Environment Variables:** Create a `.env` file to hold the `TELEGRAM_BOT_TOKEN`.
5.  **Initialize Git:** Set up version control with a proper `.gitignore` (exclude `.env`, `__pycache__`, etc.).

**Output of STAGE 2:**
*   **Directory Structure:**
    ```text
    my_telegram_bot/
    ├── .env                  # Stores TELEGRAM_BOT_TOKEN
    ├── .gitignore
    ├── requirements.txt
    ├── main.py               # Entry point
    ├── bot_handlers.py       # Contains callback functions
    └── config.py             # Loads env variables
    ```
*   **Dependencies:** `python-telegram-bot==20.7`, `python-dotenv`.

---

## STAGE 3: Bot Logic Implementation

**Expert Role:** Software Developer / Backend Engineer  
**Goal:** Write the actual code to handle Telegram updates, commands, and messages.

### Steps:
1.  **Token Loading:** Implement secure loading of the token from the `.env` file.
2.  **Application Initialization:** Set up the `Application` object with the token and error handlers.
3.  **Command Handlers:** Implement `/start` (greeting) and `/help` (usage instructions).
4.  **Message Handler:** Implement logic to echo user messages or process text.
5.  **Error Handling:** Add a global error handler to log exceptions and notify users gracefully.
6.  **Entry Point:** Configure the script to run the polling loop.

**Output of STAGE 3:**
*   **Code Implementation:** (See code block in STAGE 5).
*   **Logic Flow:** User sends message → Bot receives update → Router dispatches to handler → Handler processes logic → Bot sends response.

---

## STAGE 4: Testing & Debugging

**Expert Role:** QA Engineer / Tester  
**Goal:** Verify functionality, edge cases, and stability before deployment.

### Steps:
1.  **Unit Testing:** Write tests for individual handler functions (mocking the context and update objects).
2.  **Integration Testing:** Run the bot locally and interact via Telegram to verify commands and echo behavior.
3.  **Edge Case Analysis:** Test with empty messages, special characters, and large texts.
4.  **Logging Verification:** Ensure errors are logged correctly without exposing sensitive data.
5.  **Performance Check:** Verify response latency is acceptable.

**Output of STAGE 4:**
*   Passed test suite.
*   Confirmed behavior for `/start`, `/help`, and text echo.
*   Log file confirming no critical errors during testing.

---

## STAGE 5: Final Assembly & Deployment Readiness

**Expert Role:** Release Engineer / Deployment Specialist  
**Goal:** Package the solution so it can be easily deployed to production.

### Steps:
1.  **Code Consolidation:** Combine modular files into a final, clean state.
2.  **Dockerization (Optional but Recommended):** Create a `Dockerfile` to containerize the app.
3.  **Documentation:** Write a `README.md` with setup instructions, prerequisites, and how to run.
4.  **Final Review:** Check for any hardcoded secrets or missing dependencies.

**Output of STAGE 5:**
*   Complete, runnable code.
*   `Dockerfile` for containerization.
*   `README.md` instructions.
*   Ready-to-deploy package.

---

# Implementation: Stage 3 & 5 Combined (Final Code)

Here is the complete implementation based on the decomposition above.

### 1. `requirements.txt`
```text
python-telegram-bot==20.7
python-dotenv
```

### 2. `.env`
```text
TELEGRAM_BOT_TOKEN=your_bot_token_here
```
*(Replace `your_bot_token_here` with the token from @BotFather)*

### 3. `config.py`
```python
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")
```

### 4. `bot_handlers.py`
```python
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! 👋\nI'm your new Python Telegram bot.\n"
        "Try sending me a message or type /help for instructions."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /help command."""
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Greet the bot\n"
        "/help - Show this help message\n"
        "(Anything else) - I will echo your message back!"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echoes any non-command text message."""
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Logs errors and notifies the user."""
    print(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("Oops! Something went wrong on my end. Please try again later.")
```

### 5. `main.py` (Entry Point)
```python
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
from bot_handlers import start, help_command, echo, error_handler

def main():
    # Initialize the application with the token
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Handle all text messages that are not commands
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    
    # Add global error handler
    application.add_error_handler(error_handler)

    print("Bot is running...")
    # Start the bot (polling mode)
    application.run_polling()

if __name__ == '__main__':
    main()
```

### 6. `Dockerfile` (For Deployment)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### 7. `README.md`
```markdown
# Telegram Bot in Python

A simple, modular Telegram bot built with `python-telegram-bot`.

## Prerequisites
- Python 3.8+
- A Telegram Bot Token (get one from @BotFather)

## Setup
1. Clone this repository.
2. Create a `.env` file in the root directory and add your token:
   ```
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

## Docker Usage
To run via Docker:
```bash
docker build -t my-telegram-bot .
docker run --env-file .env my-telegram-bot
```
```

## Next Steps for You
1.  **Get a Token:** Open Telegram, search for `@BotFather`, create a new bot, and copy the API token.
2.  **Update `.env`:** Paste the token into the `.env` file.
3.  **Run:** Execute `python main.py`.
4.  **Interact:** Go to your bot in Telegram and type `/start`.

This structure ensures your bot is secure (no hardcoded tokens), maintainable (modular code), and deployable (Docker ready).