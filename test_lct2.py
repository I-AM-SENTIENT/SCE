"""
LCT II (Louguet Chess Test II) - 35 tactical test positions
This test suite evaluates tactical strength of chess engines.
Each position has a best move that should be found.
"""

import time

from board import Board
from fen import fen_to_board
from search import search
from perft import index_to_algebraic


# LCT II test positions with FEN and best move(s)
LCT2_POSITIONS = [
    {
        "id": 1,
        "fen": "r3kb1r/3n1pp1/p6p/2pPp2q/Pp2N3/3B2PP/1PQ2P2/R3K2R w KQkq -",
        "best_moves": ["d6"],
        "description": "LCTII.POS.01 - Chernin - Miles, Tunis 1985"
    },
    {
        "id": 2,
        "fen": "1k1r3r/pp2qpp1/3b1n1p/3pNQ2/2pP1P2/2N1P3/PP4PP/1K1RR3 b - -",
        "best_moves": ["Bb4"],
        "description": "LCTII.POS.02 - Lilienthal - Botvinnik, Moskau 1945"
    },
    {
        "id": 3,
        "fen": "r6k/pp4p1/2p1b3/3pP3/7q/P2B3r/1PP2Q1P/2K1R1R1 w - -",
        "best_moves": ["Qc5"],
        "description": "LCTII.POS.03 - Boissel - Boulard, corr. 1994"
    },
    {
        "id": 4,
        "fen": "1nr5/2rbkppp/p3p3/Np6/2PRPP2/8/PKP1B1PP/3R4 b - -",
        "best_moves": ["e5"],
        "description": "LCTII.POS.04 - Kaplan - Kopec, USA 1975"
    },
    {
        "id": 5,
        "fen": "2r2rk1/1p1bq3/p3p2p/3pPpp1/1P1Q4/P7/2P2PPP/2R1RBK1 b - -",
        "best_moves": ["Bb5"],
        "description": "LCTII.POS.05 - Estrin - Pytel, Albena 1973"
    },
    {
        "id": 6,
        "fen": "3r1bk1/p4ppp/Qp2p3/8/1P1B4/Pq2P1P1/2r2P1P/R3R1K1 b - -",
        "best_moves": ["e5"],
        "description": "LCTII.POS.06 - Nimzowitsch - Capablanca, New York 1927"
    },
    {
        "id": 7,
        "fen": "r1b2r1k/pp2q1pp/2p2p2/2p1n2N/4P3/1PNP2QP/1PP2RP1/5RK1 w - -",
        "best_moves": ["Nd1"],
        "description": "LCTII.POS.07 - Tartakower - Rubinstein, Moskau 1925"
    },
    {
        "id": 8,
        "fen": "r2qrnk1/pp3ppb/3b1n1p/1Pp1p3/2P1P2N/P5P1/1B1NQPBP/R4RK1 w - -",
        "best_moves": ["Bh3"],
        "description": "LCTII.POS.08 - Polugaevsky - Unzicker, Kislovodsk 1972"
    },
    {
        "id": 9,
        "fen": "5nk1/Q4bpp/5p2/8/P1n1PN2/q4P2/6PP/1R4K1 w - -",
        "best_moves": ["Qd4"],
        "description": "LCTII.POS.09 - Boissel - Del Gobbo, corr. 1994"
    },
    {
        "id": 10,
        "fen": "r3k2r/3bbp1p/p1nppp2/5P2/1p1NP3/5NP1/PPPK3P/3R1B1R b kq -",
        "best_moves": ["Bf8"],
        "description": "LCTII.POS.10 - Cucka - Jansa, Brno 1960"
    },
    {
        "id": 11,
        "fen": "bn6/1q4n1/1p1p1kp1/2pPp1pp/1PP1P1P1/3N1P1P/4B1K1/2Q2N2 w - -",
        "best_moves": ["h4"],
        "description": "LCTII.POS.11 - Landau - Schmidt, Noordwijk 1938"
    },
    {
        "id": 12,
        "fen": "3r2k1/pp2npp1/2rqp2p/8/3PQ3/1BR3P1/PP3P1P/3R2K1 b - -",
        "best_moves": ["Rb6"],
        "description": "LCTII.POS.12 - Korchnoi - Karpov, Meran 1981"
    },
    {
        "id": 13,
        "fen": "1r2r1k1/4ppbp/B5p1/3P4/pp1qPB2/2n2Q1P/P4PP1/4RRK1 b - -",
        "best_moves": ["Nxa2"],
        "description": "LCTII.POS.13 - Barbero - Kouatly, Budapest 1987"
    },
    {
        "id": 14,
        "fen": "r2qkb1r/1b3ppp/p3pn2/1p6/1n1P4/1BN2N2/PP2QPPP/R1BR2K1 w kq -",
        "best_moves": ["d5"],
        "description": "LCTII.POS.14 - Spasski - Aftonomov, Leningrad 1949"
    },
    {
        "id": 15,
        "fen": "1r4k1/1q2bp2/3p2p1/2pP4/p1N4R/2P2QP1/1P3PK1/8 w - -",
        "best_moves": ["Nxd6"],
        "description": "LCTII.CMB.01 - Romanishin - Gdansky, Polonica Zdroj 1992"
    },
    {
        "id": 16,
        "fen": "rn3rk1/pbppq1pp/1p2pb2/4N2Q/3PN3/3B4/PPP2PPP/R3K2R w KQ -",
        "best_moves": ["Qxh7+"],
        "description": "LCTII.CMB.02 - Lasker,Ed - Thomas, London 1911"
    },
    {
        "id": 17,
        "fen": "4r1k1/3b1p2/5qp1/1BPpn2p/7n/r3P1N1/2Q1RPPP/1R3NK1 b - -",
        "best_moves": ["Qf3"],
        "description": "LCTII.CMB.03 - Andruet - Spassky, BL 1988"
    },
    {
        "id": 18,
        "fen": "2k2b1r/1pq3p1/2p1pp2/p1n1PnNp/2P2B2/2N4P/PP2QPP1/3R2K1 w - -",
        "best_moves": ["exf6"],
        "description": "LCTII.CMB.04 - Vanka - Jansa, Prag 1957"
    },
    {
        "id": 19,
        "fen": "2r2r2/3qbpkp/p3n1p1/2ppP3/6Q1/1P1B3R/PBP3PP/5R1K w - -",
        "best_moves": ["Rxh7+"],
        "description": "LCTII.CMB.05 - Boros - Szabo, Budapest 1937"
    },
    {
        "id": 20,
        "fen": "2r1k2r/2pn1pp1/1p3n1p/p3PP2/4q2B/P1P5/2Q1N1PP/R4RK1 w q -",
        "best_moves": ["exf6"],
        "description": "LCTII.CMB.06 - Lilienthal - Capablanca, Hastings 1934"
    },
    {
        "id": 21,
        "fen": "2rr2k1/1b3ppp/pb2p3/1p2P3/1P2BPnq/P1N3P1/1B2Q2P/R4R1K b - -",
        "best_moves": ["Rxc3"],
        "description": "LCTII.CMB.07 - Rotlewi - Rubinstein, Lodz 1907"
    },
    {
        "id": 22,
        "fen": "2b1r1k1/r4ppp/p7/2pNP3/4Q3/q6P/2P2PP1/3RR1K1 w - -",
        "best_moves": ["Nf6+"],
        "description": "LCTII.CMB.08 - Zarkov - Mephisto, Albuquerque 1991"
    },
    {
        "id": 23,
        "fen": "6k1/5p2/3P2p1/7n/3QPP2/7q/r2N3P/6RK b - -",
        "best_moves": ["Rxd2"],
        "description": "LCTII.CMB.09 - Portisch - Kasparov, Moskau 1981"
    },
    {
        "id": 24,
        "fen": "rq2rbk1/6p1/p2p2Pp/1p1Rn3/4PB2/6Q1/PPP1B3/2K3R1 w - -",
        "best_moves": ["Bxh6"],
        "description": "LCTII.CMB.10 - Tchoudinovskikh - Merchiev, UdSSR 1987"
    },
    {
        "id": 25,
        "fen": "rnbq2k1/p1r2p1p/1p1p1Pp1/1BpPn1N1/P7/2P5/6PP/R1B1QRK1 w - -",
        "best_moves": ["Nxh7"],
        "description": "LCTII.CMB.11 - Vaisser - Genius 2, Aubervilliers, 1994"
    },
    {
        "id": 26,
        "fen": "r2qrb1k/1p1b2p1/p2ppn1p/8/3NP3/1BN5/PPP3QP/1K3RR1 w - -",
        "best_moves": ["e5"],
        "description": "LCTII.CMB.12 - Spassky - Petrosian, Moskau 1969"
    },
    {
        "id": 27,
        "fen": "8/1p3pp1/7p/5P1P/2k3P1/8/2K2P2/8 w - -",
        "best_moves": ["f6"],
        "description": "LCTII.FIN.01 - NN - Lasker,Ed"
    },
    {
        "id": 28,
        "fen": "8/pp2r1k1/2p1p3/3pP2p/1P1P1P1P/P5KR/8/8 w - -",
        "best_moves": ["f5"],
        "description": "LCTII.FIN.02 - Capablanca - Eliskases, Moskau 1936"
    },
    {
        "id": 29,
        "fen": "8/3p4/p1bk3p/Pp6/1Kp1PpPp/2P2P1P/2P5/5B2 b - -",
        "best_moves": ["Bxe4"],
        "description": "LCTII.FIN.03 - Studie 1994"
    },
    {
        "id": 30,
        "fen": "5k2/7R/4P2p/5K2/p1r2P1p/8/8/8 b - -",
        "best_moves": ["h3"],
        "avoid_moves": ["h5"],
        "description": "LCTII.FIN.04 - Karpov - Deep Thought, Analyse 1990"
    },
    {
        "id": 31,
        "fen": "6k1/6p1/7p/P1N5/1r3p2/7P/1b3PP1/3bR1K1 w - -",
        "best_moves": ["a6"],
        "description": "LCTII.FIN.05 - Karpov - Kasparov, Moskau 1985 [Analyse]"
    },
    {
        "id": 32,
        "fen": "8/3b4/5k2/2pPnp2/1pP4N/pP1B2P1/P3K3/8 b - -",
        "best_moves": ["f4"],
        "description": "LCTII.FIN.06 - Minev - Portisch, Halle 1967"
    },
    {
        "id": 33,
        "fen": "6k1/4pp1p/3p2p1/P1pPb3/R7/1r2P1PP/3B1P2/6K1 w - -",
        "best_moves": ["Bb4"],
        "description": "LCTII.FIN.07 - Lengyel - Kaufman, Los Angeles 1974"
    },
    {
        "id": 34,
        "fen": "2k5/p7/Pp1p1b2/1P1P1p2/2P2P1p/3K3P/5B2/8 w - -",
        "best_moves": ["c5"],
        "description": "LCTII.FIN.08 - Spassky - Byrne, 1974"
    },
    {
        "id": 35,
        "fen": "8/5Bp1/4P3/6pP/1b1k1P2/5K2/8/8 w - -",
        "best_moves": ["Kg4"],
        "description": "LCTII.FIN.09 - Klimenok - Kabanov, UdSSR 1969"
    }
]


