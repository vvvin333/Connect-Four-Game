from termcolor import cprint

from logic.game_logic import GameLogic, EMPTY_CODE, FIRST_PLAYER_CODE, SECOND_PLAYER_CODE, EXIT_CODE
from logic.game_objects import Board
from players.players import AI, Human, Player

COLORS = {
    # "red",  # AI color
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white"
}


class MainInterface:
    instructions = """Instructions: 
    A gameplay example, shows the first player starting Connect Four by 
    dropping one of their yellow discs into the center column of an empty game board. The two players then alternate 
    turns dropping one of their discs at a time into an unfilled column, until the second player, with red discs, 
    achieves a diagonal four in a row, and wins the game. If the board fills up before either player achieves four in 
    a row, then the game is a draw. 
    Input x/q - break/give up, -1 VP"""

    def __init__(self):
        self.statistics: dict[str, int] = {}
        self.code_player_map: dict[int, Player | None] = {
            EMPTY_CODE: None,
            FIRST_PLAYER_CODE: None,
            SECOND_PLAYER_CODE: None,
        }
        self.player_code_map: dict[str, int] = {}
        # "player1_name": FIRST_PLAYER_CODE,
        # "player2_name": SECOND_PLAYER_CODE,

    def main(self):
        self.print_instructions()

        board = Board()
        game_logic = GameLogic()
        while True:
            board.clear()

            # input data
            game_mode = input("Choose mode one or two players (1/2): ")
            player1 = self.create_player("first", None)
            if game_mode == "1":
                player2 = AI(game_logic)  # AI is always the second player
            else:
                player2 = self.create_player("second", player1.color)

            # initial score for new players set to 0
            for player in [player1, player2]:
                self.statistics[player.name] = self.statistics.get(player.name, 0)

            self.code_player_map[FIRST_PLAYER_CODE] = player1
            self.code_player_map[SECOND_PLAYER_CODE] = player2
            self.player_code_map[player1.name] = FIRST_PLAYER_CODE
            self.player_code_map[player2.name] = SECOND_PLAYER_CODE

            # game flow
            self.display_board(board)
            game_over = False
            while not game_over:
                for player in [player1, player2]:
                    cprint(player.name, player.color, end=" ")
                    print("turn.")
                    if not self.take_turn(player, board, game_logic):
                        game_over = True
                        self.statistics[player.name] -= 1
                        print(player.name+" gave up!")
                        break
                    self.display_board(board)
                    if game_over := self.game_over(board, game_logic, player):
                        if game_logic.win_situation(board):
                            self.statistics[player.name] += 1
                        break

            # results
            self.print_statistics()

            print("Do you want to repeat? (y/n): ", end="")
            if input().lower() != "y":
                break

    def create_player(self, player_order: str, excludeColor):
        name = input(f"Enter name for the {player_order} player: ")
        newCOLORS = COLORS-{excludeColor}
        print(*newCOLORS)
        color = input(f"Enter color for the {player_order} player: ")
        while color not in newCOLORS or not color:
            print("Wrong color")
            color = input(f"Enter color of the {player_order} player: ")
        return Human(name, color)

    def print_instructions(self):
        """
        print game rules
        """
        print(self.instructions)

    def print_statistics(self):
        print("Statistic:")
        for player_name, score in self.statistics.items():
            print(f"\t{player_name} - {str(score)}")

    def take_turn(self, player: Player, board: Board, game_logic: GameLogic) -> bool:
        """
        player make move or give up

        :param player: current player
        :param board: game board
        :param game_logic: game_logic
        :return: True - normal turn, False - break
        """
        while True:
            location = player.make_move(board)
            if location == (EXIT_CODE, EXIT_CODE):
                return False
            if not game_logic.is_legal(location, board):
                print("Wrong move! Repeat please.")
            else:
                break
        board.place_piece(self.player_code_map[player.name], location)
        return True

    def display_board(self, board: Board) -> None:
        """
        draw game situation

        :param board: game board
        """
        default_color = "grey"
        for row in board.field:
            for item in row:
                if player := self.code_player_map[item]:
                    color = player.color
                else:
                    color = default_color
                cprint("●", color, end=" ")
            print()
        print()

    def game_over(self, board: Board, game_logic: GameLogic, player: Player) -> bool:
        """
        game over if win or tie
        """
        if game_logic.win_situation(board):
            cprint(player.name, player.color, end=" ")
            print("win!")
            return True
        if game_logic.board_full(board):
            print("Tie!")
            return True
        return False
