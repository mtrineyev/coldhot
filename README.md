# ColdHot Telegram bot game v3.0
"Guess the Number" telegram game by Cold-Hot method ❄️☀️ by @mtrineyev

Telegram bot https://t.me/ColdHotGameBot

## Deployment and running on Linux
Installation and running process:
```bash
cd install_directory
git clone git@github.com:mtrineyev/coldhot.git
cd coldhot
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp settings.example settings.py
nano settings.py
python main.py
```
You can also start the bot in background:
```bash
nohup python main.py > /dev/null 2>&1&
```
You can find the process and its process ID with this command:
```bash
ps ax | grep main.py
```
If you want to stop the execution, you can kill it with the kill command:
```bash
kill PID
```

Application uses `pyTelegramBotAPI` Python module

Have a nice game :)
