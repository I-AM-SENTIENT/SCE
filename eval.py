from board import Board
from constants import PIECE_VALUES
#Piece values in centipawns
def evaluate(board: Board) -> int:
    """
    Evaluate the position from the perspective of the side to move.
    Positive = good for side to move, negative = bad.
    """
    score = 0
    
    #Material count
    for piece, positions in board.piece_list.items():
        score += PIECE_VALUES[piece] * len(positions)
    
    #Return from perspective of side to move
    if board.side_to_move == 1:  # Black to move
        score = -score
    
    return score