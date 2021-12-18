import numpy as np
from typing import Tuple


class Board:
    def __init__(self, length: int = 7, height: int = 6):
        self.length: int = length
        self.height: int = height
        self.field: np.array = np.zeros((height, length), dtype='int')

    def place_piece(self, code: int, location: Tuple[int, int]) -> None:
        self.field[location] = code

    def is_full(self) -> bool:
        """
        :return: if game board is full
        """
        return not np.any(self.field == 0)

    def clear(self) -> None:
        """
        reset game board
        """
        self.field = np.zeros((self.height, self.length), dtype='int')
