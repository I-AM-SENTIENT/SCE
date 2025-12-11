import pytest
from typing import Dict

from board import Board
from constants import (
    KIWIPETE_FEN,
    POS3_FEN,
    POS4_FEN,
    POS4_MIRRORED_FEN,
    STARTING_FEN,
)
from eval import evaluate_with_breakdown
from fen import fen_to_board


POSITIONS = {
    "start": STARTING_FEN,
    "kiwipete": KIWIPETE_FEN,
    "pos3": POS3_FEN,
    "pos4": POS4_FEN,
    "pos4_mirrored": POS4_MIRRORED_FEN,
}


def _describe_breakdown(breakdown: Dict[str, int]) -> str:
    parts = [f"{key}={value}" for key, value in breakdown.items()]
    return ", ".join(parts)


def test_eval_outputs_and_breakdown():
    required_keys = {"material", "piece_square", "pawn_structure", "king_safety", "mobility"}

    for name, fen in POSITIONS.items():
        board = Board()
        fen_to_board(board, fen)
        score, breakdown = evaluate_with_breakdown(board)

        # Emits a human-friendly line that shows the composition of the evaluation
        print(f"{name}: score={score} | {_describe_breakdown(breakdown)}")

        assert required_keys.issubset(breakdown.keys())
        assert isinstance(score, int)

    # Smoke check: we evaluated every configured position
    assert len(POSITIONS) == 5
