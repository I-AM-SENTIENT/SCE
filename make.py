#Make/Unmake Move
from board import Board

def make_move(board: Board, move: tuple) -> dict:
    """Apply move and return undo info."""
    from_sq, to_sq = move
    piece = board.board_play[from_sq]
    captured = board.board_play[to_sq]
    
    #Save state for undo
    undo = {
        'from_sq': from_sq,
        'to_sq': to_sq,
        'piece': piece,
        'captured': captured,
        'castle_ws': board.castle_white_short,
        'castle_wl': board.castle_white_long,
        'castle_bs': board.castle_black_short,
        'castle_bl': board.castle_black_long,
        'en_passant': board.en_passant,
        'half_move': board.half_move_counter,
    }
    
    #Move the piece
    board.board_play[to_sq] = piece
    board.board_play[from_sq] = 0
    
    #Handle castling (move rook)
    if piece in ('K', 'k'):
        if from_sq == 95 and to_sq == 97:  # White short
            board.board_play[98], board.board_play[96] = 0, 'R'
        elif from_sq == 95 and to_sq == 93:  # White long
            board.board_play[91], board.board_play[94] = 0, 'R'
        elif from_sq == 25 and to_sq == 27:  # Black short
            board.board_play[28], board.board_play[26] = 0, 'r'
        elif from_sq == 25 and to_sq == 23:  # Black long
            board.board_play[21], board.board_play[24] = 0, 'r'
    
    #Handle en passant capture
    if piece in ('P', 'p') and board.en_passant:
        ep_idx = board.en_passant_to_index()
        if to_sq == ep_idx:
            captured_pawn_sq = to_sq + (10 if piece == 'P' else -10)
            undo['ep_captured_sq'] = captured_pawn_sq
            undo['ep_captured'] = board.board_play[captured_pawn_sq]
            board.board_play[captured_pawn_sq] = 0
    
    #Update en passant square
    board.en_passant = None
    if piece in ('P', 'p') and abs(to_sq - from_sq) == 20:
        ep_sq = (from_sq + to_sq) // 2
        file_letter = chr(ord('a') + (ep_sq % 10) - 1)
        rank = 8 - ((ep_sq // 10) - 2)
        board.en_passant = f"{file_letter}{rank}"
    
    #Update castling rights
    if piece == 'K':
        board.castle_white_short = board.castle_white_long = 0
    if piece == 'k':
        board.castle_black_short = board.castle_black_long = 0
    if from_sq == 98 or to_sq == 98: board.castle_white_short = 0
    if from_sq == 91 or to_sq == 91: board.castle_white_long = 0
    if from_sq == 28 or to_sq == 28: board.castle_black_short = 0
    if from_sq == 21 or to_sq == 21: board.castle_black_long = 0
    
    # Update half-move counter: reset if pawn move or capture, else increment
    if piece in ('P', 'p') or captured != 0 or (
        piece in ('P', 'p') and board.en_passant and to_sq == board.en_passant_to_index()
    ):
        board.half_move_counter = 0
    else:
        board.half_move_counter += 1
    board.side_to_move = 1 - board.side_to_move
    board.update_piece_list()
    return undo

def undo_move(board: Board, undo: dict):
    """Revert a move using undo info."""
    board.board_play[undo['from_sq']] = undo['piece']
    board.board_play[undo['to_sq']] = undo['captured']
    
    # Restore en passant captured pawn
    if 'ep_captured_sq' in undo:
        board.board_play[undo['ep_captured_sq']] = undo['ep_captured']
    
    # Restore castling rook
    # (reverse of make_move castling logic)
    if undo['piece'] in ('K', 'k'):
        # White short castle
        if undo['from_sq'] == 95 and undo['to_sq'] == 97:
            board.board_play[98], board.board_play[96] = 'R', 0
        # White long castle
        elif undo['from_sq'] == 95 and undo['to_sq'] == 93:
            board.board_play[91], board.board_play[94] = 'R', 0
        # Black short castle
        elif undo['from_sq'] == 25 and undo['to_sq'] == 27:
            board.board_play[28], board.board_play[26] = 'r', 0
        # Black long castle
        elif undo['from_sq'] == 25 and undo['to_sq'] == 23:
            board.board_play[21], board.board_play[24] = 'r', 0
    
    board.castle_white_short = undo['castle_ws']
    board.castle_white_long = undo['castle_wl']
    board.castle_black_short = undo['castle_bs']
    board.castle_black_long = undo['castle_bl']
    board.en_passant = undo['en_passant']
    board.half_move_counter = undo['half_move']
    board.side_to_move = 1 - board.side_to_move
    board.update_piece_list()