#Project Overview
Connect Four is a two-player connection game in which the players first choose a color and then take turns dropping colored discs from the top into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the next available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs. There is an option for 2 players to play or if only one player is available then to play against AI. The winner is whoever has a continuous stack of 4 pieces in either a horizontal, vertical or diagonal fashion (e.g. next to each other in one of those directions). 

##Class MainInterface
It holds what users interact with and sees during the game.
Here’s a list of functions that I will create:

`def __init__()`:
Initializes the object.

`def main()`: 
The main function to run the game. 

`def create_player()`: 
Give a user interface to create player. 

`def print_instructions()`: 
Prints instructions. 

`def print_statistics()`: 
Prints statistics. 

`def take_turn(player,board)`: 
`Has the player make a move. 

`def display_board(board)`: 
Prints the board. Input Board. 

`def game_over(board, game_logic)`: 
Checks if the game has ended and handle final output. 


##Class GameLogic
It holds the game rules about how the game will run and what rules will be applied. 
Here’s a list of functions that I will create:

`def is_legal(location, board)`:
Checks if a move to this location is valid. 

`def win_situation(board)`: 
Checks if there is win situation on the current turn on the board. Player. 

`def board_full(board)`: 
Checks if there are no more move.


##Class Board
Is stores information about the board, the current state of the game and where all the pieces are. 

Here’s a list of functions:

`def __init__(length: int = 7, height: int = 6)`: 
Initializes an empty board at the beginning of the game.
Take in length and height.

`def place_piece(piece, location)`: 
Adds a piece in location to the board. 

`def is_full()`: 
Checks if the board is already full. 

`def clear()`: 
Resets the board.

##Class Player
Base class for Human and AI
It holds the name of the player and his color.

`def __init__(name, color)`: initializes the object. 
`make_move(board)` : Gets an input from the user or AI where to move.

##Class Human (Player)
`make_move` : let user choose the column for turn

##Class AI (Player)
Inherited from Player. It holds the logic of a computer player to make moves. 

`def __init__(self, game_logic: GameLogic):`

AI name = "AI",
AI color = "red"
game_logic -  AI needs game logic to check win.

`def make_move(board)`: 
Wrapper function to AI make a move.

Here are three choices in order:

`def winning_move(board)`: 
Checks for a winning move. 

`def blocking_move(board)`: 
Checks for a move to stop the player from winning. 

`def random_move(board)`: 
If there are no winning or blocking moves found, makes a random move.
