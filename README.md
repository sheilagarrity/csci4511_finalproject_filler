Introduction to AI Algorithms Final Project: AI Agent for Filler Game Using Depth-Limited Minimax With Alpha-Beta Pruning
Sheila Garrity
December 13, 2024

# Overview of Filler
Filler is a minigame made by Apple’s GamePigeon. It involves two players battling for dominance of a board broken up into small, colorful tiles. One player starts in the bottom-left corner of the board, and the other player starts in the top-right corner. At each turn, the player selects a color. If any of their tiles are adjacent to tiles of that same color, they are placed under the player’s control. The game ends when all of the tiles are under the control of either player. The score corresponds to the number of tiles each player controls – whoever controls the most tiles wins! 

# Software and Hardware Requirements
Python 3 must be installed in order to run the files. No extra hardware is required.
***You can run the files by running python3 filler.py.***

# Links to Data Sources
There is no outside data being used.

# Motivation for Project
One of my go-to cures for boredom is to text my friends who also have iPhones and have them play me in different GamePigeon games. There are a lot to choose from: minigolf, darts, basketball, and checkers are some of the more popular options. But, one of my favorites is Filler. I annoy my friends and family all the time with it, even though I’m not great at it. When I was thinking of final project ideas, this was one that came to mind. Since I like playing the game, I thought that creating (and extensively testing) an AI agent to play me in it would be fun and keep me engaged in my work.

# Explanation of Accomplishments
## **boards.py** holds the majority of the gameboard functionality.
- The Board object outlines dimensions and colors used to create the board.
    - Tiles are the letters associated with the available board colors (ex. r is red, g is green, etc). They are used for all of the board functionality.
    - Colors is a dictionary that shows the relationship with each tile and a square emoji of the corresponding color. This is used to visually represent the board.
- *create_random*
    - Creates a randomized game board in which no two adjacent tiles are the same color.
    - Assigns the user to start in the bottom-left corner of the board and the AI agent to the top-right corner of the board.
    - Creates a player_board: a 2D array that will fill with 0s and 1s corresponding to which player controls that tile.
        - If neither player controls it, it will be empty.
        - 0 represents the user, 1 represents the AI agent.
- *get_player_tiles* tells which corner a player controls.
- *get_legal_moves* returns a set of moves that a player can make in a given round.
    - Includes all colors except the colors currently being used by the players.
- *get_good_moves* returns a set of legal moves for a player that would increase their score by at least one point.
    - For each legal move, visit all of the tiles controlled by the player.
    - If that tile has an adjacent tile that is uncontrolled, that move is considered “good”.
- *add_move* is run after the player selects a move.
    - Changes the color of all player-controlled tiles to the color selected by the player.
    - If any of the tiles adjacent to the controlled tiles are the same color, they are put under the player’s control.
- *get_board_value* calculates the difference in score between the two players.
    - If the value is greater than 0, the user is winning.
    - If the value is less than 0, the user is losing.
    - If the value is exactly 0, the user and AI agent are tied.
- *game_over* returns a boolean determining if the game is over or not.
    - If every tile is under control, there are no more moves to be made, so return True.
- *print_board* uses the colors dictionary to print the board to the user’s terminal at the beginning of each turn.
- print_score determines the score by finding the number of tiles controlled by each player. These numbers are printed to the user’s terminal at the beginning of every turn.

## **ai.py** contains logic for the AI agent.
- The *Agent* object contains the agent’s player number (which is 1) and the maximum search depth for each turn.
    - After testing, it was found that a depth of 10 was the highest depth that could be used that would allow the user to complete rounds in a short amount of time (less than 10 seconds).
- *choose_move* uses a depth-limited Minimax algorithm with alpha-beta pruning to allow the AI agent to determine their next move.
    - At first, alpha is set to a very low number, and beta is set to a very high number.
    - For each potential move, a new Agent is made and recursively calls choose_move until the maximum search depth is reached. – read more about gathering potential moves in “Measuring Successes”.
    - This recursion allows the agent to find the move that will increase their score the most.
    - If the highest score found in each iteration is greater than the current value for beta, alpha is set to the higher value between itself and the score of the best move.
    - If the highest score found in each iteration is less than than the current value for alpha, beta is set to the lower value between itself and the score of the best move.
