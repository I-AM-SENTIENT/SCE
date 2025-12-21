class Board:
    def __init__(self):
    #States of the game
        self.side_to_move = 0 #0 - white, 1 - black

        self.castle_white_short = 1
        self.castle_white_long = 1
        self.castle_black_short = 1
        self.castle_black_long = 1

        self.en_passant = None #Stores target square

        self.half_move_counter = 0 #half-moves since the last pawn advance or capture, half moves means move by 1 player
        self.full_move_counter = 1 #Full move meaning move by both players, starts at 1 for some reason, increase after black move
        
        self.reversible_moves = 0 #Moves by pieces (not pawns) to empty squares, not sure if this usefull
        

    #Mailbox representation for 120 and 64 squares for mapping
        self.mailbox120 = [
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1,  0,  1,  2,  3,  4,  5,  6,  7, -1, #8 row
     -1,  8,  9, 10, 11, 12, 13, 14, 15, -1, #7 row...
     -1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
     -1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
     -1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
     -1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
     -1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
     -1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        
        self.mailbox64 = [
    21, 22, 23, 24, 25, 26, 27, 28, #8 row
    31, 32, 33, 34, 35, 36, 37, 38, #7 row...
    41, 42, 43, 44, 45, 46, 47, 48,
    51, 52, 53, 54, 55, 56, 57, 58,
    61, 62, 63, 64, 65, 66, 67, 68,
    71, 72, 73, 74, 75, 76, 77, 78,
    81, 82, 83, 84, 85, 86, 87, 88,
    91, 92, 93, 94, 95, 96, 97, 98]
        
        #Actual board for storing pieces
        self.board_play = [0] * 120

        #Add piece lists for move generation
        self.piece_list = {
            'P': [],
            'N': [],
            'B': [],
            'R': [],
            'Q': [],
            'K': [],
            'p': [],
            'n': [],
            'b': [],
            'r': [],
            'q': [],
            'k': []}
    #Function for updating the list 
    def update_piece_list(self):
        for key in self.piece_list:
            self.piece_list[key] = []
        
        for index64 in range(64):
            sq120 = self.mailbox64[index64]
            piece = self.board_play[sq120]
            if piece != 0:
                self.piece_list[piece].append(sq120)
                
    #Convert algebraic enpassant square to 120 index
    def en_passant_to_index(self) -> int:
        if self.en_passant is None:
            return -1
        file = ord(self.en_passant[0]) - ord('a')  #0-7
        rank = int(self.en_passant[1])  #1-8
        index64 = (8 - rank) * 8 + file
        return self.mailbox64[index64]