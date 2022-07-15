import sqlite3
from os.path import exists
from sqlite3 import Connection

from utils.logger import logger


def create_connection(sqlite_file: str) -> Connection:
    if exists(sqlite_file):
        conn = sqlite3.connect(sqlite_file)
        logger.info(
            f"Successfully connected to sqlite database located at {sqlite_file}"
        )
        return conn
    else:
        logger.error(f"Sqlite database at location {sqlite_file} does not exist")
        raise FileNotFoundError(
            f"Sqlite database at location {sqlite_file} does not exist"
        )
