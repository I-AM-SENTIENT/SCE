from constants import PIECE_VALUES

def evaluate(board) -> int:
    """Return a simple material evaluation (centipawns).

    Positive = White better, Negative = Black better.
    """
    score = 0

    # board.piece_list maps piece symbol -> list of squares
    for piece, squares in board.piece_list.items():
        if piece == 0:
            continue
        value = PIECE_VALUES.get(piece, 0)
        score += value * len(squares)

    return score
