from unittest import TestCase
from unittest.mock import MagicMock

from caddy.model.polyline import PolyLine
from caddy.shared.point import Point


class TestPolyline(TestCase):
    def test_move_by(self):
        p = PolyLine(1, [Point(0, 1), Point(1, 2), Point(2, 3), Point(3, 4)])
        p.move_by(Point(1, 1))
        self.assertEqual([Point(1, 2), Point(2, 3), Point(3, 4), Point(4, 5)], p.points)

    def test_id(self):
        p = PolyLine(42, [])
        self.assertEqual(42, p.shape_id, 'id matches')

    def test_get_color(self):
        p = PolyLine(1, [Point(1, 2), Point(3, 4)], '#000001')
        self.assertEqual('#000001', p.color, 'color matches')

    def test_set_color(self):
        p = PolyLine(1, [Point(1, 2), Point(3, 4)], '#000001')
        p.color = '#000002'
        self.assertEqual('#000002', p.color, 'color matches')

    def test_accept_visitor(self):
        p = PolyLine(1, [Point(1, 2), Point(3, 4)], '#000001')
        visitor = MagicMock()
        p.accept_visitor(visitor)
        visitor.visit_polyline.assert_called_once_with(p)

    def test___repr__(self):
        p = PolyLine(1, [Point(1, 2), Point(3, 4)], '#000001')
        self.assertEqual('PolyLine[Points: [(1,2), (3,4)]]', p.__str__())

    def test___str__(self):
        p = PolyLine(1, [Point(1, 2), Point(3, 4)], '#000001')
        self.assertEqual('PolyLine[Points: [(1,2), (3,4)]]', p.__str__())

    def test_contains_own_points(self):
        """
                   (20,20)-----(40,20)
                    |               \
                    |                 \
        (0,0)-----(20,0)(twice)         (60, 0)
        """

        points = [Point(0, 0), Point(20, 0), Point(20, 0), Point(20, 20), Point(40, 20), Point(60, 0)]
        pl = PolyLine(1, points)

        """ Test own points """
        for point in points:
            self.assertTrue(pl.contains_point(point), 'contains own point' + str(point))
            p = point + Point(0, PolyLine.TOLERANCE)
            self.assertTrue(pl.contains_point(p), 'contains own point moved by y offset' + str(p))

            p = point - Point(0, PolyLine.TOLERANCE)
            self.assertTrue(pl.contains_point(p), 'contains own point moved by y offset' + str(p))

            p = point + Point(PolyLine.TOLERANCE, 0)
            self.assertTrue(pl.contains_point(p), 'contains own point moved by x offset' + str(p))

            p = point - Point(PolyLine.TOLERANCE, 0)
            self.assertTrue(pl.contains_point(p), 'contains own point moved by x offset' + str(p))

    def test_contains_middle_points(self):
        """
                   (20,20)--x--(40,20)
                    |               \
                    x                 x
        (0,0)--x--(20,0)(twice)         (60, 0)
        """

        points = [Point(0, 0), Point(20, 0), Point(20, 0), Point(20, 20), Point(40, 20), Point(60, 0)]
        pl = PolyLine(1, points)

        middle_points = []
        for i in range(len(points) - 1):
            middle_points.append(Point.midpoint(points[i], points[i + 1]))

        """ Test middle points """
        for point in middle_points:
            self.assertTrue(pl.contains_point(point), 'contains middle point' + str(point))
            p = point + Point(0, PolyLine.TOLERANCE)
            self.assertTrue(pl.contains_point(p), 'contains middle point moved by y offset' + str(p))

            p = point - Point(0, PolyLine.TOLERANCE)
            self.assertTrue(pl.contains_point(p), 'contains middle point moved by y offset' + str(p))

            p = point + Point(PolyLine.TOLERANCE, 0)
            self.assertTrue(pl.contains_point(p), 'contains middle point moved by x offset' + str(p))

            p = point - Point(PolyLine.TOLERANCE, 0)
            self.assertTrue(pl.contains_point(p), 'contains middle point moved by x offset' + str(p))

    def test_out_of_range(self):
        """
              0    (20,20)-- --(40,20)  <0>
           0        |               \      <0>
                    x                 x
        (0,0)-- --(20,0)   0      <0>   (60, 0)     0
        """

        # TOLERANCE MUST BE <= 5 for this test to work
        # Points marked with <> are problematic and need to be adjusted manually with every tolerance

        points = [Point(0, 0), Point(20, 0), Point(20, 0), Point(20, 20), Point(40, 20), Point(60, 0)]
        tol = PolyLine.TOLERANCE
        out_of_range_points = [Point(0, 0) + Point(0, tol + 1),
                               Point(20, 0) + Point(tol + 1, 0),
                               Point(20, 20) - Point(tol + 1, 0),
                               Point(60, 0) - Point(tol + 3, 0),
                               Point(60, 0) + Point(tol + 1, 0),
                               Point(60, 0) + Point(0, tol + 3),
                               Point(40, 20) + Point(tol + 3, 0),
                               ]
        pl = PolyLine(1, points)
        for point in out_of_range_points:
            self.assertFalse(pl.contains_point(point), 'does not contain out of range point' + str(point))

    def test_not_contains_when_empty(self):
        pl = PolyLine(1, [])
        out_of_range_points = [Point(0, 0), Point(0, 1)]
        for point in out_of_range_points:
            self.assertFalse(pl.contains_point(point), 'does not contain out of range point' + str(point))
