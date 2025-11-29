from board import Board

def make_move(board: Board, move: tuple) -> dict:
    """
    Make a move on the board. Returns undo info for unmake_move.
    Move format: (from_sq, to_sq) or (from_sq, to_sq, flag)
    """
    from_sq = move[0]
    to_sq = move[1]
    flag = move[2] if len(move) > 2 else None
    
    #Store undo information
    undo = {
        'from_sq': from_sq,
        'to_sq': to_sq,
        'flag': flag,
        'moved_piece': board.board_play[from_sq],
        'captured_piece': board.board_play[to_sq],
        'castle_white_short': board.castle_white_short,
        'castle_white_long': board.castle_white_long,
        'castle_black_short': board.castle_black_short,
        'castle_black_long': board.castle_black_long,
        'en_passant': board.en_passant,
        'half_move_counter': board.half_move_counter,
        'full_move_counter': board.full_move_counter,
    }
    
    piece = board.board_play[from_sq] #Get the piece being moved
    captured = board.board_play[to_sq] #Get the piece being captured (0 if none)


    #We need to handle flag moves
    #Handle en passant capture
    if flag == 'en_passant':
        if board.side_to_move == 0:  #White captures black pawn
            captured_pawn_sq = to_sq + 10
        else:  #Black captures white pawn
            captured_pawn_sq = to_sq - 10
        undo['en_passant_captured_sq'] = captured_pawn_sq
        undo['en_passant_captured_piece'] = board.board_play[captured_pawn_sq]
        board.board_play[captured_pawn_sq] = 0
    
    #Move the piece
    board.board_play[to_sq] = piece
    board.board_play[from_sq] = 0
    
    #Handle promotion
    if flag in ('promo_q', 'promo_r', 'promo_b', 'promo_n'):
        promo_pieces = {
            'promo_q': 'Q' if board.side_to_move == 0 else 'q',
            'promo_r': 'R' if board.side_to_move == 0 else 'r',
            'promo_b': 'B' if board.side_to_move == 0 else 'b',
            'promo_n': 'N' if board.side_to_move == 0 else 'n',
        }
        board.board_play[to_sq] = promo_pieces[flag]
    
    #Handle castling - move the rook
    if flag == 'castle_short':
        if board.side_to_move == 0:  #White
            board.board_play[96] = board.board_play[98]  #Rook f1 <- h1
            board.board_play[98] = 0
        else:  #Black
            board.board_play[26] = board.board_play[28]  #Rook f8 <- h8
            board.board_play[28] = 0
    elif flag == 'castle_long':
        if board.side_to_move == 0:  #White
            board.board_play[94] = board.board_play[91]  #Rook d1 <- a1
            board.board_play[91] = 0
        else:  #Black
            board.board_play[24] = board.board_play[21]  #Rook d8 <- a8
            board.board_play[21] = 0
    
    #Update en passant square
    if flag == 'double':
        if board.side_to_move == 0:  #White double push
            file = (from_sq % 10) - 1  #Convert to 0-7
            board.en_passant = chr(ord('a') + file) + '3'
        else:  #Black double push
            file = (from_sq % 10) - 1
            board.en_passant = chr(ord('a') + file) + '6'
    else:
        board.en_passant = None
    
    #Update castling rights
    #King moves
    if piece == 'K':
        board.castle_white_short = 0
        board.castle_white_long = 0
    elif piece == 'k':
        board.castle_black_short = 0
        board.castle_black_long = 0
    #Rook moves or captured
    if from_sq == 98 or to_sq == 98:  #h1
        board.castle_white_short = 0
    if from_sq == 91 or to_sq == 91:  #a1
        board.castle_white_long = 0
    if from_sq == 28 or to_sq == 28:  #h8
        board.castle_black_short = 0
    if from_sq == 21 or to_sq == 21:  #a8
        board.castle_black_long = 0
    
    #Update halfmove clock
    if piece in ('P', 'p') or captured != 0:
        board.half_move_counter = 0
    else:
        board.half_move_counter += 1
    
    #Update fullmove counter
    if board.side_to_move == 1:
        board.full_move_counter += 1
    
    #Switch side
    board.side_to_move = 1 - board.side_to_move
    
    #Update piece list
    board.update_piece_list()
    
    return undo


def unmake_move(board: Board, undo: dict):
    """Undo a move using the undo info from make_move."""
    from_sq = undo['from_sq']
    to_sq = undo['to_sq']
    flag = undo['flag']
    
    #Switch side back
    board.side_to_move = 1 - board.side_to_move
    
    #Restore the moved piece
    board.board_play[from_sq] = undo['moved_piece']
    board.board_play[to_sq] = undo['captured_piece']
    
    #Handle en passant - restore captured pawn
    if flag == 'en_passant':
        board.board_play[undo['en_passant_captured_sq']] = undo['en_passant_captured_piece']
    
    #Handle castling - move rook back
    if flag == 'castle_short':
        if board.side_to_move == 0:  #White
            board.board_play[98] = board.board_play[96]
            board.board_play[96] = 0
        else:  #Black
            board.board_play[28] = board.board_play[26]
            board.board_play[26] = 0
    elif flag == 'castle_long':
        if board.side_to_move == 0:  #White
            board.board_play[91] = board.board_play[94]
            board.board_play[94] = 0
        else:  #Black
            board.board_play[21] = board.board_play[24]
            board.board_play[24] = 0
    
    #Restore board state
    board.castle_white_short = undo['castle_white_short']
    board.castle_white_long = undo['castle_white_long']
    board.castle_black_short = undo['castle_black_short']
    board.castle_black_long = undo['castle_black_long']
    board.en_passant = undo['en_passant']
    board.half_move_counter = undo['half_move_counter']
    board.full_move_counter = undo['full_move_counter']
    
    #Update piece list
    board.update_piece_list()