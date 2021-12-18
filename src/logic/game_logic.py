from typing import Tuple
import numpy as np
from logic.game_objects import Board

EMPTY_CODE = 0
FIRST_PLAYER_CODE = 1
SECOND_PLAYER_CODE = 2  # AI is always the second player
EXIT_CODE = -2  #
EXIT_SYMBOLS = ["x", "q"]


class GameLogic:
    def __init__(self, win_count=4):
        self.win_count = win_count

    def is_legal(self, location: Tuple[int, int], board: Board) -> bool:
        """
        :param location: position for piece
        :param board: game board
        :return: if placing in this location is by rules
        """
        return (
                0 <= location[0] < board.height and
                0 <= location[1] < board.length and
                board.field[location] == EMPTY_CODE
        )

    def win_situation(self, board: Board) -> bool:
        """
        :param board: game board
        :return: if the board has win situation
        """
        # iterate by rows and then by columns
        for matrix in [board.field, board.field.T]:
            for row in matrix:
                if self._check_win_row(row):
                    return True

        for matrix in [board.field, np.flipud(board.field)]:
            f = (-matrix.shape[0] + self.win_count,  # (6,7)
                matrix.shape[1] - self.win_count + 1)
            for offset in range(*f):
                if self._check_win_row(matrix.diagonal(offset=offset)):
                    return True

        # # Check horizontal locations for win
        # for c in range(board.length - 3):
        #     for r in range(board.height):
        #         for i in range(1, 3):
        #             if board.field[r][c] == i and board.field[r][c + 1] == i and board.field[r][c + 2] == i and \
        #                     board.field[r][c + 3] == i:
        #                 return True
        #
        # # Check vertical locations for win
        # for c in range(board.length):
        #     for r in range(board.height - 3):
        #         for i in range(1, 3):
        #             if board.field[r][c] == i and board.field[r + 1][c] == i and board.field[r + 2][c] == i and \
        #                     board.field[r + 3][c] == i:
        #                 return True
        #
        # # Check positively sloped diagonals
        # for c in range(board.length - 3):
        #     for r in range(board.height - 3):
        #         for i in range(1, 3):
        #             if board.field[r][c] == i and board.field[r + 1][c + 1] == i and board.field[r + 2][c + 2] == i \
        #                     and board.field[r + 3][c + 3] == i:
        #                 return True
        #
        # # Check negatively sloped diagonals
        # for c in range(board.length - 3):
        #     for r in range(3, board.height):
        #         for i in range(1, 3):
        #             if board.field[r][c] == i and board.field[r - 1][c + 1] == i and board.field[r - 2][c + 2] == i \
        #                     and board.field[r - 3][c + 3] == i:
        #                 return True

        return False

    def board_full(self, board: Board) -> bool:
        return board.is_full()

    def _check_win_row(self, row):
        count_in_row = 0
        previous = 0
        for item in row:
            if item:
                if item == previous:
                    count_in_row += 1
                else:
                    count_in_row = 1
            else:
                count_in_row = 0
            previous = item

            if count_in_row >= self.win_count:
                return True
