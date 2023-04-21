"""
Bots Player and Players classes

Player attributes:
    name: str,
    # Active game status
    start_time: int
    hard_mode: bool
    guess_number: int
    steps_count: int
    # Player statistics
    games_played: int
    best_time: int
    best_steps: int
    hard_games_played: int
    hard_best_time: int
    hard_best_steps: int

Player methods:
    init_game(number: int, time: int, hard_mode: bool)
    increase_games_count()
    is_game_started() -> bool
    reset_game()
    set_best_time(time: int) -> bool
    set_best_steps(steps: int) -> bool
    was_games_played() -> bool


Players methods:
    add_new_player(id: int, name: str) -> None
    get_top3_steps() -> [(name, steps)...]
    get_top3_time() -> [(name, time)...]
    get_top3_hard_steps() -> [(name, steps)...]
    get_top3_hard_time() -> [(name, time)...]
    is_exist(id: int) -> bool
    is_game_started(id: int) -> bool
    load(),
    save()
    was_games_played(id: int) -> bool

ColdHotGame bot v3.0 (c) 2020-2023 Maksym Trineiev
mtrineyev@gmail.com
"""

import json
import logging
import pickle

from settings import PLAYERS_FILE_NAME

_INFINITY = 9223372036854775807


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.number_to_guess = 0
        self.start_time = 0
        self.hard_mode = False
        self.steps_count = 0
        self.games_played = 0
        self.best_time = _INFINITY
        self.best_steps = _INFINITY
        self.games_played_hard = 0
        self.best_time_hard = _INFINITY
        self.best_steps_hard = _INFINITY

    def __str__(self) -> str:
        return json.dumps(self.__dict__, indent=2, ensure_ascii=False)

    def init_game(self, number: int, time: int, hard_mode: bool) -> None:
        self.number_to_guess = number
        self.start_time = time
        self.hard_mode = hard_mode
        self.steps_count = 0

    def reset_game(self) -> None:
        self.init_game(0, 0, False)

    def is_game_started(self) -> bool:
        return bool(self.number_to_guess)

    def set_best_time(self, time: int) -> bool:
        if self.hard_mode:
            if time < self.best_time_hard:
                self.best_time_hard = time
                return True
            return False
        if time < self.best_time:
            self.best_time = time
            return True
        return False

    def set_best_steps(self, steps: int) -> bool:
        if self.hard_mode:
            if steps < self.best_steps_hard:
                self.best_steps_hard = steps
                return True
            return False
        if steps < self.best_steps:
            self.best_steps = steps
            return True
        return False

    def increase_games_count(self) -> None:
        if self.hard_mode:
            self.games_played_hard += 1
        else:
            self.games_played += 1

    def was_games_played(self) -> bool:
        return bool(self.games_played or self.games_played_hard)


class Players:
    class _Encoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

    def __init__(self) -> None:
        self._players = dict()

    def __iter__(self):
        return iter(self._players)

    def __getitem__(self, key):
        return self._players[key]

    def __len__(self) -> int:
        return len(self._players)

    def __str__(self) -> str:
        return json.dumps(
            self._players, indent=2, ensure_ascii=False, cls=self._Encoder)

    def add_new(self, pid: int, name: str) -> None:
        if self.is_exist(pid):
            raise KeyError(f"Player {pid=} already in the database")
        self._players[pid] = Player(name)

    def get_top3_steps(self) -> list:
        top = sorted(
            [(v.name, v.best_steps) for v in self._players.values()
             if v.best_steps != _INFINITY],
            key=lambda x: x[1]
        )
        return top[:3]

    def get_top3_time(self) -> list:
        top = sorted(
            [(v.name, v.best_time) for v in self._players.values()
             if v.best_time != _INFINITY],
            key=lambda x: x[1]
        )
        return top[:3]

    def get_top3_hard_steps(self) -> list:
        top = sorted(
            [(v.name, v.best_steps_hard) for v in self._players.values()
             if v.best_steps_hard != _INFINITY],
            key=lambda x: x[1]
        )
        return top[:3]

    def get_top3_hard_time(self) -> list:
        top = sorted(
            [(v.name, v.best_time_hard) for v in self._players.values()
             if v.best_time_hard != _INFINITY],
            key=lambda x: x[1]
        )
        return top[:3]

    def is_exist(self, pid: int) -> bool:
        return pid in self._players

    def is_game_started(self, pid: int) -> bool:
        if self.is_exist(pid):
            return self._players[pid].is_game_started()
        return False

    def was_games_played(self, pid: int) -> bool:
        if self.is_exist(pid):
            return self._players[pid].was_games_played()
        return False

    def load(self) -> None:
        try:
            with open(PLAYERS_FILE_NAME, "rb") as bf:
                self._players = pickle.load(bf)
        except (
                FileNotFoundError, PermissionError,
                OSError, ModuleNotFoundError,
        ) as e:
            logging.warning(
                f"{PLAYERS_FILE_NAME=} reading error {e}. "
                "Used empty dictionary."
            )

    def save(self) -> None:
        try:
            with open(PLAYERS_FILE_NAME, "wb") as bf:
                pickle.dump(self._players, bf)
        except (IOError, OSError):
            logging.error(f"{PLAYERS_FILE_NAME=} writing error")


if __name__ == '__main__':
    print(__doc__)
