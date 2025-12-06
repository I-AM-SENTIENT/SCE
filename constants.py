#MOVE OFFSETS
QUEEN_OFFSET = [-10,10,-1,+1,-11,11,-9,9]
KING_OFFSET = [-10,10,-1,+1,-11,11,-9,9]
BISHOP_OFFSET = [-11,11,-9,9]
KNIGHT_OFFSET = [-21,-19,-12,-8,8,12,19,21]
ROOK_OFFSET = [-10,10,-1,1]
PAWN_OFFSET_WHITE = [-10,-20,-9,-11]
PAWN_OFFSET_BLACK = [10,20,9,11]

#FEN's for perft and STARTING_POS

STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
KIWIPETE_FEN = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -'
POS3_FEN = '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1'
POS4_FEN = 'r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1'
POS4_MIRRORED_FEN = 'r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1'
POS5_FEN = 'rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8'
POS6_FEN = 'r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10'

#Results for perft

PERFT_RESULTS = {
    STARTING_FEN: [20, 400, 8902, 197281, 4865609, 119060324],
    KIWIPETE_FEN: [48, 2039, 97862, 4085603, 193690690],
    POS3_FEN: [14, 191, 2812, 43238, 674624],
    POS4_FEN: [6, 264, 9467, 422333, 15833292],
    POS4_MIRRORED_FEN: [6, 264, 9467, 422333, 15833292],
    POS5_FEN: [44, 1486, 62379, 2103487, 89941194],
    POS6_FEN: [46, 2079, 89890, 3894594, 164075551],
}

#Indexes for rows

ROW_8 = {21, 22, 23, 24, 25, 26, 27, 28}
ROW_7 = {31, 32, 33, 34, 35, 36, 37, 38}
ROW_6 = {41, 42, 43, 44, 45, 46, 47, 48}
ROW_5 = {51, 52, 53, 54, 55, 56, 57, 58}
ROW_4 = {61, 62, 63, 64, 65, 66, 67, 68}
ROW_3 = {71, 72, 73, 74, 75, 76, 77, 78}
ROW_2 = {81, 82, 83, 84, 85, 86, 87, 88}
ROW_1 = {91, 92, 93, 94, 95, 96, 97, 98}

#Pieces symbols
PIECES = ['r','n','b','q','k','p','P','R','N','B','Q','K']

#Stuff for search
INFINITY = 999999
MATE_SCORE = 100000

#Time management
DEFAULT_MOVES_TO_GO = 30          # Assume 30 moves left if not specified
TIME_SAFETY_MARGIN_MS = 50        # Keep buffer to avoid losing on time
MIN_THINK_TIME_MS = 10            # Never think less than this
TIME_CHECK_NODES = 2048           # Check time every N nodes
MAX_SEARCH_DEPTH = 64             # Hard cap on search depth

#Stuff for Eval
PIECE_VALUES = {
    'P': 100,   'p': -100,
    'N': 320,   'n': -320,
    'B': 330,   'b': -330,
    'R': 500,   'r': -500,
    'Q': 900,   'q': -900,
    'K': 0,     'k': 0, 
}

#Mirror indexes (flip ranks, keep files) for 64-square indices
MIRROR64 = [
    56, 57, 58, 59, 60, 61, 62, 63,
    48, 49, 50, 51, 52, 53, 54, 55,
    40, 41, 42, 43, 44, 45, 46, 47,
    32, 33, 34, 35, 36, 37, 38, 39,
    24, 25, 26, 27, 28, 29, 30, 31,
    16, 17, 18, 19, 20, 21, 22, 23,
     8,  9, 10, 11, 12, 13, 14, 15,
     0,  1,  2,  3,  4,  5,  6,  7,
]

#Piece-square tables (white perspective, 0..63 = a8..h1)
PST = {
    'P': [
         0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10,-20,-20, 10, 10,  5,
         5, -5,-10,  0,  0,-10, -5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
         0,  0,  0,  0,  0,  0,  0,  0,
    ],
    'N': [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,
    ],
    'B': [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,
    ],
    'R': [
         0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         0,  0,  0,  5,  5,  0,  0,  0,
    ],
    'Q': [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20,
    ],
    'K': [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20,
    ],
}

#Pawn structure and king safety weights (centipawns)
ISOLATED_PAWN_PENALTY = 15
DOUBLED_PAWN_PENALTY = 12
PASSED_PAWN_BONUS = [0, 5, 10, 20, 35, 60, 90, 140]  #Index = advancement (0..7)
KING_SHIELD_BONUS_NEAR = 10   #Pawn one rank in front of king (or behind for black)
KING_SHIELD_BONUS_FAR = 5     #Pawn two ranks away from king
KING_SEMI_OPEN_FILE_PENALTY = 10  #No friendly pawn on king file, enemy pawn present
KING_OPEN_FILE_PENALTY = 6        #No pawns on king file
