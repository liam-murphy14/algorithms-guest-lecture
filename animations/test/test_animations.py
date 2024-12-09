import unittest
from animations.animations import KnightMoves
import random as r


class TestKnightMoves(unittest.TestCase):

    def test_algorithms_match(self):
        """
        test that all 3 algorithms return the same result
        """
        for _ in range(1_000):
            start_x, start_y, end_x, end_y, bishop_x, bishop_y, n = (
                self._get_test_case()
            )
            with self.subTest(
                start_x=start_x,
                start_y=start_y,
                end_x=end_x,
                end_y=end_y,
                bishop_x=bishop_x,
                bishop_y=bishop_y,
                n=n,
            ):
                knight_moves = KnightMoves(
                    start_x, start_y, end_x, end_y, bishop_x, bishop_y, n, False
                )
                control = knight_moves.unoptimized_bfs()
                bfs = knight_moves.bfs(with_gui=False)
                dbfs = knight_moves.dbfs(with_gui=False)
                self.assertEqual(control, bfs)
                self.assertEqual(control, dbfs)

    def _get_test_case(self):
        """
        get a single test case
        """
        n = r.randint(3, 100)
        start_x, start_y = self._get_random_position(n)
        end_x, end_y = self._get_random_position(n)
        bishop_x, bishop_y = self._get_random_position(n)
        while (bishop_x, bishop_y) == (start_x, start_y) or (bishop_x, bishop_y) == (end_x, end_y):
            bishop_x, bishop_y = self._get_random_position(n)
        return start_x, start_y, end_x, end_y, bishop_x, bishop_y, n

    
    def _get_random_position(self, n):
        """
        get a random position
        """
        return r.randint(0, n - 1), r.randint(0, n - 1)


if __name__ == "__main__":
    unittest.main()
