from board import Board
from constants import QUEEN_OFFSET,KING_OFFSET,BISHOP_OFFSET,KNIGHT_OFFSET,ROOK_OFFSET,ROW_2,ROW_7,ROW_5,ROW_4,ROW_8,ROW_1
from make_move import make_move, unmake_move


def knight_gen(board: Board, hostile: set) -> list: 
    """Generate a list of moves for knights"""
    moves = []
    if board.side_to_move == 0:
        knight = 'N'
    elif board.side_to_move == 1:
        knight = 'n'
    
    #We get the indices where are knights are from piecelist
    knight_indices = board.piece_list[knight]
    #We go to each piece
    for knight_pos in knight_indices:
        #We move over each offset
        for offset in KNIGHT_OFFSET:
            #Check if the square is in bounds
            if board.mailbox120[knight_pos + offset] != -1:
            #If the target square is empty or hostile we add the move
                if board.board_play[knight_pos + offset] == 0 or board.board_play[knight_pos + offset] in hostile:
                    moves.append((knight_pos, knight_pos + offset))
    return moves
            
def bishop_gen(board: Board, hostile: set) -> list:
    """Generate a list of moves for bishops"""
    moves = []
    if board.side_to_move == 0:
        bishop = 'B'
    elif board.side_to_move == 1:
        bishop = 'b'
    bishop_indices = board.piece_list[bishop]

    for start in bishop_indices:
        for offset in BISHOP_OFFSET:
            target = start + offset
            #We need to go until we are out of bounds or we find hostile(inclusive) piece or friendly(exclusive)
            while board.mailbox120[target] != -1:
                piece = board.board_play[target]
                if piece == 0:
                    #Empty square - add move and continue sliding
                    moves.append((start, target))
                    target += offset
                elif piece in hostile:
                    #Capture - add move and stop
                    moves.append((start, target))
                    break
                else:
                    #Friendly piece - stop
                    break
    return moves

def rook_gen(board: Board, hostile: set)-> list:
    '''Generate a list of moves for rooks'''
    moves = []
    if board.side_to_move == 0:
        rook = 'R'
    elif board.side_to_move == 1:
        rook = 'r'
    rook_indices = board.piece_list[rook]

    for start in rook_indices:
        for offset in ROOK_OFFSET:
            target = start + offset
            #Same as bishop
            while board.mailbox120[target] != -1:
                piece = board.board_play[target]
                if piece == 0:
                    #Empty square - add move and continue sliding
                    moves.append((start, target))
                    target += offset
                elif piece in hostile:
                    #Capture - add move and stop
                    moves.append((start, target))
                    break
                else:
                    #Friendly piece - stop
                    break
    return moves

def queen_gen(board: Board, hostile: set)-> list:
    '''Generate a list of moves for queen'''
    moves = []
    #Same as rook or bishop
    if board.side_to_move == 0:
        queen = 'Q'
    elif board.side_to_move == 1:
        queen = 'q'
    queen_indices = board.piece_list[queen]

    for start in queen_indices:
        for offset in QUEEN_OFFSET:
            target = start + offset
            #Same as rook or bishop
            while board.mailbox120[target] != -1:
                piece = board.board_play[target]
                if piece == 0:
                    #Empty square - add move and continue sliding
                    moves.append((start, target))
                    target += offset
                elif piece in hostile:
                    #Capture - add move and stop
                    moves.append((start, target))
                    break
                else:
                    #Friendly piece - stop
                    break
    return moves

def king_gen(board: Board, hostile: set)-> list:
    """Generate a list of moves for a king"""
    moves = []
    if board.side_to_move == 0:
        king = 'K'
    elif board.side_to_move == 1:
        king = 'k'
    king_indices = board.piece_list[king]

    #We start the same with capture/move moves
    for king_pos in king_indices:
        for offset in KING_OFFSET:
            if board.mailbox120[king_pos+offset] != -1:
                if board.board_play[king_pos + offset] == 0 or board.board_play[king_pos + offset] in hostile:
                    moves.append((king_pos, king_pos + offset))
    #Now we need castling
    #We check board info if castling allowed at all or already not
    if board.side_to_move == 0:
        if board.castle_white_short:
            if board.board_play[96] == 0 and board.board_play[97] == 0 and is_square_attacked(board,95,1) == False and is_square_attacked(board,96,1) == False and is_square_attacked(board,97,1) == False:
                #King moves from e1 to g1
                moves.append((95,97,'castle_short'))
                #We add 'castle_x' flag to the tuple so that we can later move a rook when castling
        if board.castle_white_long:
            if board.board_play[92] == 0 and board.board_play[93] == 0 and board.board_play[94] == 0 and is_square_attacked(board,95,1) == False and is_square_attacked(board,94,1) == False and is_square_attacked(board,93,1) == False:
                #King moves from e1 to c1
                moves.append((95,93,'castle_long'))
    if board.side_to_move == 1:
        if board.castle_black_short:
            if board.board_play[26] == 0 and board.board_play[27] == 0 and is_square_attacked(board,25,0) == False and is_square_attacked(board,26,0) == False and is_square_attacked(board,27,0) == False:
                #King moves from e8 to g8
                moves.append((25,27,'castle_short'))
        if board.castle_black_long:
            if board.board_play[22] == 0 and board.board_play[23] == 0 and board.board_play[24] == 0 and is_square_attacked(board,25,0) == False and is_square_attacked(board,24,0) == False and is_square_attacked(board,23,0) == False:
                #King moves from e8 to c8
                moves.append((25,23,'castle_long'))
    return moves

