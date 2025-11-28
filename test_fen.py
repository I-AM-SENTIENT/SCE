# python
from fen import fen_to_board, board_to_fen
from board import Board
from constants import STARTING_FEN
import pytest # type: ignore

def test_starting_fen_roundtrip():
    board = Board()
    fen_to_board(board, STARTING_FEN)
    assert board_to_fen(board) == STARTING_FEN

def test_empty_fen_raises():
    board = Board()
    with pytest.raises(ValueError):
        fen_to_board(board, "")

def test_invalid_character_in_fen_raises():
    board = Board()
    bad_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNX w KQkq - 0 1"
    with pytest.raises(ValueError):
        fen_to_board(board, bad_fen)

def test_invalid_side_in_fen_raises():
    board = Board()
    bad_fen = "8/8/8/8/8/8/8/8 c - - 0 1"
    with pytest.raises(ValueError):
        fen_to_board(board, bad_fen)

def test_castling_en_passant_and_counters_parsed():
    board = Board()
    fen = "8/8/8/8/8/8/8/8 b Kq a3 3 4"
    fen_to_board(board, fen)
    assert board.side_to_move == 1
    assert board.castle_white_short == 1
    assert board.castle_white_long == 0
    assert board.castle_black_short == 0
    assert board.castle_black_long == 1
    assert board.en_passant == "a3"
    assert board.half_move_counter == 3
    assert board.full_move_counter == 4
    assert board_to_fen(board) == fen