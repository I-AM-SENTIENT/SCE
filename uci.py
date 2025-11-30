import sys
from board import Board
from fen import fen_to_board, board_to_fen
from move_gen import generate_legal_moves
from make_move import make_move
from perft import perft, index_to_algebraic
from constants import STARTING_FEN

ENGINE_NAME = "SCE"
ENGINE_AUTHOR = "I-AM-SENTIENT"


def algebraic_to_index(alg: str) -> int:
    """Convert algebraic notation to 120-index."""
    file = ord(alg[0]) - ord('a')  # 0-7
    rank = int(alg[1])  # 1-8
    #Directly convert to 120 index
    return 21 + (8 - rank) * 10 + file


def move_to_uci(move: tuple) -> str:
    """Convert internal move tuple to UCI string (e.g., 'e2e4')."""
    from_sq = index_to_algebraic(move[0])
    to_sq = index_to_algebraic(move[1])
    
    #Handle promotion
    if len(move) > 2 and move[2]:
        flag = move[2]
        if flag.startswith('promo_'):
            promo_piece = flag[-1]  #'q', 'r', 'b', 'n'
            return from_sq + to_sq + promo_piece
    
    return from_sq + to_sq


def uci_to_move(board: Board, uci_str: str) -> tuple:
    """Convert UCI string to internal move tuple."""
    from_sq = algebraic_to_index(uci_str[0:2])
    to_sq = algebraic_to_index(uci_str[2:4])
    
    #Check for promotion
    promo = None
    if len(uci_str) == 5:
        promo_char = uci_str[4]
        promo = f'promo_{promo_char}'
    
    #Find matching legal move (to get correct flags)
    legal_moves = generate_legal_moves(board)
    for move in legal_moves:
        if move[0] == from_sq and move[1] == to_sq:
            if promo:
                if len(move) > 2 and move[2] == promo:
                    return move
            else:
                #For non-promotion moves, return first match
                #This handles castling, en passant, double push flags
                if len(move) <= 2 or not move[2].startswith('promo_'):
                    return move
    
    #Fallback (shouldn't happen with legal input)
    return (from_sq, to_sq, promo) if promo else (from_sq, to_sq)


def parse_position(board: Board, tokens: list):
    """Parse 'position' command."""
    idx = 0
    
    if tokens[idx] == 'startpos':
        fen_to_board(board, STARTING_FEN)
        idx += 1
    elif tokens[idx] == 'fen':
        idx += 1
        fen_parts = []
        while idx < len(tokens) and tokens[idx] != 'moves':
            fen_parts.append(tokens[idx])
            idx += 1
        fen_str = ' '.join(fen_parts)
        fen_to_board(board, fen_str)
    
    #Apply moves if present
    if idx < len(tokens) and tokens[idx] == 'moves':
        idx += 1
        while idx < len(tokens):
            move = uci_to_move(board, tokens[idx])
            make_move(board, move)
            idx += 1


def parse_go(board: Board, tokens: list) -> str:
    """Parse 'go' command and return best move."""
    #Check for perft
    if tokens and tokens[0] == 'perft':
        depth = int(tokens[1]) if len(tokens) > 1 else 1
        run_perft_from_uci(board, depth)
        return None
    
    #For now, just return a random legal move
    #Later: implement actual search
    moves = generate_legal_moves(board)
    if moves:
        return move_to_uci(moves[0])
    return None


def run_perft_from_uci(board: Board, depth: int):
    """Run perft and print results in UCI format."""
    import time
    
    moves = generate_legal_moves(board)
    total = 0
    start = time.time()
    
    for move in moves:
        undo = make_move(board, move)
        nodes = perft(board, depth - 1) if depth > 1 else 1
        from make_move import unmake_move
        unmake_move(board, undo)
        
        print(f"{move_to_uci(move)}: {nodes}")
        total += nodes
    
    elapsed = time.time() - start
    print(f"\nNodes searched: {total}")
    print(f"Time: {elapsed:.3f}s")
    if elapsed > 0:
        print(f"NPS: {int(total / elapsed):,}")


def uci_loop():
    """Main UCI communication loop."""
    board = Board()
    fen_to_board(board, STARTING_FEN)
    
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        
        if not line:
            continue
        
        tokens = line.split()
        cmd = tokens[0]
        
        if cmd == 'uci':
            print(f"id name {ENGINE_NAME}")
            print(f"id author {ENGINE_AUTHOR}")
            #Add options here later
            print("uciok")
        
        elif cmd == 'isready':
            print("readyok")
        
        elif cmd == 'ucinewgame':
            board = Board()
            fen_to_board(board, STARTING_FEN)
        
        elif cmd == 'position':
            parse_position(board, tokens[1:])
        
        elif cmd == 'go':
            best_move = parse_go(board, tokens[1:])
            if best_move:
                print(f"bestmove {best_move}")
        
        elif cmd == 'd':
            #Debug: print board and FEN
            print_board(board)
            print(f"\nFEN: {board_to_fen(board)}")
        
        elif cmd == 'quit':
            break
        
        #Flush output for GUI communication
        sys.stdout.flush()


def print_board(board: Board):
    """Print board for debugging."""
    print("\n  +---+---+---+---+---+---+---+---+")
    for rank in range(8):
        print(f"{8 - rank} |", end="")
        for file in range(8):
            idx64 = rank * 8 + file
            sq120 = board.mailbox64[idx64]
            piece = board.board_play[sq120]
            char = piece if piece != 0 else ' '
            print(f" {char} |", end="")
        print("\n  +---+---+---+---+---+---+---+---+")
    print("    a   b   c   d   e   f   g   h\n")
    
    side = "White" if board.side_to_move == 0 else "Black"
    print(f"Side to move: {side}")


if __name__ == "__main__":
    uci_loop()