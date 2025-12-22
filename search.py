"""Basic search for SCE: negamax with alpha-beta and iterative deepening.

search(board, depth, time_ms, uci_info) -> (best_move, score, depth_reached)

- depth: if None, a small default depth is used
- time_ms: time budget in milliseconds (or None for no limit)
- uci_info: optional callback used to print info lines: uci_info(depth, score, nodes, nps, time_ms)
"""
import time
from move_gen import generate_legal_moves
from make_move import make_move, unmake_move
from eval import evaluate
from move_gen import is_square_attacked

MATE_SCORE = 1_000_000
INF = 10**9


class Searcher:
    def __init__(self):
        self.nodes = 0
        self.start_time = 0
        self.time_limit_ms = None
        self.stop = False

    def timed_out(self):
        if self.time_limit_ms is None:
            return False
        elapsed_ms = (time.time() - self.start_time) * 1000
        return elapsed_ms >= self.time_limit_ms

    def negamax(self, board, depth, alpha, beta):
        """Negamax search returning score from White's perspective."""
        if self.timed_out():
            self.stop = True
            return 0

        self.nodes += 1

        #Terminal condition: check for no legal moves (mate/stalemate)
        moves = generate_legal_moves(board)
        if depth == 0 or not moves:
            if not moves:
                #No legal moves — check if side to move is in check
                king = 'K' if board.side_to_move == 0 else 'k'
                king_positions = board.piece_list.get(king, [])
                if king_positions and is_square_attacked(board, king_positions[0], 1 - board.side_to_move):
                    #Checkmate for side to move
                    return -MATE_SCORE
                else:
                    #Stalemate or no moves
                    return 0
            #Leaf node
            return evaluate(board)

        best = -INF
        for move in moves:
            undo = make_move(board, move)
            val = -self.negamax(board, depth - 1, -beta, -alpha)
            unmake_move(board, undo)

            if self.stop:
                return 0

            if val > best:
                best = val
            if val > alpha:
                alpha = val
            if alpha >= beta:
                break  #Beta cut-off

        return best


def search(board, depth=None, time_ms=None, uci_info=None):
    """Top-level search entry.

    Returns (best_move, best_score, depth_reached).
    """
    se = Searcher()
    se.nodes = 0
    se.start_time = time.time()
    se.time_limit_ms = time_ms
    se.stop = False

    #Choose default depth if none provided
    if depth is None:
        max_depth = 3
    else:
        max_depth = depth

    best_move = None
    best_score = 0
    depth_reached = 0

    for d in range(1, max_depth + 1):
        if se.timed_out():
            break

        root_alpha = -INF
        root_beta = INF
        moves = generate_legal_moves(board)
        if not moves:
            #No legal moves at root
            king = 'K' if board.side_to_move == 0 else 'k'
            kp = board.piece_list.get(king, [])
            if kp and is_square_attacked(board, kp[0], 1 - board.side_to_move):
                best_score = -MATE_SCORE
            else:
                best_score = 0
            depth_reached = d - 1
            break

        local_best_move = None
        local_best_score = -INF

        for move in moves:
            if se.timed_out():
                break
            undo = make_move(board, move)
            score = -se.negamax(board, d - 1, -root_beta, -root_alpha)
            unmake_move(board, undo)

            if se.stop:
                break

            if score > local_best_score:
                local_best_score = score
                local_best_move = move
            if score > root_alpha:
                root_alpha = score

        if se.stop or se.timed_out():
            break

        best_move = local_best_move
        best_score = local_best_score
        depth_reached = d

        #UCI info callback
        if uci_info:
            elapsed_ms = int((time.time() - se.start_time) * 1000)
            nps = int(se.nodes / max(1, (time.time() - se.start_time)))
            uci_info(d, best_score, se.nodes, nps, elapsed_ms)

    return best_move, best_score, depth_reached
