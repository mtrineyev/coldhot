"""
Methods for Telegram API:

    get_updates(offset: int) -> dict:
        Forms TG API getUpdates request with the given offset

    send_message(chat_id: int, text: str) -> str:
        Send text to chat_id and returns True if succes

(c) 2020 Maksym Trineyev
mtrineyev@gmail.com
"""


import requests

import config


def skip_connection_error(func):
    """To skip connection errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError:
            return False
    return wrapper


@skip_connection_error
def get_updates(offset: int) -> dict:
    """Forms TG API getUpdates request with the given offset"""
    result = requests.get(f'{config.TG_API}/getUpdates',
        params={'offset': offset}).json()
    return result


@skip_connection_error
def send_message(chat_id: int, text: str, parse_mode='markdown') -> str:
    """Send text to chat_id and returns True if succes"""
    result = requests.get(f'{config.TG_API}/sendMessage',
        params={'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        ).ok
    return result


if __name__ == '__main__':
    print(__doc__)