# Scoring constants
BASE_SCORE = 1900
MAX_PER_POSITION = 30


def points_for_position(correct: bool, elapsed_seconds: float) -> int:
    """Compute LCT2 points for a single position based on time buckets."""
    if not correct:
        return 0

    if elapsed_seconds <= 9:
        return 30
    if elapsed_seconds <= 29:
        return 25
    if elapsed_seconds <= 89:
        return 20
    if elapsed_seconds <= 209:
        return 15
    if elapsed_seconds <= 389:
        return 10
    if elapsed_seconds <= 600:
        return 5
    return 0


def algebraic_to_move(board: Board, alg: str) -> tuple:
    """
    Convert algebraic notation (like 'Bxc6', 'Ng5') to internal move format.
    Returns the matching move from legal moves.
    """
    from move_gen import generate_legal_moves
    
    legal_moves = generate_legal_moves(board)
    
    # Simple approach: convert all legal moves to algebraic and match
    for move in legal_moves:
        move_alg = move_to_simple_algebraic(board, move)
        if move_alg == alg or move_alg.replace('+', '').replace('#', '') == alg:
            return move
    
    return None


def move_to_simple_algebraic(board: Board, move: tuple) -> str:
    """
    Convert internal move to simplified algebraic notation for matching.
    """
    from_sq, to_sq = move[0], move[1]
    piece = board.board_play[from_sq]
    captured = board.board_play[to_sq]
    
    to_alg = index_to_algebraic(to_sq)
    from_alg = index_to_algebraic(from_sq)
    
    # Pawn moves
    if piece in 'Pp':
        if captured != 0:
            # Pawn capture
            return f"{from_alg[0]}x{to_alg}"
        else:
            return to_alg
    
    # Piece moves
    piece_char = piece.upper()
    capture_char = 'x' if captured != 0 else ''
    
    # Simple format: piece + [capture] + destination
    return f"{piece_char}{capture_char}{to_alg}"


