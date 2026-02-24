# 💪 Muscle Recovery & Growth Tracker Bot
An asynchronous Telegram bot designed to optimize workout routines by tracking muscle recovery windows. It helps users prevent overtraining and maximize growth by visually displaying which muscle groups are fully recovered and ready for the next session.

## ✨ Features
* Interactive Dashboard: Users can view their current muscle recovery states directly in the chat using interactive inline keyboards.

* Smart Tracking: Automatically calculates a 72-hour recovery window from the exact moment a workout is logged.

* Visual Status Indicators: Uses a color-coded traffic light system (🔴 Untrained, 🟡 Recovering/Unready, 🟢 Ready) for quick status checks.

* Customizable Tracking: Users can easily add or remove specific muscle groups from their personal tracking list with a single click.

* Persistent Storage: Utilizes an asynchronous SQLite database to securely store user profiles, tracked muscles, and workout timestamps.

🛠 Tech Stack
Language: Python 3.10+

Framework: Aiogram 3.x (Asynchronous Telegram Bot API)

Database: SQLite3 with aiosqlite for non-blocking database operations

Architecture: Modular design with separated concerns (Handlers, Keyboards, Database, Configurations)

🗂 Project Structure
Plaintext
├── app/
│   ├── bot/
│   │   ├── bot.py          # Bot instance and Dispatcher initialization
│   │   ├── handlers.py     # Message, command, and callback query handlers
│   │   ├── keyboards.py    # Reply and Inline keyboard builders
│   │   └── states.py       # Finite State Machine (FSM) states
│   ├── database/
│   │   └── db.py           # Asynchronous database wrapper and queries
│   ├── config.py           # Environment variable management
│   └── messages.py         # Centralized static messages and texts
├── .env                    # Secret environment variables (TOKEN)
├── .gitignore              
├── main.py                 # Entry point
├── muscles.db              # SQLite database file (generated on run)
└── requirements.txt        # Python dependencies
## 🚀 Quick Start Commands
Once interacting with the bot, users have access to the following commands:

/show_my_muscles – Opens the dashboard to see exactly which muscles are Ready, Recovering, or Untrained. Click a muscle to log a workout.

/add_muscle – Add a new custom muscle group to track.

/remove_muscle – Select a muscle to stop tracking it.

/settings – Customize the recovery window or notification preferences.

## 💻 Installation & Setup
To run this bot locally, follow these steps:

- Clone the repository:

Bash
git clone https://github.com/Mafusail2020/training_schedule_bot.git
cd training_schedule_bot
- Create and activate a virtual environment:

Bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
- Install dependencies:

Bash
```pip install -r requirements.txt```
Environment Variables:
Create a .env file in the root directory and add your Telegram Bot Token (obtained from @BotFather):

```TOKEN=your_telegram_bot_token_here```
- Run the bot:

Bash
```python main.py```