from unittest import TestCase

from kep.query.end_user import date_to_tuple


class TestEndUserAux(TestCase):
    def test_date_to_tuple(self):
        self.assertEqual(date_to_tuple(2000), (2000, 1))
        self.assertEqual(date_to_tuple("2000"),  (2000, 1))
        self.assertEqual(date_to_tuple("2000-07"),  (2000, 7))
        self.assertEqual(date_to_tuple("2000-1"),  (2000, 1))
