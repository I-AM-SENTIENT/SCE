from board import Board
from constants import PIECES

def fen_to_board(board: Board, fen: str):
    parts = fen.split()
    if not parts:
        raise ValueError("Empty FEN")

    placement = parts[0]
    rows = placement.split('/')
    if len(rows) != 8:
        raise ValueError("FEN must have 8 ranks")

    board.board_play = [0] * 120
    index = 0  #0..63 index into mailbox64
    for row in rows:
        for char in row:
            if char.isdigit():
                index += int(char)
            elif char in PIECES:
                if index < 0 or index >= 64:
                    raise ValueError("Piece index out of range while parsing FEN")
                sq120 = board.mailbox64[index]
                board.board_play[sq120] = char
                index += 1
            else:
                raise ValueError('Invalid character in FEN piece placement')

    #side to move
    if len(parts) > 1:
        if parts[1] == 'w':
            board.side_to_move = 0
        elif parts[1] == 'b':
            board.side_to_move = 1
        else:
            raise ValueError("Invalid side to move in FEN")
    else:
        board.side_to_move = 0

    #castling
    castling = parts[2] if len(parts) > 2 else '-'
    board.castle_white_short = 1 if 'K' in castling else 0
    board.castle_white_long = 1 if 'Q' in castling else 0
    board.castle_black_short = 1 if 'k' in castling else 0
    board.castle_black_long = 1 if 'q' in castling else 0

    #en passant
    en_passant = parts[3] if len(parts) > 3 else '-'
    board.en_passant = None if en_passant == '-' else en_passant

    #halfmove clock
    board.half_move_counter = int(parts[4]) if len(parts) > 4 else 0

    #fullmove number
    board.full_move_counter = int(parts[5]) if len(parts) > 5 else 1

    board.update_piece_list()


def board_to_fen(board: Board) -> str:
    ranks = []
    for r in range(8):
        empty = 0
        parts = []
        for c in range(8):
            idx64 = r * 8 + c
            sq120 = board.mailbox64[idx64]
            piece = board.board_play[sq120]
            if piece == 0:
                empty += 1
            else:
                if empty:
                    parts.append(str(empty))
                    empty = 0
                parts.append(str(piece))
        if empty:
            parts.append(str(empty))
        ranks.append(''.join(parts))

    placement = '/'.join(ranks)
    side = 'w' if board.side_to_move == 0 else 'b'

    castling = ''
    if board.castle_white_short:
        castling += 'K'
    if board.castle_white_long:
        castling += 'Q'
    if board.castle_black_short:
        castling += 'k'
    if board.castle_black_long:
        castling += 'q'
    if castling == '':
        castling = '-'

    en_pass = board.en_passant if board.en_passant is not None else '-'

    return f"{placement} {side} {castling} {en_pass} {board.half_move_counter} {board.full_move_counter}"