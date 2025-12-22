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

#Timing defaults used by the UCI time allocator

DEFAULT_MOVES_TO_GO = 40            #default moves to go when movestogo not provided
TIME_SAFETY_MARGIN_MS = 50          #ms to subtract as safety slack when allocating time
MIN_THINK_TIME_MS = 10              #minimum thinking time allocated in ms

#Stuff for eval

PIECE_VALUES = {
    'P': 100,
    'N': 320,
    'B': 330,
    'R': 500,
    'Q': 900,
    'K': 20000,
    'p': -100,
    'n': -320,
    'b': -330,
    'r': -500,
    'q': -900,
    'k': -20000,
}