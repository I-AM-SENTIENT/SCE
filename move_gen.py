# Pseudo legal moves generation
from board import Board
from constants import QUEEN_OFFSET, KING_OFFSET, BISHOP_OFFSET, KNIGHT_OFFSET, ROOK_OFFSET, PAWN_OFFSET_WHITE, PAWN_OFFSET_BLACK



def generate_knight_moves(board: Board) -> list:
    # Store our moves
    moves = []
    knight = 'N' if board.side_to_move == 0 else 'n' # Get correct knight symbol
    for sq120 in board.piece_list[knight]:
        for offset in KNIGHT_OFFSET: # All possible knight moves
            target_sq = sq120 + offset
            if board.mailbox120[target_sq] != -1:  # Ensure target square is within bounds
                target_piece = board.board_play[target_sq]
                if (
                    target_piece == 0 or
                    (board.side_to_move == 0 and isinstance(target_piece, str) and target_piece.islower()) or
                    (board.side_to_move == 1 and isinstance(target_piece, str) and target_piece.isupper())
                ):
                    moves.append((sq120, target_sq))
    return moves

def generate_rook_moves(board: Board) -> list:
    moves = []
    rook = 'R' if board.side_to_move == 0 else 'r'
    for sq120 in board.piece_list[rook]:
        for offset in ROOK_OFFSET:
            target_sq = sq120 + offset
            # Ensure target square is within bounds
            if board.mailbox120[target_sq] != -1:
                while board.board_play[target_sq] == 0:
                    moves.append((sq120, target_sq))
                    target_sq += offset
                    if board.mailbox120[target_sq] == -1:
                        break
                if board.mailbox120[target_sq] != -1:
                    target_piece = board.board_play[target_sq]
                    if (
                        (board.side_to_move == 0 and isinstance(target_piece, str) and target_piece.islower()) or
                        (board.side_to_move == 1 and isinstance(target_piece, str) and target_piece.isupper())
                    ):
                        moves.append((sq120, target_sq))
    return moves

def generate_bishop_moves(board: Board) -> list:
    moves = []
    bishop = 'B' if board.side_to_move == 0 else 'b'
    for sq120 in board.piece_list[bishop]:
        for offset in BISHOP_OFFSET:
            target_sq = sq120 + offset
            if board.mailbox120[target_sq] != -1:
                while board.board_play[target_sq] == 0:
                    moves.append((sq120, target_sq))
                    target_sq += offset
                    if board.mailbox120[target_sq] == -1:
                        break
                if board.mailbox120[target_sq] != -1:
                    target_piece = board.board_play[target_sq]
                    if (board.side_to_move == 0 and isinstance(target_piece, str) and target_piece.islower()) or (board.side_to_move == 1 and isinstance(target_piece, str) and target_piece.isupper()):
                        moves.append((sq120, target_sq))
    return moves
                    
def generate_queen_moves(board: Board) -> list:
    moves = []
    queen = 'Q' if board.side_to_move == 0 else 'q'
    for sq120 in board.piece_list[queen]:
        for offset in QUEEN_OFFSET:
            target_sq = sq120 + offset
            # guard: first step must be on-board
            if board.mailbox120[target_sq] == -1:
                continue
            while True:
                if board.mailbox120[target_sq] == -1:
                    break
                if board.board_play[target_sq] == 0:
                    moves.append((sq120, target_sq))
                    target_sq += offset
                    continue
                # capture if opponent piece, then stop sliding
                target_piece = board.board_play[target_sq]
                if (
                    (board.side_to_move == 0 and isinstance(target_piece, str) and target_piece.islower()) or
                    (board.side_to_move == 1 and isinstance(target_piece, str) and target_piece.isupper())
                ):
                    moves.append((sq120, target_sq))
                break
    return moves

def generate_king_moves(board: Board) -> list:
    moves = []
    king = 'K' if board.side_to_move == 0 else 'k'
    for sq120 in board.piece_list[king]:
        for offset in KING_OFFSET:
            target_sq = sq120 + offset
            if board.mailbox120[target_sq] == -1:
                continue
            target_piece = board.board_play[target_sq]
            if target_piece == 0 or (isinstance(target_piece, str) and ((board.side_to_move == 0 and target_piece.islower()) or (board.side_to_move == 1 and target_piece.isupper()))):
                moves.append((sq120, target_sq))
    #Castling moves 
    if board.side_to_move == 0:
        if board.castle_white_short:
            if board.board_play[97] == 0 and board.board_play[98] == 0:
                moves.append((95, 97)) #e1 to g1
        if board.castle_white_long:
            if board.board_play[93] == 0 and board.board_play[94] == 0 and board.board_play[92] == 0:
                moves.append((95, 93)) #e1 to c1
    else:
        if board.castle_black_short:
            if board.board_play[27] == 0 and board.board_play[28] == 0:
                moves.append((25, 27)) #e8 to g8
        if board.castle_black_long:
            if board.board_play[24] == 0 and board.board_play[23] == 0 and board.board_play[22] == 0:
                moves.append((25, 23)) #e8 to c8
    return moves

