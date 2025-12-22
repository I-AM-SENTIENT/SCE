"""Standalone perft check script intended for CI.
Exits with non-zero status if any perft count mismatches expected results.
Runs only shallow depths for speed.
"""
import sys
from perft import perft
from constants import PERFT_RESULTS
from fen import fen_to_board
from board import Board

POSITIONS = list(PERFT_RESULTS.keys())[:3]
MAX_DEPTH = 3

errors = 0
for fen in POSITIONS:
    b = Board()
    fen_to_board(b, fen)
    expected = PERFT_RESULTS[fen]
    for depth in range(1, min(MAX_DEPTH, len(expected)) + 1):
        result = perft(b, depth)
        if result != expected[depth - 1]:
            print(f"Mismatch for fen={fen[:30]}... depth={depth}: got {result}, expected {expected[depth-1]}")
            errors += 1
        else:
            print(f"OK: depth {depth} = {result}")

if errors:
    sys.exit(2)
else:
    print("All perft checks passed.")
    sys.exit(0)
