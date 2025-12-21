import sys
import time
from board import Board
from fen import fen_to_board, board_to_fen
from move_gen import generate_legal_moves
from make_move import make_move
from perft import perft, index_to_algebraic
from constants import STARTING_FEN, DEFAULT_MOVES_TO_GO, TIME_SAFETY_MARGIN_MS, MIN_THINK_TIME_MS

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
    if not tokens:
        return
    token_index = 0
    
    if tokens[token_index] == 'startpos':
        fen_to_board(board, STARTING_FEN)
        token_index += 1
    elif tokens[token_index] == 'fen':
        token_index += 1
        fen_parts = []
        while token_index < len(tokens) and tokens[token_index] != 'moves':
            fen_parts.append(tokens[token_index])
            token_index += 1
        fen_str = ' '.join(fen_parts)
        fen_to_board(board, fen_str)
    
    #Apply moves if present
    if token_index < len(tokens) and tokens[token_index] == 'moves':
        token_index += 1
        while token_index < len(tokens):
            move = uci_to_move(board, tokens[token_index])
            make_move(board, move)
            token_index += 1


def parse_go(board: Board, tokens: list) -> str:
    """Parse 'go' command and return best move."""
    from search import search
    
    #Check for perft
    if tokens and tokens[0] == 'perft':
        depth = int(tokens[1]) if len(tokens) > 1 else 1
        run_perft_from_uci(board, depth)
        return None
    
    #Parse time parameters
    wtime = None
    btime = None
    winc = 0
    binc = 0
    movestogo = None
    movetime = None
    depth = None
    infinite = False
    
    i = 0
    while i < len(tokens):
        if tokens[i] == 'wtime' and i + 1 < len(tokens):
            wtime = int(tokens[i + 1])
            i += 2
        elif tokens[i] == 'btime' and i + 1 < len(tokens):
            btime = int(tokens[i + 1])
            i += 2
        elif tokens[i] == 'winc' and i + 1 < len(tokens):
            winc = int(tokens[i + 1])
            i += 2
        elif tokens[i] == 'binc' and i + 1 < len(tokens):
            binc = int(tokens[i + 1])
            i += 2
        elif tokens[i] == 'movestogo' and i + 1 < len(tokens):
            movestogo = int(tokens[i + 1])
            i += 2
        elif tokens[i] == 'movetime' and i + 1 < len(tokens):
            movetime = int(tokens[i + 1])
            i += 2
        elif tokens[i] == 'depth' and i + 1 < len(tokens):
            depth = int(tokens[i + 1])
            i += 2
        elif tokens[i] == 'infinite':
            infinite = True
            i += 1
        else:
            i += 1
    
    #Calculate allocated time
    if movetime is not None:
        time_to_use = movetime
    elif infinite:
        time_to_use = None  # No time limit
    elif wtime is not None and btime is not None:
        #Determine our time
        our_time = wtime if board.side_to_move == 0 else btime
        our_inc = winc if board.side_to_move == 0 else binc
        
        #Moves to go
        moves_left = movestogo if movestogo else DEFAULT_MOVES_TO_GO
        
        #Simple time allocation: remaining_time / moves_left + increment * 0.9
        time_to_use = max(
            MIN_THINK_TIME_MS,
            (our_time // moves_left) + int(our_inc * 0.9) - TIME_SAFETY_MARGIN_MS
        )
    else:
        time_to_use = None
    
    #Define info callback for UCI output during search
    def uci_info(depth, score, nodes, nps, time_ms):
        print(f"info depth {depth} score cp {score} nodes {nodes} nps {nps} time {time_ms}")
    
    #Search for best move
    best_move, score, search_depth = search(board, depth, time_to_use, uci_info)
    
    if best_move:
        return move_to_uci(best_move)
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
        if not tokens:
            continue
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
        print(" |", end="")
        for file in range(8):
            square_index = rank * 8 + file
            sq120 = board.mailbox64[square_index]
            piece = board.board_play[sq120]
            char = piece if piece != 0 else ' '
            print(f" {char} |", end="")
        print("\n  +---+---+---+---+---+---+---+---+")
    print("    a   b   c   d   e   f   g   h\n")
    
    side = "White" if board.side_to_move == 0 else "Black"
    print(f"Side to move: {side}")


if __name__ == "__main__":
    uci_loop()