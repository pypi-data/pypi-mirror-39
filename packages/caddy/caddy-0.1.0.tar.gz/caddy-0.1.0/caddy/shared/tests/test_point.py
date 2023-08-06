from unittest import TestCase

from caddy.shared.point import Point


class TestPoint(TestCase):
    def test_eq(self):
        p1 = p2 = Point(1, 1)
        self.assertTrue(p1 == p2)
        self.assertTrue(Point(1, 1) == Point(1, 1))
        self.assertFalse(Point(1, 0) == Point(1, 1))

    def test_ne(self):
        self.assertTrue(Point(1, 0) != Point(1, 1))
        self.assertFalse(Point(1, 1) != Point(1, 1))

    def test_dist_from(self):
        self.assertEqual(0, Point(1, 2).dist_from(Point(1, 2)))
        self.assertEqual(1, Point(1, 2).dist_from(Point(1, 3)))
        self.assertEqual(1, Point(1, 2).dist_from(Point(2, 2)))
        self.assertAlmostEqual(5, Point(1, 1).dist_from(Point(5, 4)))

    def test_dist_from_squared(self):
        self.assertEqual(0, Point.dist_from_squared(Point(1, 2), Point(1, 2)))
        self.assertEqual(1, Point.dist_from_squared(Point(1, 3), Point(1, 2)))
        self.assertEqual(1, Point.dist_from_squared(Point(2, 2), Point(1, 2)))
        self.assertEqual(25, Point.dist_from_squared(Point(1, 1), Point(5, 4)))

    def test_dist(self):
        self.assertEqual(0, Point.dist(Point(1, 2), Point(1, 2)))
        self.assertEqual(1, Point.dist(Point(1, 2), Point(1, 3)))
        self.assertEqual(1, Point.dist(Point(1, 2), Point(2, 2)))
        self.assertAlmostEqual(5, Point.dist(Point(1, 1), Point(5, 4)))

    def test_dist_squared(self):
        self.assertEqual(0, Point.dist_squared(Point(1, 2), Point(1, 2)))
        self.assertEqual(1, Point.dist_squared(Point(1, 2), Point(1, 3)))
        self.assertEqual(1, Point.dist_squared(Point(1, 2), Point(2, 2)))
        self.assertAlmostEqual(25, Point.dist_squared(Point(1, 1), Point(5, 4)))

    def test_midpoint(self):
        self.assertEqual(Point(1, 4), Point.midpoint(Point(1, 1), Point(1, 8)))
        self.assertEqual(Point(4, 1), Point.midpoint(Point(1, 1), Point(8, 1)))
        self.assertEqual(Point(4, 3), Point.midpoint(Point(0, 0), Point(8, 6)))

    def test_add(self):
        self.assertEqual(Point(1, 2), Point(1, 1) + Point(0, 1))
        self.assertEqual(Point(1, 1), Point(1, 1) + Point(0, 0))

    def test_as_tuple(self):
        self.assertEqual(Point(1, 2).as_tuple(), (1, 2))
        self.assertEqual(Point(2, 3).as_tuple(), (2, 3))

    def test_iadd(self):
        p = Point(1, 1)
        p += Point(0, 1)
        self.assertEqual(Point(1, 2), p)

    def test_sub(self):
        self.assertEqual(Point(1, 1), Point(1, 2) - Point(0, 1))
        self.assertEqual(Point(1, 1), Point(1, 1) - Point(0, 0))

    def test_isub(self):
        p = Point(1, 2)
        p -= Point(0, 1)
        self.assertEqual(Point(1, 1), p)

    def test_str(self):
        self.assertEqual('(1,2)', Point(1, 2).__str__())

    def test_repr(self):
        self.assertEqual('(1,2)', Point(1, 2).__repr__())
