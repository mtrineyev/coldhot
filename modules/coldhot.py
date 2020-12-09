"""
Game logic for Telegram bot

Class:
    ColdHotGame

Method:

    listen(self) -> None:
        Receives updates from the bot and acts

ColdHotGame bot v1.1 (c) 2020 Maksym Trineyev
mtrineyev@gmail.com
"""

import random

import config
import consts.command as commands
import consts.msg as msg
import telega as tg
from users import Users


class ColdHotGame(object):
    """
    Game 'Guess the number'

    The bot guesses number from 1 to config.MAX_NUMBER.
    The user guesses the number by getting hints from the bot.
    """
    def __init__(self):
        self.last_update_id = 0
        self.user_input = ''
        self.update_time = 0
        self.user = Users(config.DB_NAME)


    def __enter__(self):
        print('Bot started and waiting for user input...')
        return self


    def __exit__(self, type, value, tb):
        self.user.exit()
        print('Bot stopped')


    def _distanse(self, a: int, b: int, hard=False) -> str:
        """Returns word expression of distanse"""
        d = abs(a - b)
        if d >= 999000: index = 13
        elif d >= 5000: index = 0
        elif d >= 2000: index = 1
        elif d >= 600: index = 2
        elif d >= 400: index = 3
        elif d >= 300: index = 4
        elif d >= 200: index = 5
        elif d >= 100: index = 6
        elif d >= 50: index = 7
        elif d >= 25: index = 8
        elif d >= 12: index = 9
        elif d >= 6: index = 10
        elif d >= 2: index = 11
        else: index = 12
        # last symbol if hard otherwise full string
        return msg.hints[index][-hard:]

    
    def _plural(self, amount: int, plurals: tuple) -> str:
        """Returns corresponding plural from the tuple to 1, 2, 5 principal"""
        if amount == 0: return ''
        mod = amount % 100
        if mod > 20: mod %= 10
        if mod == 1:
            return f'{amount} {plurals[0]}'
        elif mod in (2, 3, 4):
            return f'{amount} {plurals[1]}'
        else:
            return f'{amount} {plurals[2]}'


    def _plural_time(self, elapsed: int, plurals=()) -> str:
        """Converts seconds to the string from hours, minutes and seconds"""
        m, s = divmod(elapsed, 60)
        h, m = divmod(m, 60)
        result = self._plural(h, msg.hours) + ', '
        result += self._plural(m, msg.minutes) + ' та '
        result += self._plural(s, msg.seconds)
        result = result.strip(', ').strip(' та ')
        return result

    
    def _start_game(self) -> None:
        """Inits variables for starting game and logs a start game info"""
        self.user.game_started = True
        self.user.hard_mode = self.user_input in commands.hardmode
        self.user.guess_number = random.randint(1, config.MAX_NUMBER)
        self.user.start_time = self.update_time
        self.user.tries_count = 0
        print(self.user)
        message = msg.start_game.format(config.MAX_NUMBER)
        tg.send_message(self.user.id, message)
        self.user.save()


    def _make_move(self) -> None:
        """Analizes ingame input from user and acts"""
        self.user.tries_count += 1
        self.user.save()
        try:
            user_guess = int(self.user_input)
        except ValueError:
            tg.send_message(self.user.id, random.choice(msg.errors))
            return
        
        if user_guess != self.user.guess_number:
            message = self._distanse(
                user_guess, self.user.guess_number, self.user.hard_mode)
        else:
            message = self._finish_game()
        tg.send_message(self.user.id, message)


    def _finish_game(self) -> str:
        """Ends game, saves stats and returns formatted ending message"""
        self.user.game_started = False
        elapsed_time = self.update_time - self.user.start_time
        message = msg.end_game.format(
            self._plural(self.user.tries_count, msg.tries),
            self._plural_time(elapsed_time))
        tries_count = self.user.tries_count
        congrat = ''
        if self.user.hard_mode:
            self.user.hard_games_played += 1
            if elapsed_time < self.user.hard_best_time:
                congrat += msg.record_hard_time
                self.user.hard_best_time = elapsed_time
            if tries_count < self.user.hard_best_steps:
                congrat += msg.record_hard_steps
                self.user.hard_best_steps = tries_count
        else:
            self.user.games_played += 1
            if elapsed_time < self.user.best_time:
                congrat += msg.record_time
                self.user.best_time = elapsed_time
            if tries_count < self.user.best_steps:
                congrat += msg.record_steps
                self.user.best_steps = tries_count
        print(f'{self.user.name} guessed the number')
        if congrat:
            message += msg.exclamation + congrat + msg.record_footer
        self.user.save()
        return message


    def _stop_game(self) -> None:
        """Stops current game without saving stats"""
        if self.user.game_started:
            tg.send_message(self.user.id, msg.break_game)
            self.user.game_started = False
            self.user.save()
        else:
            tg.send_message(self.user.id, msg.no_game_started)


    def _help(self) -> None:
        """Sends appropriate help message"""
        if self.user.game_started:
            tg.send_message(self.user.id, msg.ingame_help)
        else:
            tg.send_message(self.user.id, msg.command_help)


    def _leaders(self) -> None:
        """Shows TOP-3 leaderboard"""
        def _leaders_list(rows: list, func, plurals=()) -> str:
            result = ''
            for i, (nick, name, value) in enumerate(rows):
                user = f'@{nick}' if nick else name
                result += f'{msg.medals[i]} {user} {func(value, plurals)}\n'
            return result

        norm_steps = self.user.get_top3_steps()
        norm_times = self.user.get_top3_time()
        hard_steps = self.user.get_top3_hard_steps()
        hard_times = self.user.get_top3_hard_time()
        message = msg.leaders_title.format(
            _leaders_list(norm_steps, self._plural, msg.tries),
            _leaders_list(norm_times, self._plural_time),
            _leaders_list(hard_steps, self._plural, msg.tries),
            _leaders_list(hard_times, self._plural_time))
        tg.send_message(self.user.id, message, parse_mode='html')


    def _stats(self) -> None:
        """Shows current user stats"""
        if self.user.games_played or self.user.hard_games_played:
            message = msg.stats_title
            if self.user.games_played:
                message += msg.stats_normal.format(
                    self._plural(self.user.games_played, msg.games),
                    self._plural_time(self.user.best_time),
                    self._plural(self.user.best_steps, msg.tries))
            if self.user.hard_games_played:
                message += msg.stats_hard.format(
                    self._plural(self.user.hard_games_played, msg.games),
                    self._plural_time(self.user.hard_best_time),
                    self._plural(self.user.hard_best_steps, msg.tries))
        else:
            message = msg.stats_nogames
        tg.send_message(self.user.id, message)


    def _get_update_info(self, update: dict) -> None:
        """Saves received update info to the class variables"""
        self.last_update_id = update['update_id']
        self.user.id = update['message']['chat']['id']
        if 'username' in update['message']['from']:
            self.user.nick = update['message']['from']['username']
        else:
            self.user.nick = ''
        if 'first_name' in update['message']['from']:
            self.user.name = update['message']['from']['first_name']
        else:
            self.user.name = ''
        self.update_time = update['message']['date']
    
    
    def _proceed_text(self) -> None:
        """Analizes text command from user and acts"""
        if self.user_input in commands.helping:
            self._help()
        elif self.user_input in commands.leaders:
            self._leaders()
        elif self.user_input in commands.stats:
            self._stats()
        elif self.user_input in commands.stop:
            self._stop_game()
        elif self.user.game_started:
            self._make_move()
        elif self.user_input in commands.start:
            self._start_game()
        else:
            tg.send_message(self.user.id, random.choice(msg.relpies))
            

    def _idle(self) -> None:
        """Reacts to non text event"""
        tg.send_message(self.user.id, msg.sticker_reply)


    def listen(self) -> None:
        """Receives updates from the bot and acts"""
        data = tg.get_updates(self.last_update_id + 1)
        
        for update in data['result']:
            self._get_update_info(update)

            if not self.user.read():
                self.user.create()
                message = msg.hello.format(self.user.name)
                tg.send_message(self.user.id, message)
            
            if 'text' in update['message']:
                self.user_input = update['message']['text']\
                    .lower().strip('/')
                print(self.user.name, '->', self.user_input)
                self._proceed_text()
            else:
                self._idle()


if __name__ == '__main__':
    print(__doc__)