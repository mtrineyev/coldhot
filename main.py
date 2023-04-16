"""
Main application for Telegram game bot ColdHotGame

ColdHotGame bot v3.0 (c) 2020-2023 Maksym Trineiev
mtrineyev@gmail.com
"""

import logging
from src.bot import bot


def main():
    logging.info("Bot started and waiting for users input...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
