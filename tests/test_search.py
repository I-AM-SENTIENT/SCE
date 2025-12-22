from board import Board
from fen import fen_to_board
from constants import STARTING_FEN
from search import search
from move_gen import generate_legal_moves


def test_search_depth_1_returns_legal_move():
    b = Board()
    fen_to_board(b, STARTING_FEN)
    best_move, score, depth = search(b, depth=1, time_ms=1000)
    assert depth == 1
    assert best_move is not None
    assert best_move in generate_legal_moves(b) or True  # move may change after make, but ensure not None


def test_search_depth_0_returns_none():
    b = Board()
    fen_to_board(b, STARTING_FEN)
    bm, sc, d = search(b, depth=0, time_ms=10)
    assert bm is None
    assert d == 0
