"""
Contains utilities for ColdHotGame bot

get_hit_index(guess: int, goal: int) - returns index of the hit
get_plural_word() - for the number returns corresponding plural word from list
seconds_to_ua() - for the seconds returns string in Ukrainian

ColdHotGame bot v3.0 (c) 2020-2023 Maksym Trineiev
mtrineyev@gmail.com
"""

from settings import MAX_GUESS_NUMBER

HOURS = ("година", "години", "годин")
MINUTES = ("хвилина", "хвилини", "хвилин")
SECONDS = ("секунда", "секунди", "секунд")
STEPS = ("хід", "ходи", "ходів")
GAMES = ("гру", "гри", "ігор")


def get_hit_index(guess: int, goal: int) -> int:
    distance = abs(guess - goal)
    percent = distance / MAX_GUESS_NUMBER
    if abs(guess) >= MAX_GUESS_NUMBER * 5:
        index = 0
    elif guess > MAX_GUESS_NUMBER or guess <= 0:
        index = 1
    elif percent >= 0.9:
        index = 2
    elif percent >= 0.6:
        index = 3
    elif percent >= 0.4:
        index = 4
    elif percent >= 0.3:
        index = 5
    elif percent >= 0.2:
        index = 6
    elif distance >= MAX_GUESS_NUMBER * 0.1:
        index = 7
    elif distance >= 50:
        index = 8
    elif distance >= 25:
        index = 9
    elif distance >= 12:
        index = 10
    elif distance >= 6:
        index = 11
    elif distance >= 2:
        index = 12
    else:
        index = 13
    return index


def get_plural_word(number: int, plurals: tuple) -> str:
    if number == 0:
        return ""
    modulus = number % 100
    if modulus > 20:
        modulus %= 10
    if modulus == 1:
        return f"{number} {plurals[0]}"
    elif modulus in (2, 3, 4):
        return f"{number} {plurals[1]}"
    else:
        return f"{number} {plurals[2]}"


def seconds_to_ua(seconds: int, plural=()) -> str:
    assert plural == ()
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return " ".join(
        [w for w in (
            get_plural_word(h, HOURS),
            get_plural_word(m, MINUTES),
            get_plural_word(s, SECONDS)
        ) if w]
    )


def escape_markdown(text: str) -> str:
    return (text
            .replace("_", "\\_")
            .replace("*", "\\*")
            .replace("[", "\\[")
            .replace("]", "\\]")
            .replace("(", "\\(")
            .replace(")", "\\)")
            .replace("~", "\\~")
            .replace("`", "\\`")
            .replace(">", "\\>")
            .replace("#", "\\#")
            .replace("+", "\\+")
            .replace("-", "\\-")
            .replace("=", "\\=")
            .replace("|", "\\|")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace(".", "\\.")
            .replace("!", "\\!")
            )


if __name__ == "__main__":
    print(__doc__)
