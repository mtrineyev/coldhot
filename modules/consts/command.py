"""
This module contains list of the commands for ColdHotGame bot

Constants:
    hardmode - list of commands for start hardmode game
    start - list of commands for start game
    helping - list of commands for help
    leaders - list of commands for show leaders
    stats - list of commands for show stats
    stop  - list of commands for stop game

ColdHotGame bot v1.1 (c) 2020 Maksym Trineyev
mtrineyev@gmail.com
"""


hardmode = ('hardmode', 'hardcore', 'жги!')
start = ('start', 'старт', 'please',
    'будь ласка', 'калі ласка', 'пожалуйста') + hardmode
helping = ('help', 'допомога', 'помощь')
leaders = ('leaders', 'лідери', 'лидеры')
stats = ('stats', 'статистика', 'як мої справи?')
stop = ('stop', 'стоп')


if __name__ == "__main__":
    print(__doc__)
