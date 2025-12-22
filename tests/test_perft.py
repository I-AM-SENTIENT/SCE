import pytest
from perft import perft
from constants import PERFT_RESULTS
from fen import fen_to_board
from board import Board

# Limit perft tests to small depths for CI speed
POSITIONS = [
    list(PERFT_RESULTS.keys())[0],  # STARTING_FEN
    list(PERFT_RESULTS.keys())[1],  # KIWIPETE_FEN
    list(PERFT_RESULTS.keys())[2],  # POS3_FEN
]


@pytest.mark.parametrize("fen", POSITIONS)
def test_perft_depths_1_to_3(fen):
    b = Board()
    fen_to_board(b, fen)
    expected = PERFT_RESULTS[fen]
    max_depth = min(3, len(expected))
    for depth in range(1, max_depth + 1):
        result = perft(b, depth)
        assert result == expected[depth - 1]
