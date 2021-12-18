import random
import numpy as np
from typing import Tuple, Optional

from logic.game_logic import GameLogic, SECOND_PLAYER_CODE, FIRST_PLAYER_CODE, EMPTY_CODE, EXIT_CODE, EXIT_SYMBOLS
from logic.game_objects import Board


def free_position(column: np.array) -> int:
    """
    find the first free position in column
    numeration from 1

    :param column: array slice
    :return:
            position index,
         -1 - if the whole column is free,
         0 - if the column has no free place
    """
    if np.all(column == 0):  # if the whole column is free
        return -1
    return np.argmax(column > 0)  # first empty position (numeration from 1) in column or 0


class Player:
    def __init__(self, name: str, color: str = "white"):
        self.name = name
        self.color = color

    def make_move(self, board: Board) -> Tuple[int, int]:
        pass


class Human(Player):
    def make_move(self, board) -> Tuple[int, int]:
        """
        human player move, player chooses just column number

        :param board: game board
        :return: chosen position, (EXIT_CODE, EXIT_CODE) or (-1, -1) - wrong move
        """
        try:
            input_str = input("Enter column number: ")
            column_number = int(input_str) - 1
            column = board.field[:, column_number]  # get the column
        except (ValueError, IndexError) as e:
            if input_str.lower() in EXIT_SYMBOLS:
                return EXIT_CODE, EXIT_CODE
            print(e)
            return -1, -1  # wrong input - wrong move
        position = free_position(column)
        if position >= 0:
            row_number = position - 1
        else:
            row_number = board.height - 1  # the lower location

        return row_number, column_number


class AI(Player):
    def __init__(self, game_logic: GameLogic):
        """
        AI name = "AI",
        AI color = "red"

        :param game_logic: AI needs game logic to check win
        """
        name = "AI"
        color = "red"
        super().__init__(name, color)
        self.game_logic = game_logic

    def make_move(self, board: Board) -> Tuple[int, int]:
        """
        AI try to make win move,
        then try to prevent the enemy win,
        and then make <super_secret_logic> move

        :param board: game board
        :return: location for the new piece
        """
        input("press enter...")  # for delay
        return (
                self.winning_move(board) or
                self.blocking_move(board) or
                self.random_move(board)
        )

    def winning_move(self, board: Board) -> Optional[Tuple[int, int]]:
        """
        try to do winning move

        :param board: game board
        :return: winning position if exist
        """
        return self._common_move(board, code=SECOND_PLAYER_CODE)

    def blocking_move(self, board: Board) -> Optional[Tuple[int, int]]:
        """
        try to do blocking move

        :param board: game board
        :return: blocking enemy winning position if exist
        """
        return self._common_move(board, code=FIRST_PLAYER_CODE)

    def random_move(self, board: Board) -> Tuple[int, int]:
        """
        <super_secret_logic>

        :param board: game board
        :return: position by AI logic
        """
        row_number = -1
        while row_number < 0:
            column_number = random.randint(0, board.length - 1)
            column = board.field[:, column_number]  # get the column
            position = free_position(column)
            if position >= 0:
                row_number = position - 1
            else:
                row_number = board.height - 1  # the lower location

        return row_number, column_number

    def _common_move(self, board: Board, code: int = SECOND_PLAYER_CODE) -> Optional[Tuple[int, int]]:
        """
        difference between winning_move and blocking_move is just
        which player code is a winner

        :param board: game board
        :param code: AI/not_AI _CODE
        :return: winning position
        """
        for column_number, column in enumerate(board.field.T):  # iterate by columns
            position = free_position(column)
            if position >= 0:
                row_number = position - 1
            else:
                row_number = board.height - 1  # the lower location
            if row_number < 0:
                continue

            board.place_piece(code, (row_number, column_number))
            if self.game_logic.win_situation(board):
                # we shouldn't place the piece, just return location
                board.place_piece(EMPTY_CODE, (row_number, column_number))
                return row_number, column_number
            board.place_piece(EMPTY_CODE, (row_number, column_number))
        return None
