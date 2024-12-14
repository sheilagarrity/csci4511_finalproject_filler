from typing import Tuple
import boards

class Agent:
    def __init__(self, player: int, maxdepth: int):
        self.player = player
        self.maxdepth = maxdepth
    
    def choose_move(self, board: boards.Board, depth: int, alpha: int=float('-inf'), beta: int=float('inf')) -> Tuple[str, int]:
        best_move = None
        best_move_score = float('-inf')
      
        # "pseudo-pruning"
        # get good moves first
        potential_moves = board.get_good_moves(player=self.player)             
        # if there are no good moves, get the first legal move
        if not potential_moves:
            potential_moves = list(board.get_legal_moves(player=self.player))[:1]

        if depth < self.maxdepth:
            for move in potential_moves:
                # add move to board
                board_after_move = board.add_move(move=move, player=self.player)

                # create opponent 
                opponent = Agent(player=1-self.player, maxdepth=self.maxdepth)
                # recursively find the opponent's best move and score
                opponent_move, opponent_score = opponent.choose_move(board=board_after_move, depth=depth+1, alpha=alpha, beta=beta)
                # whatever move a player makes will have the negative effect on the opponent
                move_score = -opponent_score

                # if the score is better than current max, save the move
                if best_move_score is None or move_score > best_move_score:
                    best_move, best_move_score = move, move_score

                # pruning
                # AI is maximizing agent
                if self.player == 1:
                    if best_move_score > beta:
                        break
                    alpha = max(alpha, best_move_score)
                # player is minimizing agent
                else:
                    if best_move_score < alpha:
                        break
                    beta = min(beta, best_move_score)

        # if reached maxdepth
        else:
            for move in potential_moves:
                # add move to board and see if it improved value of board
                board_after_move = board.add_move(move=move, player=self.player)
                move_score = board_after_move.get_board_value(player=self.player)

                # if the score is better than current max, save the move
                if best_move_score is None or move_score > best_move_score:
                    best_move, best_move_score = move, move_score

                # pruning - AI is maximizing agent
                if self.player == 1:
                    if best_move_score > beta:
                        break
                    alpha = max(alpha, best_move_score)
                # player is minimizing agent
                else:
                    if best_move_score < alpha:
                        break
                    beta = min(beta, best_move_score)

        return best_move, best_move_score
