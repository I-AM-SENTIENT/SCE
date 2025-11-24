from board import Board
from constants import PIECES
#Functions that 1 - Take board return FEN, 2 - Take FEN return board



def fen_to_board(fen):
    #Get all parts of the FEN
    parts = fen.split()
    #Get the part that contains our possitions of pieces
    pieces = parts[0].split()
    #We now get it by row
    rows = pieces[0].split('/')
    #FEN starts from the top to bottom meaning from a8 to b8.... and then a7....
    #Numbers indicate number of empty squars
    #rows will always have 8 parts and its a list of strings
    
    #Now we need to take it part by part where each part represents whats in a row
    index = 0 #We will be using that to allocate our pieces
    for row in rows:
        for char in row: #We take each charachter in our row
            if char.isdigit(): #We start by checking if the char is a number, it indicates amount of empty squares
                value = int(char)
                index += value
            elif char in PIECES:
                Board.board_play[index] = char #If it's a piece we simply put it on the board
                index += 1
            else:
                raise ValueError('CHAR IN ROW NEITHER A NUMBER OR A VALID PIECE')
    #Now we are done with board and we need to workout the rest of the fen
    #2[1] part of fen is side to move
    if parts[1] == 'w':
        Board.side_to_move = 0
    elif parts[1] == 'b':
        Board.side_to_move = 1
    else:
        raise ValueError("FEN SIDE TO MOVE INNCORECT/NOTFOUND")
    
    #Now castling
    castling = parts[2]
    if 'K' in castling:
        Board.castle_white_short = 1
    else:
        Board.castle_white_short = 0

    if 'Q' in castling:
        Board.castle_white_long = 1
    else:
        Board.castle_white_long = 0

    if 'k' in castling:
        Board.castle_black_short = 1
    else:
        Board.castle_black_short = 0

    if 'q' in castling:
        Board.castle_black_long = 1
    else:
        Board.castle_black_long = 0

    #En passant target square, this is given in algebraic soooo it sucks
    en_passant = parts[3]
    if en_passant == '-':
        Board.en_passant = None
    else:
        Board.en_passant = en_passant
    #Half move clock
    half_move = parts[4]
    Board.half_move_counter = int(half_move)

    #Full move
    full_move = parts[5]
    Board.full_move_counter = int(full_move)
    


def board_to_fen(board):
    fen = []
    #Get pieces from board and convert to FEN
    for row in range(8):
        empty_count = 0
        for col in range(8):
            piece = board.board_play[row * 8 + col]
            if piece == 0:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen.append(str(empty_count))
                    empty_count = 0
                fen.append(piece)
        if empty_count > 0:
            fen.append(str(empty_count))
        if row != 7:
            fen.append('/')
    #Side to move
    if board.side_to_move == 0:
        fen.append(' w ')
    else:
        fen.append(' b ')
    #Castling rights
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
    fen.append(' ' + castling + ' ')
    #En passant target square
    if board.en_passant is None:
        fen.append('- ')
    else:
        fen.append(board.en_passant + ' ') #Assuming en_passant is already in algebraic notation
    #Half move clock
    fen.append(str(board.half_move_counter) + ' ')
    #Full move number
    fen.append(str(board.full_move_counter))
    return ''.join(fen)

fen_to_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')