import unittest
from XiangqiGame import *


class MyTestCase(unittest.TestCase):

    def test_init_state(self):
        game = XiangqiGame()
        self.assertEqual(game.get_game_state(), "UNFINISHED")

    def test_make_move_edge_cases(self):
        game = XiangqiGame()
        self.assertEqual(game.make_move("z1", "e3"), False)  # tests from col out of range
        self.assertEqual(game.make_move("c1", "Z3"), False)  # tests to col out of range
        self.assertEqual(game.make_move("c11", "e3"), False)  # tests from row out of range
        self.assertEqual(game.make_move("c1", "e11"), False)  # tests to row out of range
        self.assertEqual(vars(game.get_game_piece_at_square("c1")), vars(Elephant("red")))  # tests function
        self.assertEqual(game.make_move("c1", "d1"), False)    # tests friendly fire

    """---------ELEPHANT TESTS--------------------------------------------------------------------------"""

    def test_elephant_move_row_range_false(self):
        game = XiangqiGame()
        self.assertEqual(game.make_move("b3", "d6"), False)
        self.assertEqual(game.make_move("b3", "d5"), False)
        self.assertEqual(game.make_move("b8", "d6"), False)

    """---------CHARIOT TESTS--------------------------------------------------------------------------"""

    def test_chariot_jump_false(self):
        game = XiangqiGame()
        game.make_move("e4", "e5")
        self.assertEqual(game.make_move("I10", "i6"), False)
        self.assertEqual(game.make_move("a10", "a9"), True)
        self.assertEqual(game.make_move("i1", "i3"), True)

    """---------CANNON TESTS--------------------------------------------------------------------------"""

    def test_cannon_jump_false(self):
        game = XiangqiGame()
        game.make_move("e4", "e5")
        self.assertEqual(game.make_move("g10", "g8"), False)
        game.make_move("e7", "e6")
        game.make_move("a4", "a5")
        self.assertEqual(game.make_move("h8", "c8"), True)

    """---------GENERAL TESTS--------------------------------------------------------------------------"""

    def test_general_leave_castle(self):
        game = XiangqiGame()
        game.make_move("e1", "e2")
        game.make_move("e7", "e6")
        game.make_move("e2", "d2")
        game.make_move("e6", "e5")
        self.assertEqual(game.make_move("d2", "c2"), False)
        self.assertEqual(game.make_move("d2", "d3"), True)

    def test_general_can_see(self):
        game = XiangqiGame()
        game.make_move("e4", "e5")
        game.make_move("e7", "e6")
        game.make_move("e5", "e6")
        game.make_move("i7", "i6")
        self.assertEqual(game.make_move("e6", "g6"), False)

    """---------ADVISOR TESTS--------------------------------------------------------------------------"""

    def test_advisor(self):
        game = XiangqiGame()
        self.assertEqual(game.make_move("d1", "d2"), False)
        self.assertEqual(game.make_move("f1", "e2"), True)

    """---------HORSE TESTS--------------------------------------------------------------------------"""

    def test_horse(self):
        game = XiangqiGame()
        self.assertEqual(game.make_move("h1", "g3"), True)
        game.make_move("h1", "g3")
        self.assertEqual(game.make_move("g3", "e4"), False)
        self.assertEqual(game.make_move("g3", "d5"), False)

    """---------SOLDIER TESTS--------------------------------------------------------------------------"""

    def test_soldier(self):
        game = XiangqiGame()
        self.assertEqual(game.make_move("e4", "e5"), True)
        game.make_move("e4", "e5")
        self.assertEqual(game.make_move("e5", "f5"), False)
        game.make_move("a7", "a6")
        game.make_move("e5", "e6")
        game.make_move("a6", "a5")
        self.assertEqual(game.make_move("e6", "f6"), True)

    """---------CHECK TESTS--------------------------------------------------------------------------"""

    def test_check(self):
        game = XiangqiGame()
        game.make_move("e4", "e5")
        game.make_move("e7", "e6")
        game.make_move("i4", "i5")
        game.make_move("a10", "a9")
        game.make_move("g4", "g5")
        game.make_move("h8", "c8")
        game.make_move("e5", "e6")
        game.make_move("a9", "e9")
        self.assertEqual(game.make_move("e6", "g6"), False)     # will put general in check
        game.make_move("e6", "e7")
        game.make_move("e9", "e7")
        self.assertEqual(game.is_in_check('red'), True)     # puts red general in check
        self.assertEqual(game.make_move("a4", "a5"), False)     # will not save general
        self.assertEqual(game.make_move("f1", "e2"), True)      # move saves the general
        self.assertEqual(game.is_in_check('red'), False)     # previous move saved the general out of check

    def test_real_game_1(self):
        """
        The following code is a game copied from an online match found at:
        http://wxf.ca/wxf/index.php/xiangqi-news/news-from-europ/381-world-xiangqi-championships-2015-game-records
        :return:
        """
        game = XiangqiGame()
        game.make_move('g4', 'g5')
        game.make_move('c7', 'c6')
        game.make_move('b3', 'c3')
        game.make_move('c10', 'e8')
        game.make_move('b1', 'a3')
        game.make_move('b8', 'b4')
        game.make_move('h1', 'g3')
        game.make_move('b10', 'c8')
        game.make_move('g1', 'e3')
        game.make_move('c8', 'd6')
        game.make_move('a1', 'b1')
        game.make_move('a10', 'b10')
        game.make_move('f1', 'e2')
        game.make_move('b4', 'b2')
        game.make_move('i1', 'f1')
        game.make_move('f10', 'e9')
        game.make_move('f1', 'f6')
        game.make_move('d6', 'c8')
        game.make_move('a4', 'a5')
        game.make_move('b10', 'b3')
        game.make_move('c3', 'd3')
        game.make_move('c8', 'b6')
        game.make_move('g3', 'f5')
        game.make_move('b6', 'c4')
        game.make_move('d3', 'd9')
        game.make_move('c4', 'a3')
        game.make_move('h3', 'b3')
        game.make_move('a3', 'b1')
        game.make_move('b3', 'b10')
        self.assertEqual(game.get_game_state(), 'RED_WON')


if __name__ == '__main__':
    unittest.main()
