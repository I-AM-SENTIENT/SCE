import pytest
from board import Board
from fen import fen_to_board, board_to_fen
from constants import STARTING_FEN


def test_starting_fen_roundtrip():
    b = Board()
    fen_to_board(b, STARTING_FEN)
    out = board_to_fen(b)
    assert out == STARTING_FEN


def test_invalid_fen_raises():
    b = Board()
    with pytest.raises(ValueError):
        fen_to_board(b, "")
    with pytest.raises(ValueError):
        fen_to_board(b, "8/8/8/8/8/8/8 w - -")
