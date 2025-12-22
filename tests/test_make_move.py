from board import Board
from fen import fen_to_board
from make_move import make_move, unmake_move


def test_make_unmake_move_restores_board():
    b = Board()
    fen_to_board(b, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    # pick the first legal move and ensure restoration
    from move_gen import generate_legal_moves
    moves = generate_legal_moves(b)
    assert moves
    move = moves[0]

    # snapshot
    board_snapshot = list(b.board_play)
    piece_list_snapshot = {k: list(v) for k, v in b.piece_list.items()}

    undo = make_move(b, move)
    # ensure something changed
    assert b.board_play != board_snapshot or b.piece_list != piece_list_snapshot

    unmake_move(b, undo)
    assert b.board_play == board_snapshot
    assert all(sorted(b.piece_list[k]) == sorted(piece_list_snapshot[k]) for k in b.piece_list)
