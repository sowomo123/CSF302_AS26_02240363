import random
import unittest
from closest import closest_pair, closest_pair_brute


class TestClosestPair(unittest.TestCase):
    def check_both(self, points):
        """Check that both algorithms return the same distance."""
        brute = closest_pair_brute(points)
        divide = closest_pair(points)
        self.assertAlmostEqual(brute[0], divide[0], places=6)

    def test_two_points(self):
        self.check_both([(1, 2), (5, 5)])

    def test_duplicate_points(self):
        self.check_both([(1, 2), (5, 5), (1, 2)])

    def test_vertical_line(self):
        self.check_both([(2, 1), (2, 8), (2, 4), (2, 5)])

    def test_pair_across_dividing_line(self):
        self.check_both([
            (0, 0), (2, 10), (10, 0),
            (10.1, 0), (20, 10), (30, 0)
        ])

    def test_given_example(self):
        points = [
            (2, 3), (12, 30), (40, 50),
            (5, 1), (12, 10), (3, 4)
        ]
        result = closest_pair(points)
        self.assertAlmostEqual(result[0], 2 ** 0.5)
        self.assertEqual(result[1:], (0, 5))

    def test_500_random_inputs(self):
        rng = random.Random(2026)
        for _ in range(500):
            n = rng.randint(2, 50)
            points = [
                (rng.randint(-100, 100),
                 rng.randint(-100, 100))
                for _ in range(n)
            ]
            with self.subTest(points=points):
                self.check_both(points)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            closest_pair([])
        with self.assertRaises(ValueError):
            closest_pair_brute([(1, 2)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
