from board import Board
from fen import fen_to_board
from uci import parse_go
from constants import STARTING_FEN


def test_uci_go_depth2_smoke():
    b = Board()
    fen_to_board(b, STARTING_FEN)
    best = parse_go(b, ['depth', '2'])
    assert best is not None


def test_uci_go_movetime_smoke():
    b = Board()
    fen_to_board(b, STARTING_FEN)
    best = parse_go(b, ['movetime', '200'])
    assert best is not None
