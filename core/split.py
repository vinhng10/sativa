
from enum import Enum, unique
from pathlib import Path
from typing import List


@unique
class Suffix(Enum):
    H5 = ".h5"


class FileSplitter():

    @staticmethod
    def split_h5(path, n_chunks: int) -> None:
        pass

    def __init__(self, path):
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, value) -> None:
        self._path = Path(value)

    def suffix(self) -> str:
        return self._path.suffix

    def split(self, n_chunks: int = 1) -> List:
        if n_chunks <= 0:
            raise ValueError("Number of chunks must be a postive "
                             "integer value")

        if self.suffix == Suffix.H5.value:
            self.split_h5(self.path, n_chunks=n_chunks)











