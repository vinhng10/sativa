import sqlite3
from pathlib import Path
from typing import Union

AnyPath = Union[Path, str, bytes]


def save_to_db(db: AnyPath, table: str, *args) -> None:
    """
    Save data to database.

    Parameters
    ----------
    db: AnyPath
        Path to sqlite database.
    table: str
        Name of table to save data to.
    args:
        Positional arguments.

    Returns
    -------
    None

    """
    connection = sqlite3.connect(db)

    try:
        cursor = connection.cursor()
        values = ','.join([f'\'{arg}\'' for arg in args])
        sql = f"INSERT INTO {table} VALUES ({values})"
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)
        connection.rollback()

    connection.close()
