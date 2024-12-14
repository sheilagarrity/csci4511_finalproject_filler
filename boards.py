from copy import deepcopy
import random

# functionality:
#   creates random board
#   add a player's move to the board 
#   retrieves starting position of each player
#   retrieves overall board score
#   retrieves "good" and "legal" moves
#       good: moves to improve a player's score
#       legal: all moves a player can make - won't necessesarily improve their score
#   determines if game is over
#   prints board and score to player's terminal

# visual component - creates and updates boards
class Board:
    def __init__(self):

        # filler board is always a 7x8 rectangle
        self.num_cols = 7
        self.num_rows = 8

        # create empty board
        self.board = list()

        # available color options - called "tiles"
        self.tiles = {'r','g','y','b','p','w'}

        # dictionary to convert tiles to corresponding emojis, used for printing board
        self.colors = {'r':'🟥','g':'🟩','y':'🟨','b':'🟦','p':'🟪','w':'⬜️'}

    # creates a random board
    def create_random(self):

        # 1: randomly generate tile colors #

        # loop through all spaces on board
        for i in range(self.num_rows):
            row = list()
            for j in range(self.num_cols):
                illegal_tiles = set()     # must be a set in order to be compatable with self.tiles

                # get rid of certain color options for tiles - adjacent colors can't be the same color
                # kinda like map coloring :p
                if i > 0:
                    # can't be the same color of above neighbor
                    illegal_tiles.add(self.board[-1][j])
                if j > 0:
                    # can't be the same color of the left neighbor
                    illegal_tiles.add(row[-1])

                # all of the other colors are elegible
                eligible_tiles = self.tiles - illegal_tiles
                # get a random color from elgible colors and assign it to current space in the row
                row.append(random.choice(list(eligible_tiles)))

            # add row to board
            self.board.append(row)

        # 2: create player board and assign corner spaces to players #

        # create an empty 7x8 player board
        # a player board is a 2D array that will fill with 0s and 1s based on the tiles that the players control
        # used to calculate score 
        self.player_board = [[None for j in range(self.num_cols)] for i in range(self.num_rows)]
        # bottom left = user (player 0)
        self.player_board[-1][0] = 0
        # top right = AI agent (player 1)
        self.player_board[0][-1] = 1 

    # "updates" board after move from either player
    def add_move(self, move: str, player: int):
        
        # make a copy of board and player_board bc add_move is called for all potential moves in ai.py
        # we need to keep the original to modify with the move we *actually* pick
        new_board = Board()
        new_board.board = deepcopy(self.board)
        new_board.player_board = deepcopy(self.player_board)

        # go through every space on player_board
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                # check if space is controlled by given player
                if new_board.player_board[i][j] == player:
                    # set color of tile to color of current move
                    new_board.board[i][j] = move

                    # check if neighboring tiles are the same color as the current move and aren't under control
                    # if yes, put them under control of the current player on player_board
                    if ((i > 0) and (new_board.player_board[i-1][j] is None) and (new_board.board[i-1][j] == move)): 
                        new_board.player_board[i-1][j] = player
                        
                    if ((i+1 < self.num_rows) and (new_board.player_board[i+1][j] is None) and (new_board.board[i+1][j] == move)):
                        new_board.player_board[i+1][j] = player

                    if ((j > 0) and (new_board.player_board[i][j-1] is None) and (new_board.board[i][j-1] == move)):
                        new_board.player_board[i][j-1] = player

                    if ((j+1 < self.num_cols) and (new_board.player_board[i][j+1] is None) and (new_board.board[i][j+1] == move)):
                        new_board.player_board[i][j+1] = player    

        return new_board

    # tells which corner each player controls when the game starts
    def get_player_tiles(self) -> str:
        # if p0 is the bottom left
        if self.player_board[(self.num_rows) - 1][0] == 0:
            return self.board[(self.num_rows) - 1][0], self.board[0][(self.num_cols) - 1]
        # if p0 is top right
        else:
            return self.board[0][(self.num_cols) - 1], self.board[(self.num_rows) - 1][0]

    # calculates difference in tiles for each player
    # positive number: user has more tiles
    # negative number: ai agent has more tiles
    # 0: tie
    def get_board_value(self, player: int) -> int:

        player_score = 0
        for i in range(self.num_rows):
            player_score += self.player_board[i].count(player)

        opponent_score = 0
        for i in range(self.num_rows):
            opponent_score += self.player_board[i].count(1 - player)

        return player_score - opponent_score

    # "good" moves are moves that would improve the player's score by at least 1
    def get_good_moves(self, player: int) -> set[str]: 
        good_moves = set()

        # iterate over each tile on the board
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                # check if current tile is controlled by the player
                if self.player_board[i][j] == player:
                    # add adjacent tiles if not already controlled by player
                    if i > 0 and self.player_board[i-1][j] is None:
                        good_moves.add(self.board[i-1][j])

                    if i+1 < self.num_rows and self.player_board[i+1][j] is None:
                        good_moves.add(self.board[i+1][j])

                    if j > 0 and self.player_board[i][j-1] is None:
                        good_moves.add(self.board[i][j-1])

                    if j+1 < self.num_cols and self.player_board[i][j+1] is None:
                        good_moves.add(self.board[i][j+1])

        # get beginning tile that each player controls
        player_0_tile, player_1_tile = self.get_player_tiles()

        # subtract controlled tiles from potential tiles 
        return good_moves - {player_0_tile, player_1_tile}

    # all legal moves a given player can make
    # doesn't necessarily improve their score
    def get_legal_moves(self, player: int) -> set[str]:
        player_0_tile, player_1_tile = self.get_player_tiles()
        # return all tiles other than the current ones
        return self.tiles - {player_0_tile, player_1_tile}

    # checks if game is over
    def game_over(self) -> bool:
        # check every tile to if player_board position is filled
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                # if one is not filled, the game isn't over yet
                if self.player_board[i][j] is None:
                    return False
        # if all are filled, the game is over
        return True


    ### PRINTING BOARD ###

    # print board to terminal
    def print_board(self):
        for row in self.board:
            for i, tile in enumerate(row):
                print(f"{self.colors[tile]}", end = "") # end = "" keeps python from printing a new line after each 
                # make sure they print the correct configuration
                if i + 1 < self.num_cols:
                    print(" ", end = "")
            print("")

    # get current score
    def print_score(self):
        user_score = sum(self.player_board[i].count(0) for i in range(self.num_rows))
        ai_score = sum(self.player_board[i].count(1) for i in range(self.num_rows))
        print("       SCORE")
        print("You: " + str(user_score) + "   Opponent: " + str(ai_score))