import sqlite3
import subprocess
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import List, Union

AnyPath = Union[Path, str, bytes]
RETRY = 3

class Tool(Enum):
    SWIFT = "swift"
    S3CMD = "s3cmd"
    RCLONE = "rclone"


def retry(f):
    """
    Retry a function for a fixed amount of time if failed.

    Parameters
    ----------
    f:
        Function to retry if failed.

    Returns
    -------
    decorated:
        Decorated function.

    """
    @wraps(f)
    def decorated(*args, **kwargs):
        for _ in range(RETRY):
            try:
                result = f(*args, **kwargs)
                return result
            except Exception as e:
                print(e)
                print("Retrying ...")
        print(f"Retried {RETRY} times but all failed.")
    return decorated


def save_to_db(db: AnyPath, table: str, *args) -> bool:
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


def split_file(file: AnyPath, file_split_size: int = 0, suffix_length: int = 4) -> List[Path]:
    """
    Split a file into smaller files. All the split files will locate in dedicated
    folder to separate from other splits (from other experiments).

    The name format of dedicated folder:
        <file_name>-<file_extension>-<file_split_size>G-splits

    The name format of split file:
        <file_name>-<file_extension>-<file_split_size>G-<number>

    Parameters
    ----------
    file: AnyPath
        Path to the file to be split.
    file_split_size: int
        Size of a split file. Measured in Gigabyte.
    suffix_length: int
        Length of suffix for split files.

    Returns
    -------
    split_files: List[Path]
        List of path to split files.

    """
    if not isinstance(file_split_size, int):
        raise TypeError(f"Non-negataive integer file_split_size expected, but got {type(file_split_size)} instead.")
    if not isinstance(suffix_length, int):
        raise TypeError(f"Positive integer suffix_length expected, but got {type(suffix_length)} instead.")
    if suffix_length < 0:
        raise ValueError(f"Positive integer suffix_length expected, but got {suffix_length} instead.")

    file = Path(file)
    prefix = f"{file.name.replace('.', '-')}-{file_split_size}G-"

    # Create directory to store split files. This is for easy management:
    parent_folder = file.parent / (prefix + "splits")
    parent_folder.mkdir(parents=True, exist_ok=True)

    if file_split_size > 0:
        # Call linux "split" to split the file. This is for convenience and reliability.
        # Might need check for performance compared to native python code in different settings:
        cmd = f"split -d -a {suffix_length} -b {file_split_size}GB " \
              f"{file.as_posix()} {parent_folder / prefix}"
        p = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            check=True
        )
    else:
        # If file_split_size is 0, then don't split the file, only move to new directory:
        file.rename(parent_folder / (prefix + "0"*suffix_length))

    # Glob all paths to split files:
    split_files = list(parent_folder.glob(f"*{prefix}*"))

    return split_files




