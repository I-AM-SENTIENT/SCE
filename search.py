from board import Board
from move_gen import generate_legal_moves, is_square_attacked
from make_move import make_move, unmake_move
from eval import evaluate
from constants import INFINITY, MATE_SCORE
def negamax(board: Board, depth: int, alpha: int, beta: int) -> int:
    """
    Negamax search with alpha-beta pruning.
    Returns the score from the perspective of the side to move.
    """
    #Base case: evaluate at leaf nodes
    if depth == 0:
        return evaluate(board)
    
    moves = generate_legal_moves(board)
    
    #Checkmate or stalemate
    if not moves:
        #Check if king is in check
        king = 'K' if board.side_to_move == 0 else 'k'
        king_sq = board.piece_list[king][0]
        in_check = is_square_attacked(board, king_sq, 1 - board.side_to_move)
        
        if in_check:
            #Checkmate - return negative score (bad for us)
            #Add depth so shorter mates are preferred
            return -MATE_SCORE + (100 - depth)
        else:
            #Stalemate - draw
            return 0
    
    best_score = -INFINITY
    
    for move in moves:
        undo = make_move(board, move)
        score = -negamax(board, depth - 1, -beta, -alpha)
        unmake_move(board, undo)
        
        best_score = max(best_score, score)
        alpha = max(alpha, score)
        
        #Beta cutoff - opponent won't allow this line
        if alpha >= beta:
            break
    
    return best_score


def search(board: Board, depth: int) -> tuple:
    """
    Search for the best move.
    Returns (best_move, score).
    """
    moves = generate_legal_moves(board)
    
    if not moves:
        return None, 0
    
    best_move = moves[0]
    best_score = -INFINITY
    alpha = -INFINITY
    beta = INFINITY
    
    for move in moves:
        undo = make_move(board, move)
        score = -negamax(board, depth - 1, -beta, -alpha)
        unmake_move(board, undo)
        
        if score > best_score:
            best_score = score
            best_move = move
        
        alpha = max(alpha, score)
    
    return best_move, best_score