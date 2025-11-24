class Board:
    def __init__(self):
    #States of the game
        self.side_to_move = 1 #1 - white, 0 - black

        self.castle_white_short = 1
        self.castle_white_long = 1
        self.castle_black_short = 1
        self.castle_black_long = 1

        self.en_passant = None #Stores target square

        self.half_move_counter = 0 #half-moves since the last pawn advance or capture, half moves means move by 1 player
        self.full_move_counter = 0 #Full move meaning move by both players

        self.reversible_moves = 0 #Moves by pieces (not pawns) to empty squares, not sure if this usefull
        

    #Mailbox representation for 120 and 64 squares for mapping
        self.mailbox120 = [
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1,  0,  1,  2,  3,  4,  5,  6,  7, -1,
     -1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
     -1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
     -1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
     -1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
     -1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
     -1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
     -1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        
        self.mailbox64 = [
    21, 22, 23, 24, 25, 26, 27, 28,
    31, 32, 33, 34, 35, 36, 37, 38,
    41, 42, 43, 44, 45, 46, 47, 48,
    51, 52, 53, 54, 55, 56, 57, 58,
    61, 62, 63, 64, 65, 66, 67, 68,
    71, 72, 73, 74, 75, 76, 77, 78,
    81, 82, 83, 84, 85, 86, 87, 88,
    91, 92, 93, 94, 95, 96, 97, 98]
        
        #Actual board for storing pieces

        #Initialize it empty, populate from STARTING_FEN
        self.board = [0] * 64

        