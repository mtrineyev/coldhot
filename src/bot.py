"""
Game logic for 'Guess the number' for Telegram bot

The bot thinks number from 1 to settings.MAX_GUESS_NUMBER.
The user tries to guess the number by getting hints from the bot.

ColdHotGame bot v3.0 (c) 2020-2023 Maksym Trineiev
mtrineyev@gmail.com
"""

import logging
import random
import telebot

from settings import BOT_TOKEN, MAX_GUESS_NUMBER
from src.thesaurus.commands import LEADERS, HELP, STOP, STATS, HARD, START
from src.thesaurus.messages import (
    ABORT_GAME, END_GAME, ERRORS, EXCLAMATION, START_GAME_OTHER_CHAT,
    GAME_ALREADY_STARTED, HELLO, HELP_IN_GAME, HELP_OUT_GAME, HINTS,
    NO_GAME_STARTED, RECORD_HEADER, RECORD_TIME, RECORD_STEPS, GAME_TYPE,
    RECORD_FOOTER, REPLIES, START_GAME, STICKER_REPLY,
    STATS_TITLE, STATS_NO_GAMES, STATS_NORMAL, STATS_HARD, STATS_OTHER_CHAT,
    LEADERS_TABLE, MEDALS,
)
from src.players import Players
from src.utils import (
    get_hit_index, get_plural_word, seconds_to_ua,
    GAMES, STEPS,
)


bot = telebot.TeleBot(BOT_TOKEN, parse_mode="MarkdownV2")
players = Players()
players.load()


@bot.message_handler(commands=START+HARD)
def start_game(message) -> None:
    user = message.from_user
    last_name = f" {user.last_name}" if user.last_name else ""
    name = f"{user.first_name}{last_name}"
    if message.chat.id != user.id:
        bot.send_message(message.chat.id, START_GAME_OTHER_CHAT.format(name))
    if not players.is_exist(user.id):
        players.add_new(user.id, name)
        bot.send_message(user.id, HELLO.format(name))
        players.save()
    player = players[user.id]
    if player.is_game_started():
        bot.send_message(
            user.id, GAME_ALREADY_STARTED.format(
                seconds_to_ua(message.date - player.start_time)))
        return
    hard_mode = any([c in message.text for c in HARD])
    player.init_game(
        random.randint(1, MAX_GUESS_NUMBER), message.date, hard_mode)
    bot.send_message(user.id, START_GAME.format(MAX_GUESS_NUMBER))
    logging.info(
        "Game started "
        f"{player.name=}, {player.hard_mode=}, {player.number_to_guess=}")


@bot.message_handler(commands=STOP)
def stop_command(message) -> None:
    user = message.from_user
    if not players.is_game_started(user.id):
        bot.send_message(message.chat.id, NO_GAME_STARTED)
        return
    player = players[user.id]
    player.reset_game()
    bot.send_message(message.chat.id, ABORT_GAME)
    logging.info(f"Game aborted {player.name=}")


@bot.message_handler(commands=HELP)
def help_command(message) -> None:
    user = message.from_user
    if players.is_game_started(user.id):
        bot.send_message(message.chat.id, HELP_IN_GAME)
    else:
        bot.send_message(message.chat.id, HELP_OUT_GAME)


@bot.message_handler(commands=STATS)
def stats_command(message) -> None:
    user = message.from_user
    if user.id != message.chat.id:
        bot.send_message(
            message.chat.id,
            STATS_OTHER_CHAT.format(message.from_user.first_name))
    if players.was_games_played(user.id):
        player = players[user.id]
        stats = STATS_TITLE
        if player.games_played:
            stats += STATS_NORMAL.format(
                get_plural_word(player.games_played, GAMES),
                get_plural_word(player.best_steps, STEPS),
                seconds_to_ua(player.best_time))
        if player.games_played_hard:
            stats += STATS_HARD.format(
                get_plural_word(player.games_played_hard, GAMES),
                get_plural_word(player.best_steps_hard, STEPS),
                seconds_to_ua(player.best_time_hard))
    else:
        stats = STATS_NO_GAMES
    bot.send_message(user.id, stats)


@bot.message_handler(commands=LEADERS)
def leaders_command(message) -> None:
    def top3(rows: list, func, plurals=()) -> str:
        result = ""
        for i, (name, value) in enumerate(rows):
            result += f"{MEDALS[i]} {name} {func(value, plurals)}\n"
        return result

    bot.send_message(message.chat.id, LEADERS_TABLE.format(
        top3(players.get_top3_steps(), get_plural_word, STEPS),
        top3(players.get_top3_time(), seconds_to_ua),
        top3(players.get_top3_hard_steps(), get_plural_word, STEPS),
        top3(players.get_top3_hard_time(), seconds_to_ua)
    ))


@bot.message_handler(content_types=["text"])
def make_move(message):
    def record_message(record_type: str, mode: str) -> str:
        return " ".join([RECORD_HEADER, record_type, GAME_TYPE[mode]])

    user = message.from_user
    if players.is_game_started(user.id):
        player = players[user.id]
        player.steps_count += 1
        try:
            guess = int(message.text.lstrip("/"))
        except ValueError:
            bot.send_message(message.chat.id, random.choice(ERRORS))
            return
        if guess == player.number_to_guess:
            elapsed_time = message.date - player.start_time
            relpy = END_GAME.format(
                get_plural_word(player.steps_count, STEPS),
                seconds_to_ua(elapsed_time))
            record = ""
            if player.set_best_time(elapsed_time):
                record = record_message(RECORD_TIME, player.hard_mode)
            if player.set_best_steps(player.steps_count):
                record += record_message(RECORD_STEPS, player.hard_mode)
            player.increase_games_count()
            player.reset_game()
            players.save()
            if record:
                relpy += EXCLAMATION + record + RECORD_FOOTER
            logging.info(f"{player.name=} guessed the number, {elapsed_time=}")
        else:
            hint = HINTS[get_hit_index(guess, player.number_to_guess)]
            relpy = hint[-player.hard_mode:]  # last symbol if hard
    else:
        relpy = random.choice(REPLIES)
    bot.send_message(message.chat.id, relpy)


@bot.message_handler(content_types=[
    "audio", "document", "photo", "sticker",
    "video", "voice", "location", "contact"])
def message_reply(message):
    bot.send_message(message.from_user.id, STICKER_REPLY)


if __name__ == '__main__':
    print(__doc__)
