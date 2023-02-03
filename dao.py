import sqlite3


def get_connection():
    connection = sqlite3.connect('wirkaufendeinauto.sqlite')
    return connection