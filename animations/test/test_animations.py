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
        n = r.randint(2, 100)
        start_x = r.randint(0, n - 1)
        start_y = r.randint(0, n - 1)
        end_x = r.randint(0, n - 1)
        end_y = r.randint(0, n - 1)
        bishop_x = r.randint(0, n - 1)
        bishop_y = r.randint(0, n - 1)
        return start_x, start_y, end_x, end_y, bishop_x, bishop_y, n


if __name__ == "__main__":
    unittest.main()
