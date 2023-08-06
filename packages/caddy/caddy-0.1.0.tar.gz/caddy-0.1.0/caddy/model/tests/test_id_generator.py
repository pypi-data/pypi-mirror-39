from unittest import TestCase

from caddy.model.model import IdGenerator


class TestIdGenerator(TestCase):
    def test_next(self):
        gen = IdGenerator()
        for i in range(10):
            self.assertEqual(i + 1, gen.next(), 'id matches')

        offset = 4
        gen = IdGenerator(offset)
        for i in range(10):
            self.assertEqual(i + offset + 1, gen.next(), 'id matches')