def generate_pawn_moves(board: Board) -> list:
    moves = []
    pawn = 'P' if board.side_to_move == 0 else 'p'
    offsets = PAWN_OFFSET_WHITE if board.side_to_move == 0 else PAWN_OFFSET_BLACK
    
    #starting row indices for double-move detection (0-based with 10x12 mailbox: rank = (sq120//10)-2)
    start_row = 6 if board.side_to_move == 0 else 1


    for sq120 in board.piece_list[pawn]:
        #compute 0-based row from 120-square index
        row = (sq120 // 10) - 2

        # Single forward move
        target_sq = sq120 + offsets[0]
        if board.mailbox120[target_sq] != -1 and board.board_play[target_sq] == 0:
            moves.append((sq120, target_sq))

        # Double move forward from starting position (independent check)
        if row == start_row:
            target_sq2 = sq120 + offsets[1]
            # Both squares must be empty and within bounds
            if (board.mailbox120[target_sq] != -1 and board.board_play[target_sq] == 0 and
                board.mailbox120[target_sq2] != -1 and board.board_play[target_sq2] == 0):
                moves.append((sq120, target_sq2))
        # Captures
        for capture_offset in offsets[2:]:
            target_sq = sq120 + capture_offset
            if board.mailbox120[target_sq] == -1:
                continue
            target_piece = board.board_play[target_sq]
            if (board.side_to_move == 0 and isinstance(target_piece, str) and target_piece.islower()) or (board.side_to_move == 1 and isinstance(target_piece, str) and target_piece.isupper()):
                moves.append((sq120, target_sq))

        # En passant
        if board.en_passant is not None:
            en_passant_index = board.en_passant_to_index()
            for capture_offset in offsets[2:]:
                target_sq = sq120 + capture_offset
                if target_sq == en_passant_index:
                    moves.append((sq120, target_sq))

        #promotion handling (piece types) can be added later; moves to the final rank are already produced above.
    return moves

def generate_all_moves(board: Board) -> list:
    pseudo_moves = []
    pseudo_moves.extend(generate_pawn_moves(board))
    pseudo_moves.extend(generate_knight_moves(board))
    pseudo_moves.extend(generate_bishop_moves(board))
    pseudo_moves.extend(generate_rook_moves(board))
    pseudo_moves.extend(generate_queen_moves(board))
    pseudo_moves.extend(generate_king_moves(board))
    return pseudo_moves 

def king_in_check(board: Board, side: int) -> bool:
    king = 'K' if side == 0 else 'k'
    king_sq = board.piece_list[king][0]
    return is_square_attacked(board, king_sq, 1 - side)

def is_square_attacked(board: Board, sq120: int, by_side: int) -> bool:
    #Check for pawn attacks
    pawn = 'P' if by_side == 0 else 'p'
    pawn_offsets = PAWN_OFFSET_WHITE if by_side == 0 else PAWN_OFFSET_BLACK
    for offset in pawn_offsets[2:]:
        attacker_sq = sq120 + offset
        if board.mailbox120[attacker_sq] != -1 and board.board_play[attacker_sq] == pawn:
            return True

    #Check for knight attacks
    knight = 'N' if by_side == 0 else 'n'
    for offset in KNIGHT_OFFSET:
        attacker_sq = sq120 + offset
        if board.mailbox120[attacker_sq] != -1 and board.board_play[attacker_sq] == knight:
            return True

    #Check for bishop/queen diagonal attacks
    bishop = 'B' if by_side == 0 else 'b'
    queen = 'Q' if by_side == 0 else 'q'
    for offset in BISHOP_OFFSET:
        target_sq = sq120 + offset
        while board.mailbox120[target_sq] != -1:
            target_piece = board.board_play[target_sq]
            if target_piece == 0:
                target_sq += offset
                continue
            if target_piece == bishop or target_piece == queen:
                return True
            break

    #Check for rook/queen straight attacks
    rook = 'R' if by_side == 0 else 'r'
    for offset in ROOK_OFFSET:
        target_sq = sq120 + offset
        while board.mailbox120[target_sq] != -1:
            target_piece = board.board_play[target_sq]
            if target_piece == 0:
                target_sq += offset
                continue
            if target_piece == rook or target_piece == queen:
                return True
            break

    #Check for king attacks ?
    king = 'K' if by_side == 0 else 'k'
    for offset in KING_OFFSET:
        attacker_sq = sq120 + offset
        if board.mailbox120[attacker_sq] != -1 and board.board_play[attacker_sq] == king:
            return True

    return False