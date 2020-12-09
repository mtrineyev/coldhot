# ColdHot Telegram bot game
"Guess the Number" telegram game by Cold-Hot method ❄️☀️ by @mtrineyev

Live bot @ColdHotGameBot

## Deployment and running
```
cd <install directory>
git clone git@github.com:mtrineyev/coldhot.git
cd coldhot
echo token=\'your_bot_token_here\' > ./modules/prod.py
python3 app.py
```

Application uses `requests`, `random` and `sqlite3`  Python3 modules

Users database will be auto created in the `bot/modules` directory

Have a nice game :)