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

    def test_valid_cases(self):
        """
        test all 3 algorithms on known cases
        """
        test_cases = [
            (4, 2, 2, 6, 2, 3, 8, 4),
            (2, 2, 2, 2, 3, 4, 5, 0),
            (3, 3, 1, 0, 1, 3, 4, 5),
            (3, 3, 4, 0, 3, 1, 5, 6),
            (17, 43, 14, 18, 38, 42, 47, 28),
        ]
        for test_case in test_cases:
            start_x, start_y, end_x, end_y, bishop_x, bishop_y, n, expected = test_case
            with self.subTest(
                start_x=start_x,
                start_y=start_y,
                end_x=end_x,
                end_y=end_y,
                bishop_x=bishop_x,
                bishop_y=bishop_y,
                n=n,
                expected=expected,
            ):
                knight_moves = KnightMoves(
                    start_x, start_y, end_x, end_y, bishop_x, bishop_y, n, False
                )
                control = knight_moves.unoptimized_bfs()
                bfs = knight_moves.bfs(with_gui=False)
                dbfs = knight_moves.dbfs(with_gui=False)
                self.assertEqual(control, expected)
                self.assertEqual(bfs, expected)
                self.assertEqual(dbfs, expected)

    def _get_test_case(self):
        """
        get a single test case
        """
        n = r.randint(3, 100)
        start_x, start_y = self._get_random_position(n)
        end_x, end_y = self._get_random_position(n)

        bishop_x, bishop_y = self._get_random_position(n)
        bishop_positions = self._get_bishop_positions(bishop_x, bishop_y, n)
        while (
            (bishop_x, bishop_y) == (start_x, start_y)
            or (bishop_x, bishop_y) == (end_x, end_y)
            or (start_x, start_y) in bishop_positions
        ):
            bishop_x, bishop_y = self._get_random_position(n)
            bishop_positions = self._get_bishop_positions(bishop_x, bishop_y, n)

        return start_x, start_y, end_x, end_y, bishop_x, bishop_y, n

    def _get_random_position(self, n):
        """
        get a random position
        """
        return r.randint(0, n - 1), r.randint(0, n - 1)

    def _get_bishop_positions(
        self, bishop_x: int, bishop_y: int, n: int
    ) -> set[tuple[int, int]]:
        """
        Get all possible positions for the bishop.
        """
        bishop_positions = set()
        for i in range(1, n):
            new_positions = [
                (bishop_x + i, bishop_y + i),
                (bishop_x + i, bishop_y - i),
                (bishop_x - i, bishop_y + i),
                (bishop_x - i, bishop_y - i),
            ]
            for new_x, new_y in new_positions:
                if self._is_valid_position(new_x, new_y, n):
                    bishop_positions.add((new_x, new_y))
        return bishop_positions

    def _is_valid_position(self, x: int, y: int, n: int) -> bool:
        """
        Check if position is valid.
        """
        return 0 <= x < n and 0 <= y < n


if __name__ == "__main__":
    unittest.main()
