#Functions for performing perft
import time
from board import Board
from fen import fen_to_board
from move_gen import generate_legal_moves
from make_move import make_move, unmake_move
from constants import PERFT_RESULTS

def perft(board: Board, depth: int) -> int:
    """Count all leaf nodes at the given depth."""
    if depth == 0:
        return 1
    
    moves = generate_legal_moves(board)
    nodes = 0
    
    for move in moves:
        undo = make_move(board, move)
        nodes += perft(board, depth - 1)
        unmake_move(board, undo)
    
    return nodes

def perft_divide(board: Board, depth: int) -> dict:
    """Perft with move breakdown - useful for debugging."""
    moves = generate_legal_moves(board)
    results = {}
    total = 0
    
    for move in moves:
        undo = make_move(board, move)
        nodes = perft(board, depth - 1)
        unmake_move(board, undo)
        
        move_str = index_to_algebraic(move[0]) + index_to_algebraic(move[1])
        if len(move) > 2 and move[2]:
            move_str += f" ({move[2]})"
        
        results[move_str] = nodes
        total += nodes
    
    return results, total

def index_to_algebraic(sq120: int) -> str:
    """Convert 120-index to algebraic notation (e.g., 95 -> 'e1')."""
    file_idx = (sq120 % 10) - 1  # 0-7
    rank = 10 - (sq120 // 10)  # 1-8
    return chr(ord('a') + file_idx) + str(rank)

def run_perft_tests():
    """Run perft tests against known results."""
    print("Running perft tests...\n")
    
    for fen, expected_results in PERFT_RESULTS.items():
        print(f"FEN: {fen[:50]}...")
        board = Board()
        fen_to_board(board, fen)
        
        for depth, expected in enumerate(expected_results, start=1):
            #if depth > 3:  #Limit depth for speed during testing
            #    break
            
            start_time = time.time()
            result = perft(board, depth)
            elapsed = time.time() - start_time
            
            status = "✓" if result == expected else "✗"
            nps = int(result / elapsed) if elapsed > 0 else 0
            print(f"  Depth {depth}: {result:>10} (expected {expected:>10}) {status}  [{elapsed:.3f}s, {nps:,} nps]")
            
            if result != expected:
                print(f"    MISMATCH! Difference: {result - expected}")
        print()


def debug_perft(fen: str, depth: int):
    """Debug a specific position with divide."""
    board = Board()
    fen_to_board(board, fen)
    
    print(f"Position: {fen}")
    print(f"Depth: {depth}\n")
    
    results, total = perft_divide(board, depth)
    
    for move, nodes in sorted(results.items()):
        print(f"  {move}: {nodes}")
    
    print(f"\nTotal: {total}")
    print(f"Moves: {len(results)}")

if __name__ == "__main__":
    run_perft_tests()