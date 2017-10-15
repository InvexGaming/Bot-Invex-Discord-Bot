Bot Invex Discord Bot
=========
Bot for Invex Gaming Discord Server.

Requirements
-----
* python3 (3.6+)
* discord.py#rewrite module (https://github.com/Rapptz/discord.py)
* screen (optional)

Usage
-----
1. Enter required configuration details into `config.ini`:

```
[DEFAULT]
TOKEN = REMOVED
CLIENTID = REMOVED
INVEXGUILD = REMOVED
PREFIX = !

[DB]
HOST = localhost
PORT = 3306
USER = root
PASSWORD = REMOVED
DATABASE = REMOVED

[CHANNELUTILITIES]
VOICE_CHANNEL_CATEGORY_ID = REMOVED
TEXT_CHANNEL_CATEGORY_ID = REMOVED
DEFAULT_VOICE_CHANNEL_ID = REMOVED
```

2. Run script as follows:
  ```
  python3.6 /path/to/script/botinvex.py &
  ```
  
  or from inside a screen:
  ```
  screen -S discordBotInvex -d -m python3.6 /path/to/script/botinvex.py &
  ```


License
-----
All Rights Reserved.
