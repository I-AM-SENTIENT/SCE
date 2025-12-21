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
    
    board_play = board.board_play
    piece_list = board.piece_list

    piece = board_play[from_sq]  #Get the piece being moved
    captured = board_play[to_sq]  #Get the piece being captured (0 if none)

    #Handle en passant capture
    if flag == 'en_passant':
        if board.side_to_move == 0:  #White captures black pawn
            captured_pawn_sq = to_sq + 10
        else:  #Black captures white pawn
            captured_pawn_sq = to_sq - 10
        undo['en_passant_captured_sq'] = captured_pawn_sq
        undo['en_passant_captured_piece'] = board_play[captured_pawn_sq]
        piece_list[board_play[captured_pawn_sq]].remove(captured_pawn_sq)
        board_play[captured_pawn_sq] = 0

    #Remove moving and captured pieces from lists
    piece_list[piece].remove(from_sq)
    if captured != 0:
        piece_list[captured].remove(to_sq)

    #Move the piece
    board_play[from_sq] = 0
    final_piece = piece

    #Handle promotion
    if flag in ('promo_q', 'promo_r', 'promo_b', 'promo_n'):
        promo_pieces = {
            'promo_q': 'Q' if board.side_to_move == 0 else 'q',
            'promo_r': 'R' if board.side_to_move == 0 else 'r',
            'promo_b': 'B' if board.side_to_move == 0 else 'b',
            'promo_n': 'N' if board.side_to_move == 0 else 'n',
        }
        final_piece = promo_pieces[flag]

    board_play[to_sq] = final_piece
    piece_list[final_piece].append(to_sq)

    #Handle castling - move the rook and lists
    if flag == 'castle_short':
        if board.side_to_move == 0:  #White
            rook_from, rook_to, rook_piece = 98, 96, 'R'
        else:  #Black
            rook_from, rook_to, rook_piece = 28, 26, 'r'
        piece_list[rook_piece].remove(rook_from)
        board_play[rook_to] = board_play[rook_from]  #Rook f file
        board_play[rook_from] = 0
        piece_list[rook_piece].append(rook_to)
    elif flag == 'castle_long':
        if board.side_to_move == 0:  #White
            rook_from, rook_to, rook_piece = 91, 94, 'R'
        else:  #Black
            rook_from, rook_to, rook_piece = 21, 24, 'r'
        piece_list[rook_piece].remove(rook_from)
        board_play[rook_to] = board_play[rook_from]  #Rook d file
        board_play[rook_from] = 0
        piece_list[rook_piece].append(rook_to)
    
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
    
    return undo


def unmake_move(board: Board, undo: dict):
    """Undo a move using the undo info from make_move."""
    from_sq = undo['from_sq']
    to_sq = undo['to_sq']
    flag = undo['flag']
    
    board_play = board.board_play
    piece_list = board.piece_list

    #Switch side back
    board.side_to_move = 1 - board.side_to_move

    moved_piece = undo['moved_piece']
    captured_piece = undo['captured_piece']

    #Remove the piece that currently sits on the destination square
    current_piece = board_play[to_sq]
    if current_piece != 0:
        piece_list[current_piece].remove(to_sq)
    board_play[to_sq] = 0

    #Handle castling - move rook back
    if flag == 'castle_short':
        if board.side_to_move == 0:  #White
            rook_from, rook_to, rook_piece = 96, 98, 'R'
        else:  #Black
            rook_from, rook_to, rook_piece = 26, 28, 'r'
        piece_list[rook_piece].remove(rook_from)
        board_play[rook_to] = board_play[rook_from]
        board_play[rook_from] = 0
        piece_list[rook_piece].append(rook_to)
    elif flag == 'castle_long':
        if board.side_to_move == 0:  #White
            rook_from, rook_to, rook_piece = 94, 91, 'R'
        else:  #Black
            rook_from, rook_to, rook_piece = 24, 21, 'r'
        piece_list[rook_piece].remove(rook_from)
        board_play[rook_to] = board_play[rook_from]
        board_play[rook_from] = 0
        piece_list[rook_piece].append(rook_to)

    #Restore the moved piece
    board_play[from_sq] = moved_piece
    piece_list[moved_piece].append(from_sq)

    #Restore captured piece on destination square
    board_play[to_sq] = captured_piece
    if captured_piece != 0:
        piece_list[captured_piece].append(to_sq)

    #Handle en passant - restore captured pawn
    if flag == 'en_passant':
        captured_sq = undo['en_passant_captured_sq']
        captured_pawn = undo['en_passant_captured_piece']
        board_play[captured_sq] = captured_pawn
        piece_list[captured_pawn].append(captured_sq)

    #Restore board state
    board.castle_white_short = undo['castle_white_short']
    board.castle_white_long = undo['castle_white_long']
    board.castle_black_short = undo['castle_black_short']
    board.castle_black_long = undo['castle_black_long']
    board.en_passant = undo['en_passant']
    board.half_move_counter = undo['half_move_counter']
    board.full_move_counter = undo['full_move_counter']