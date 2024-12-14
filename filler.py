import ai, boards

# functionality:
#   provides skeleton of gameplay
#       (1) create random board
#       (2) get move from player or AI agent
#       (3) verify that the move is legal
#       (4) add move to board
#       (5) print new board and score

# main function that allows for gameplay
def play():
    # create a random board
    board = boards.Board()
    board.create_random()

    # print score and board to user
    board.print_score()
    board.print_board()

    alpha = float('-inf')   # worst possible score for maximizing player
    beta = float('inf')     # worst possible score for minimizing player

    # one iteration of loop is one turn of the game (player and agent)
    while not board.game_over():

        ### user moves ###
        # get (and validate) next move from user
        print("> ", end = "")
        move = get_move(board=board)

        # if the player inputs "q", end the game
        if move == "q":
            print("")
            print("Game quit successfully.")
            print("")
            return

        # add user move to board
        board = board.add_move(move=move, player=0)
        ### end user moves ###

        ### AI moves ###
        # create AI agent for current board
        ai_agent = ai.Agent(player=1, maxdepth=10) # after testing, 10 is the highest depth to use that doesn't keep you waiting for too long for choose_move() to return

        # agent chooses move and adds it to board
        opponent_move, opponent_score = ai_agent.choose_move(board=board, depth=0, alpha=alpha, beta=beta)
        board = board.add_move(move=opponent_move, player=1)
        ### end AI moves ###

        # print current score and board
        board.print_score() 
        board.print_board()

    # score at the end of the game - determines if player won, lost, or tied
    value = board.get_board_value(player=0)
    if value > 0:
        print("You win!")
        print("Thanks for playing!")
        print("")
    elif value == 0:
        print("Tie!")
        print("Thanks for playing!")
        print("")
    elif value < 0:
        print("You lose!")
        print("Thanks for playing!")
        print("")

# gets and validates user's chosen move
def get_move(board: boards.Board) -> str:
    valid_move = False

    # all legal moves for player
    legal_moves = board.get_legal_moves(0)

    # wait until there's a valid move
    while not valid_move:
        # get input from keyboard
        move = input()
        
        # a valid move is anything in legal_moves OR a quit
        valid_move = move in legal_moves or move == "q"

        if not valid_move:
            # give player all legal moves if they input an invalid move
            # then wait for them to input something else
            print("Move is not valid. Valid moves are: ", legal_moves)
            print("> ", end = "")
    return move 

if __name__ == "__main__":
    print("")
    print("Beginning game...")
    print("")

    play()