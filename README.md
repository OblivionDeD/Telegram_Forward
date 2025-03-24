# Telegram Forward Bot
This project consists of two scripts:  
- **`user_session.py`** – listens to chats and forwards messages to the bot.  
- **`bot_session.py`** – processes commands and forwards messages to target chats.  

## Installation
### 1. Clone the repository
```sh
git clone https://github.com/OblivionDeD/Telegram_Forward.git
cd REPO_NAME
```

### 2. Install dependencies
Make sure you have Python 3.8+ installed, then install the required packages:
```sh
pip install -r requirements.txt  
```
### 3. Configure variables
Before running the scripts, set up your credentials in the files:
```
user_session.py:

api_id_user = ...

api_hash_user = '...'

BOT_USERNAME = '...'

bot_session.py:

api_id_bot = ...

api_hash_bot = '...'

bot_token = '...'

FORWARD_RULES – chat forwarding settings.
```
## Running the scripts
### Run both scripts in separate terminals:
```sh
python user_session.py  
```
```sh
python bot_session.py  
```