def pawn_gen(board: Board, hostile: set) -> list:
    '''Generate pawn moves'''
    moves = []
    
    if board.side_to_move == 0:  #White
        pawn = 'P'
        forward = -10
        start_row = ROW_2
        passant_row = ROW_5
        promo_row = ROW_8
        capture_offsets = [-9, -11]
    else:  #Black
        pawn = 'p'
        forward = 10
        start_row = ROW_7
        passant_row = ROW_4
        promo_row = ROW_1
        capture_offsets = [9, 11]
    
    pawn_indexs = board.piece_list[pawn]
    ep_target = board.en_passant_to_index() if board.en_passant else -1
    
    for x in pawn_indexs:
        #Single push
        target = x + forward
        if board.mailbox120[target] != -1 and board.board_play[target] == 0:
            if target in promo_row:
                # Promotion moves
                moves.append((x, target, 'promo_q'))
                moves.append((x, target, 'promo_r'))
                moves.append((x, target, 'promo_b'))
                moves.append((x, target, 'promo_n'))
            else:
                moves.append((x, target))
            
            #Double push (only if single push was valid and on starting row)
            if x in start_row:
                target2 = x + forward * 2
                if board.board_play[target2] == 0:
                    moves.append((x, target2, 'double'))
        
        #Captures (including en passant)
        for offset in capture_offsets:
            target = x + offset
            if board.mailbox120[target] == -1:
                continue
            
            piece_at_target = board.board_play[target]
            is_capture = piece_at_target in hostile
            is_en_passant = (x in passant_row and target == ep_target)
            
            if is_capture or is_en_passant:
                if target in promo_row:
                    moves.append((x, target, 'promo_q'))
                    moves.append((x, target, 'promo_r'))
                    moves.append((x, target, 'promo_b'))
                    moves.append((x, target, 'promo_n'))
                elif is_en_passant:
                    moves.append((x, target, 'en_passant'))
                else:
                    moves.append((x, target))
    
    return moves

def is_square_attacked(board:Board,square:int,side:int)->bool:
    '''Check if a square is attacked by the GIVEN side'''
    
    #Pawn attacks
    if side == 0:
        pawn_offsets = [9, 11]  #Look below for white pawns
        pawn = 'P'
    else:
        pawn_offsets = [-9, -11]  #Look above for black pawns
        pawn = 'p'
    for offset in pawn_offsets:
        target = square + offset
        if board.mailbox120[target] != -1:
            if board.board_play[target] == pawn:
                return True
    
    #Knight attacks
    knight = 'N' if side == 0 else 'n'
    for offset in KNIGHT_OFFSET:
        target = square + offset
        if board.mailbox120[target] != -1:
            if board.board_play[target] == knight:
                return True
    
    #Bishop/Queen attacks (diagonal)
    bishop = 'B' if side == 0 else 'b'
    queen = 'Q' if side == 0 else 'q'
    for offset in BISHOP_OFFSET:
        target = square + offset
        while board.mailbox120[target] != -1:
            piece = board.board_play[target]
            if piece == 0:
                target += offset
            elif piece == bishop or piece == queen:
                return True
            else:
                break  #Any other piece blocks
    
    #Rook/Queen attacks (orthogonal)
    rook = 'R' if side == 0 else 'r'
    for offset in ROOK_OFFSET:
        target = square + offset
        while board.mailbox120[target] != -1:
            piece = board.board_play[target]
            if piece == 0:
                target += offset
            elif piece == rook or piece == queen:
                return True
            else:
                break  #Any other piece blocks
    
    #King attacks
    king = 'K' if side == 0 else 'k'
    for offset in KING_OFFSET:
        target = square + offset
        if board.mailbox120[target] != -1:
            if board.board_play[target] == king:
                return True
    
    return False

def generate_moves(board: Board) -> list:
    """Generates all pseudo-legal moves for the side to move"""
    #Pre-compute hostile pieces once
    if board.side_to_move == 0:
        hostile = {'p','n','b','r','q','k'}
    else:
        hostile = {'P','N','B','R','Q','K'}
    
    moves = []
    moves.extend(pawn_gen(board, hostile))
    moves.extend(knight_gen(board, hostile))
    moves.extend(bishop_gen(board, hostile))
    moves.extend(rook_gen(board, hostile))
    moves.extend(queen_gen(board, hostile))
    moves.extend(king_gen(board, hostile))
    return moves

def generate_legal_moves(board: Board)-> list:
    """Generate legal moves(filter out the illegal ones)"""
    pseudo_moves = generate_moves(board)
    legal_moves = []
    for move in pseudo_moves:
        undo = make_move(board, move)
        
        #Find our king and check if it's attacked
        #After make_move, side_to_move has switched, so:
        #If we were white (0), now it's black's turn (1), our king is 'K'
        #If we were black (1), now it's white's turn (0), our king is 'k'
        king = 'K' if board.side_to_move == 1 else 'k'
        king_positions = board.piece_list[king]
        
        #Check if king still exists (shouldn't be captured in legal position)
        if king_positions:
            king_sq = king_positions[0]
            #Check if opponent (current side_to_move) is attacking our king
            if not is_square_attacked(board, king_sq, board.side_to_move):
                legal_moves.append(move)
        
        unmake_move(board, undo)
    
    return legal_moves