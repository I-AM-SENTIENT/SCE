from typing import Dict, List, Set, Tuple

from board import Board
from constants import (
    DOUBLED_PAWN_PENALTY,
    ISOLATED_PAWN_PENALTY,
    KING_OPEN_FILE_PENALTY,
    KING_SEMI_OPEN_FILE_PENALTY,
    KING_SHIELD_BONUS_FAR,
    KING_SHIELD_BONUS_NEAR,
    MIRROR64,
    PASSED_PAWN_BONUS,
    PIECE_VALUES,
    PST,
)


def _index64(board: Board, square120: int) -> int:
    idx = board.mailbox120[square120]
    if idx == -1:
        raise ValueError("Invalid square for mailbox64 index")
    return idx


def _file_rank(idx64: int) -> Tuple[int, int]:
    return idx64 % 8, idx64 // 8


def _material_score(board: Board) -> int:
    score = 0
    for piece, positions in board.piece_list.items():
        score += PIECE_VALUES[piece] * len(positions)
    return score


def _piece_square_score(board: Board) -> int:
    score = 0
    for piece, positions in board.piece_list.items():
        pst = PST.get(piece.upper())
        if not pst:
            continue
        for sq120 in positions:
            idx64 = _index64(board, sq120)
            if piece.isupper():
                score += pst[idx64]
            else:
                score -= pst[MIRROR64[idx64]]
    return score


def _collect_pawns(board: Board) -> Tuple[List[List[int]], List[List[int]], Set[Tuple[int, int]], Set[Tuple[int, int]]]:
    white_files: List[List[int]] = [[] for _ in range(8)]
    black_files: List[List[int]] = [[] for _ in range(8)]
    white_coords: Set[Tuple[int, int]] = set()
    black_coords: Set[Tuple[int, int]] = set()

    for sq120 in board.piece_list['P']:
        idx64 = _index64(board, sq120)
        file, rank = _file_rank(idx64)
        white_files[file].append(rank)
        white_coords.add((file, rank))

    for sq120 in board.piece_list['p']:
        idx64 = _index64(board, sq120)
        file, rank = _file_rank(idx64)
        black_files[file].append(rank)
        black_coords.add((file, rank))

    return white_files, black_files, white_coords, black_coords


def _is_passed_white(file: int, rank: int, black_files: List[List[int]]) -> bool:
    for df in (-1, 0, 1):
        f = file + df
        if 0 <= f < 8:
            for b_rank in black_files[f]:
                if b_rank < rank:
                    return False
    return True


def _is_passed_black(file: int, rank: int, white_files: List[List[int]]) -> bool:
    for df in (-1, 0, 1):
        f = file + df
        if 0 <= f < 8:
            for w_rank in white_files[f]:
                if w_rank > rank:
                    return False
    return True


def _pawn_structure_score(board: Board, pawn_info=None) -> int:
    white_files, black_files, white_coords, black_coords = pawn_info or _collect_pawns(board)
    score = 0

    #Doubled pawns
    for file in range(8):
        w_count = len(white_files[file])
        b_count = len(black_files[file])
        if w_count > 1:
            score -= DOUBLED_PAWN_PENALTY * (w_count - 1)
        if b_count > 1:
            score += DOUBLED_PAWN_PENALTY * (b_count - 1)

    #Isolated and passed pawns
    for file in range(8):
        for rank in white_files[file]:
            left = file - 1
            right = file + 1
            if (left < 0 or not white_files[left]) and (right > 7 or not white_files[right]):
                score -= ISOLATED_PAWN_PENALTY
            if _is_passed_white(file, rank, black_files):
                advance = 7 - rank  #Closer to promotion = bigger bonus
                score += PASSED_PAWN_BONUS[advance]

        for rank in black_files[file]:
            left = file - 1
            right = file + 1
            if (left < 0 or not black_files[left]) and (right > 7 or not black_files[right]):
                score += ISOLATED_PAWN_PENALTY
            if _is_passed_black(file, rank, white_files):
                advance = rank
                score -= PASSED_PAWN_BONUS[advance]

    return score


def _king_safety_side(
    board: Board,
    king_symbol: str,
    is_white: bool,
    friendly_files: List[List[int]],
    enemy_files: List[List[int]],
    friendly_coords: Set[Tuple[int, int]],
) -> int:
    positions = board.piece_list.get(king_symbol, [])
    if not positions:
        return 0

    idx64 = _index64(board, positions[0])
    file, rank = _file_rank(idx64)
    direction = -1 if is_white else 1
    near_rank = rank + direction
    far_rank = rank + 2 * direction
    score = 0

    for df in (-1, 0, 1):
        f = file + df
        if 0 <= f < 8:
            if 0 <= near_rank <= 7 and (f, near_rank) in friendly_coords:
                score += KING_SHIELD_BONUS_NEAR
            elif 0 <= far_rank <= 7 and (f, far_rank) in friendly_coords:
                score += KING_SHIELD_BONUS_FAR

    #Open/semi-open file penalties on king file
    if not friendly_files[file]:
        if enemy_files[file]:
            score -= KING_SEMI_OPEN_FILE_PENALTY
        else:
            score -= KING_OPEN_FILE_PENALTY

    return score


def _king_safety_score(board: Board, pawn_info=None) -> int:
    white_files, black_files, white_coords, black_coords = pawn_info or _collect_pawns(board)
    score = 0
    score += _king_safety_side(board, 'K', True, white_files, black_files, white_coords)
    score -= _king_safety_side(board, 'k', False, black_files, white_files, black_coords)
    return score


def evaluate_with_breakdown(board: Board) -> Tuple[int, Dict[str, int]]:
    pawn_info = _collect_pawns(board)
    material = _material_score(board)
    pst = _piece_square_score(board)
    pawn_structure = _pawn_structure_score(board, pawn_info)
    king_safety = _king_safety_score(board, pawn_info)

    total = material + pst + pawn_structure + king_safety
    breakdown = {
        'material': material,
        'piece_square': pst,
        'pawn_structure': pawn_structure,
        'king_safety': king_safety,
    }

    if board.side_to_move == 1:
        total = -total
        breakdown = {k: -v for k, v in breakdown.items()}

    return total, breakdown


def evaluate(board: Board) -> int:
    total, _ = evaluate_with_breakdown(board)
    return total