"""
Class for working with sqlite3 database

Database is stored in the same with the script directory

Methods:
    exec(self, sql: str, args=tuple()) -> bool
        Executes sql and returns successed
    fetch(self, sql: str, args=tuple()) -> list
        Executes sql and returns result row or None if err
    close(self) -> None
        Closes connection to database

ColdHotGame bot v1.1 (c) 2020 Maksym Trineyev
mtrineyev@gmail.com
"""

from os import path
import sqlite3


class SQLite3(object):
    def __init__(self, database_name, init_sql) -> None:
        self.name = f'{path.dirname(__file__)}/{database_name}'
        try:
            self.conn = sqlite3.connect(self.name)
        except sqlite3.Error as e:
            print(e)
        self.cursor = self.conn.cursor()
        try:
            self.exec(init_sql)
        except sqlite3.Error as e:
            print(e)
        print(f'Connected to [{self.name}] database v{sqlite3.version}')


    def exec(self, sql: str, args=tuple()) -> bool:
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return True
        except sqlite3.Error:
            self.conn.rollback()
            return False


    def fetch(self, sql: str, args=tuple()) -> list:
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchall()
        except sqlite3.Error:
            return None


    def close(self) -> None:
        self.conn.close()
        print(f'Disconnected from [{self.name}] database')


if __name__ == '__main__':
    print(__doc__)