def run_lct2_test(depth=5, verbose=True):
    """
    Run the LCT II test suite.
    
    Args:
        depth: Search depth for each position
        verbose: Print details for each position
    
    Returns:
        Number of positions solved correctly
    """
    solved = 0
    total = len(LCT2_POSITIONS)
    position_points = 0
    
    if verbose:
        print(f"Running LCT II Test Suite (depth={depth})")
        print("=" * 60)
    
    for pos in LCT2_POSITIONS:
        board = Board()
        fen_to_board(board, pos["fen"])
        
        # Search for best move
        start_time = time.time()
        best_move, eval_score, _ = search(board, depth)
        elapsed = time.time() - start_time
        
        if best_move is None:
            if verbose:
                print(f"Position {pos['id']:2d}: FAILED - No legal moves found")
            continue
        
        # Convert move to algebraic
        move_alg = move_to_simple_algebraic(board, best_move)
        
        # Check if it matches any of the best moves
        correct = False
        for expected in pos["best_moves"]:
            # Try to match the expected move
            expected_move = algebraic_to_move(board, expected)
            if expected_move and expected_move == best_move:
                correct = True
                break
            # Also try simple string matching
            if move_alg.replace('+', '').replace('#', '') == expected.replace('+', '').replace('#', ''):
                correct = True
                break
        
        # Check if move is in avoid list
        if correct and "avoid_moves" in pos:
            for avoid in pos["avoid_moves"]:
                avoid_move = algebraic_to_move(board, avoid)
                if avoid_move and avoid_move == best_move:
                    correct = False
                    break
                if move_alg.replace('+', '').replace('#', '') == avoid.replace('+', '').replace('#', ''):
                    correct = False
                    break
        
        points = points_for_position(correct, elapsed)
        position_points += points

        if correct:
            solved += 1
            if verbose:
                print(
                    f"Position {pos['id']:2d}: PASS - Found {move_alg} "
                    f"(eval: {eval_score}, time: {elapsed:.2f}s, points: {points})"
                )
        else:
            if verbose:
                expected_str = '/'.join(pos["best_moves"])
                print(
                    f"Position {pos['id']:2d}: FAIL - Found {move_alg}, expected {expected_str} "
                    f"(eval: {eval_score}, time: {elapsed:.2f}s, points: {points})"
                )
    
    total_points = BASE_SCORE + position_points
    max_points = BASE_SCORE + len(LCT2_POSITIONS) * MAX_PER_POSITION

    if verbose:
        print("=" * 60)
        print(f"Result: {solved}/{total} positions solved ({100*solved/total:.1f}%)")
        print(
            f"Score: {total_points} (base {BASE_SCORE} + position points {position_points}); "
            f"max {max_points}"
        )
    
    return solved


if __name__ == "__main__":
    import sys
    
    # Default depth
    depth = 5
    
    # Check for command line argument
    if len(sys.argv) > 1:
        try:
            depth = int(sys.argv[1])
        except ValueError:
            print(f"Invalid depth: {sys.argv[1]}, using default depth 5")
    
    run_lct2_test(depth=depth, verbose=True)
