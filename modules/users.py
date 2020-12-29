"""
Class for working with bots users stored in SQLite database

Values:
    id,
    nick,
    name,
    game_started,
    hard_mode,
    guess_number,
    start_time,
    tries_count,
    games_played,
    hard_games_played,
    best_time,
    hard_best_time,
    best_steps,
    hard_best_steps

Methods:
    create() -> bool,
    exist() -> bool,
    exit(),
    get_top3_steps() -> list,
    get_top3_time() -> list,
    get_top3_hard_steps() -> list,
    get_top3_hard_time() -> list,
    read() -> bool,
    save() -> bool

ColdHotGame bot v1.1 (c) 2020 Maksym Trineyev
mtrineyev@gmail.com
"""

from database import SQLite3


class Users(object):
    """Class for working with bots users stored in SQLite database"""

    max_int = 9223372036854775807

    def _set_init_values(self) -> None:
        self.game_started = 0
        self.hard_mode = 0
        self.guess_number = 0
        self.start_time = 0
        self.tries_count = 0
        self.games_played = 0
        self.hard_games_played = 0
        self.best_time = self.max_int
        self.hard_best_time = self.max_int
        self.best_steps = self.max_int
        self.hard_best_steps = self.max_int

    def __init__(self, source: str) -> None:
        sql = f"""
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER NOT NULL PRIMARY KEY,
            nick TEXT,
            name TEXT,
            game_started INTEGER DEFAULT 0,
            hard_mode INTEGER DEFAULT 0,
            guess_number INTEGER DEFAULT 0,
            start_time INTEGER DEFAULT 0,
            tries_count INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0,
            hard_games_played INTEGER DEFAULT 0,
            best_time INTEGER DEFAULT {self.max_int},
            hard_best_time INTEGER DEFAULT {self.max_int},
            best_steps INTEGER DEFAULT {self.max_int},
            hard_best_steps INTEGER DEFAULT {self.max_int}
        )"""
        self._db = SQLite3(source, sql)
        self.id = ''
        self.nick = ''
        self.name = ''
        self._set_init_values()


    def __str__(self) -> str:
        result = '{ ' + ', '.join((
            f'id: {self.id}',
            f'nick: {self.nick or "-"}',
            f'name: {self.name}',
            f'\ngame started: {self.game_started}',
            f'hardcore: {self.hard_mode}',
            f'guess: {self.guess_number}',
            f'time: {self.start_time}',
            f'steps: {self.tries_count}',
            f'\ngames played: {self.games_played}',
            f'best time: {self.best_time}',
            f'best steps: {self.best_steps}',
            f'\nhard games played: {self.hard_games_played}',
            f'hard best time: {self.hard_best_time}',
            f'hard best steps: {self.hard_best_steps}'
        )) + ' }'
        return result


    def create(self) -> bool:
        sql = """
            INSERT INTO Users (id, nick, name)
            VALUES (?, ?, ?)
        """
        values = (self.id, self.nick, self.name)
        self._set_init_values()
        return self._db.exec(sql, values)


    def exist(self) -> bool:
        sql = """
            SELECT id
            FROM Users
            WHERE id = ?
        """
        row = self._db.fetch(sql, (self.id,))
        if row:
            return True
        else:
            return False


    def get_top3_steps(self) -> list:
        sql = """
            SELECT nick, name, best_steps
            FROM Users
            ORDER BY best_steps LIMIT 3
        """
        return self._db.fetch(sql)


    def get_top3_time(self) -> list:
        sql = """
            SELECT nick, name, best_time
            FROM Users
            ORDER BY best_time LIMIT 3
        """
        return self._db.fetch(sql)


    def get_top3_hard_steps(self) -> list:
        sql = """
            SELECT nick, name, hard_best_steps
            FROM Users
            ORDER BY hard_best_steps LIMIT 3
        """
        return self._db.fetch(sql)


    def get_top3_hard_time(self) -> list:
        sql = """
            SELECT nick, name, hard_best_time
            FROM Users
            ORDER BY hard_best_time LIMIT 3
        """
        return self._db.fetch(sql)


    def read(self) -> bool:
        sql = """
            SELECT *
            FROM Users
            WHERE id = ?
        """
        row = self._db.fetch(sql, (self.id,))
        if row:
            # skip id, nick and name leave them from bot update
            # self.id, self.nick, self.name,
            (self.game_started,
            self.hard_mode, self.guess_number, self.start_time,
            self.tries_count, self.games_played, self.hard_games_played,
            self.best_time, self.hard_best_time, self.best_steps,
            self.hard_best_steps) = row[0][3:]
            return True
        else:
            return False


    def save(self) -> bool:
        sql = """
            UPDATE Users
            SET nick = ?,
                name = ?,
                game_started = ?,
                hard_mode = ?,
                guess_number = ?,
                start_time = ?,
                tries_count = ?,
                games_played = ?,
                hard_games_played = ?,
                best_time = ?,
                hard_best_time = ?,
                best_steps = ?,
                hard_best_steps = ?
            WHERE id = ?
        """
        values = (self.nick, self.name, self.game_started,
            self.hard_mode, self.guess_number, self.start_time,
            self.tries_count, self.games_played, self.hard_games_played,
            self.best_time, self.hard_best_time, self.best_steps,
            self.hard_best_steps, self.id)
        return self._db.exec(sql, values)


    def exit(self) -> None:
        self.save()
        self._db.close()


if __name__ == '__main__':
    print(__doc__)
