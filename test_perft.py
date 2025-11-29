import pytest
from board import Board
from fen import fen_to_board
from perft import perft, index_to_algebraic
from constants import STARTING_FEN, KIWIPETE_FEN, POS3_FEN, POS4_FEN


class TestPerft:
    """Perft tests for move generation validation."""
    
    def test_starting_position_depth_1(self):
        board = Board()
        fen_to_board(board, STARTING_FEN)
        assert perft(board, 1) == 20
    
    def test_starting_position_depth_2(self):
        board = Board()
        fen_to_board(board, STARTING_FEN)
        assert perft(board, 2) == 400
    
    def test_starting_position_depth_3(self):
        board = Board()
        fen_to_board(board, STARTING_FEN)
        assert perft(board, 3) == 8902
    
    def test_starting_position_depth_4(self):
        board = Board()
        fen_to_board(board, STARTING_FEN)
        assert perft(board, 4) == 197281
    
    def test_kiwipete_depth_1(self):
        board = Board()
        fen_to_board(board, KIWIPETE_FEN)
        assert perft(board, 1) == 48
    
    def test_kiwipete_depth_2(self):
        board = Board()
        fen_to_board(board, KIWIPETE_FEN)
        assert perft(board, 2) == 2039
    
    def test_kiwipete_depth_3(self):
        board = Board()
        fen_to_board(board, KIWIPETE_FEN)
        assert perft(board, 3) == 97862
    
    def test_pos3_depth_1(self):
        board = Board()
        fen_to_board(board, POS3_FEN)
        assert perft(board, 1) == 14
    
    def test_pos3_depth_2(self):
        board = Board()
        fen_to_board(board, POS3_FEN)
        assert perft(board, 2) == 191
    
    def test_pos3_depth_3(self):
        board = Board()
        fen_to_board(board, POS3_FEN)
        assert perft(board, 3) == 2812
    
    def test_pos4_depth_1(self):
        board = Board()
        fen_to_board(board, POS4_FEN)
        assert perft(board, 1) == 6
    
    def test_pos4_depth_2(self):
        board = Board()
        fen_to_board(board, POS4_FEN)
        assert perft(board, 2) == 264
    
    def test_pos4_depth_3(self):
        board = Board()
        fen_to_board(board, POS4_FEN)
        assert perft(board, 3) == 9467


class TestIndexToAlgebraic:
    """Test coordinate conversion."""
    
    def test_a1(self):
        assert index_to_algebraic(91) == "a1"
    
    def test_h1(self):
        assert index_to_algebraic(98) == "h1"
    
    def test_a8(self):
        assert index_to_algebraic(21) == "a8"
    
    def test_h8(self):
        assert index_to_algebraic(28) == "h8"
    
    def test_e1(self):
        assert index_to_algebraic(95) == "e1"
    
    def test_e8(self):
        assert index_to_algebraic(25) == "e8"
    
    def test_d4(self):
        assert index_to_algebraic(64) == "d4"


class TestSpecialMoves:
    """Test specific edge cases."""
    
    def test_en_passant_position(self):
        #Position where en passant is possible
        board = Board()
        fen_to_board(board, "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3")
        #White pawn on e5 can capture en passant on d6
        result = perft(board, 1)
        assert result == 31  #30 normal + 1 en passant
    
    def test_castling_both_sides(self):
        #Position where both castles are possible
        board = Board()
        fen_to_board(board, "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
        result = perft(board, 1)
        assert result == 25  #16 pawn moves + 4 knight moves + 2 castles + 3 rook moves
    
    def test_promotion_position(self):
        #Pawn about to promote
        board = Board()
        fen_to_board(board, "8/P7/8/8/8/8/8/4K2k w - - 0 1")
        result = perft(board, 1)
        # 4 promotions + king moves
        assert result >= 4