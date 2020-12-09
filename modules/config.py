"""
Settings for Telegram bot

Constants:

    DB_NAME - name of the file with sqlite3 database
    MAX_NUMBER - upper limit for guessed number
    TOKEN - bot token
    TG_API - Telegram API url adress

ColdHotGame bot v1.1 (c) 2020 Maksym Trineyev
mtrineyev@gmail.com
"""

tg_setname = """
❄️☀️ColdHotGame
"""

tg_setabouttext = """
Гра "Вгадай Число" 🤔 методом "Холодно-Спекотно" ❄️☀️
автор @mtrineyev
"""

tg_setdescription = """
🤖 загадає ціле число від 1 до 1000, яке треба вгадати якнайшвидше, використовуючи підказки 💪 Це може бути не так і просто, як може здатися спочатку 🤨 Наважишся ⁉️ Тоді тисни "Старт" і почнемо гру 🏁
"""

tg_setcommands = """
start - Почати гру
help - Допомога
hardcore - Складний режим
leaders - Лідери
stats - Моя статистика
stop - Припинити гру
"""

import prod

TOKEN = prod.token
# @ColdHotGameBot


TG_API = f'https://api.telegram.org/bot{TOKEN}'
# Telegram API url adress


DB_NAME = 'coldhot.db'
# name of the file with sqlite3 database


MAX_NUMBER = 1000
# upper limit for guessed number


if __name__ == "__main__":
    print(__doc__)