- Once the maximum search depth is reached, the opponent’s score and corresponding move are recorded as best_move_score and best_move, and they are added to the board using add_move.

## **filler.py** allows the game to be run easily.
- *play*
    - Prompts boards.py to create a random board.
    - Prompts the user for a move, then determines if it’s a legal move or not using get_move.
    - *get_move*
        - Requires that the user inputs a color from the predefined colors list as their move.
        - The user can not input a color that is currently being used by the player or the AI agent.
        - If the user puts in (1) a letter that is not on the predefined colors list, or (2) a letter that corresponds to a color being used on the current board, an error message is displayed that tells the user the colors they can pick.
        - If the user inputs ‘q’, the game quits immediately and prints “Game quit successfully” to the user’s terminal.
    - Prompts boards.py to add the move to the board by calling add_move (see boards.py section).
    - Prompts boards.py to print the new board and score by calling print_board and print_score (see boards.py section).
    - After the game ends, filler.py determines if the player won, lost, or tied.
        - Calls get_board_value in boards.py (see boards.py section).
        - If the function returns a positive number, a winning message will be printed.
            - “You Win!”
        - If the function returns a negative number, a losing message will be printed.
            - “You Lose!”
        - If the function returns a zero, a “tie” message will be printed.
            - “Tie!”

# Measuring Success
    One of the first successes of the project was figuring out a straightforward way to depict gameplay to the user. It would be extremely difficult for a user to play successfully without seeing the board, and describing the board with words using print statements wouldn’t be enough to give them an idea of how the game worked. I knew I didn’t have the expertise to create a sophisticated game engine like we’ve seen in previous homework assignments, and there wasn’t enough time for me to research how to do it effectively. Luckily, the Filler game board is much simpler than Pacman, so I was able to use emojis and print statements to my advantage to display a simple board. This also made it easy for the board to be updated after each player’s turn.

    In the beginning of the project, I had the goal of having the AI agent use Monte Carlo Tree Search to play the user. As I attempted to implement it, and kept running into problems – as a result, I went back to the drawing board to see if I could use a different tree search algorithm. Expectimax was another option, but after the board is randomly generated, there are no aspects of chance in the game. So, I eventually landed on Minimax. The state space for Filler is extremely large and would take a long time for just Minimax to process completely, so I also implemented alpha-beta pruning and a maximum depth limit. This helped to decrease the computing time when it was the agent’s turn, which makes it more enjoyable for the user to play. Even though the algorithm is simpler than I originally set out for it to be, the one I created still successfully plays the game (maybe I’m bad at it, but I lost a few times while testing).

    Traditional alpha-beta pruning is implemented, and I also included a bit of “pseudo-pruning”. When the AI agent gathers their potential moves, they first get moves that will increase their score by at least one point (using get_good_moves). If there are good moves to make, the agent does not gather information on any other moves, which would include moves that would not increase their score. If the agent doesn’t have any moves that would increase their score, they find the first legal move and use that as their move. I chose to assume that any move that doesn’t increase a player’s score will have the same effect on the game. So, by eliminating the other legal moves, it decreases the computational time needed for the agent to complete their turn. The caveat to this is that this pruning cuts off any sequences of moves stemming from those pruned branches, some of which could result in a win. I prioritized making the game run faster over exploring all possible options of gameplay, which I believe makes for a more enjoyable playing experience.

    I ran into lots of problems over the course of this project and I didn’t achieve exactly what I set out to do, but I’m happy with what I was able to accomplish. I aim to work on it in the future to see if I can improve it further. This class was my first exposure to AI algorithms and even though it was challenging, I think it laid a solid foundation for me to use in future exploration. Thank you so much for a wonderful semester, happy holidays!

