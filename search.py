import time
from board import Board
from move_gen import generate_legal_moves, is_square_attacked
from make_move import make_move, unmake_move
from eval import evaluate
from constants import INFINITY, MATE_SCORE, TIME_CHECK_NODES, MAX_SEARCH_DEPTH

# Global state for time management
class SearchState:
    def __init__(self):
        self.start_time = None
        self.allocated_time_ms = None
        self.node_count = 0
        self.should_stop = False
    
    def reset(self, allocated_time_ms):
        self.start_time = time.time() * 1000  # Convert to milliseconds
        self.allocated_time_ms = allocated_time_ms
        self.node_count = 0
        self.should_stop = False
    
    def check_time(self):
        """Check if we've exceeded allocated time."""
        if self.allocated_time_ms is None:
            return False
        
        elapsed = (time.time() * 1000) - self.start_time
        return elapsed >= self.allocated_time_ms

search_state = SearchState()
def negamax(board: Board, depth: int, alpha: int, beta: int) -> int:
    """
    Negamax search with alpha-beta pruning.
    Returns the score from the perspective of the side to move.
    """
    # Check time limit periodically
    search_state.node_count += 1
    if search_state.node_count % TIME_CHECK_NODES == 0:
        if search_state.check_time():
            search_state.should_stop = True
    
    if search_state.should_stop:
        # Time's up, return evaluation
        return evaluate(board)
    
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


def search(board: Board, depth: int = None, allocated_time_ms: int = None) -> tuple:
    """
    Search for the best move using iterative deepening.
    Returns (best_move, score).
    
    Args:
        board: The board state
        depth: Maximum depth to search (default: MAX_SEARCH_DEPTH)
        allocated_time_ms: Time limit in milliseconds (default: unlimited)
    """
    moves = generate_legal_moves(board)
    
    if not moves:
        return None, 0
    
    if depth is None:
        depth = MAX_SEARCH_DEPTH
    
    # Initialize time management
    search_state.reset(allocated_time_ms)
    
    best_move = moves[0]
    best_score = 0
    
    # Iterative deepening: search depth 1, 2, 3, ... until time runs out
    for current_depth in range(1, depth + 1):
        if search_state.should_stop:
            break
        
        search_state.node_count = 0
        alpha = -INFINITY
        beta = INFINITY
        current_best_move = moves[0]
        current_best_score = -INFINITY
        
        # Search at current depth
        for move in moves:
            if search_state.should_stop:
                break
            
            undo = make_move(board, move)
            score = -negamax(board, current_depth - 1, -beta, -alpha)
            unmake_move(board, undo)
            
            if score > current_best_score:
                current_best_score = score
                current_best_move = move
            
            alpha = max(alpha, score)
        
        # If we didn't timeout, save the result from this depth
        if not search_state.should_stop:
            best_move = current_best_move
            best_score = current_best_score
    
    return best_move, best_score