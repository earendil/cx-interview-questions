from unittest import TestCase

from shopping_basket.promotions import calculate_percentage_discount, calculate_bogof, round_up


class TestDiscount(TestCase):

    def test_calculate_discount(self):
        self.assertEqual(0.47, calculate_percentage_discount(1.89, 0.25))
        self.assertEqual(0.5, calculate_percentage_discount(0.99, 0.5))
        self.assertEqual(0.07, calculate_percentage_discount(0.23, 0.3))

    def test_larger_than_100_percent(self):
        with self.assertRaises(AssertionError):
            calculate_percentage_discount(0.99, 1.2)

    def test_negative_discount(self):
        with self.assertRaises(AssertionError):
            calculate_percentage_discount(0.99, -0.2)


class TestBOGOF(TestCase):

    def test_calculate_bogof(self):
        self.assertEqual(0.0, calculate_bogof(1.0, 1, 2, 1))
        self.assertEqual(0.0, calculate_bogof(0.99, 2, 2, 1))
        self.assertEqual(1.0, calculate_bogof(0.5, 6, 2, 1))
        self.assertEqual(1.5, calculate_bogof(1.5, 6, 3, 1))
        self.assertEqual(2.0, calculate_bogof(1.0, 8, 3, 1))
        self.assertEqual(0.2, calculate_bogof(0.2, 3, 2, 1))

    def test_negative_value(self):
        with self.assertRaises(AssertionError):
            calculate_bogof(-0.2, 4, 2, 1)

        with self.assertRaises(AssertionError):
            calculate_bogof(0.2, -4, 2, 1)

        with self.assertRaises(AssertionError):
            calculate_bogof(0.2, 4, -2, 1)

        with self.assertRaises(AssertionError):
            calculate_bogof(0.2, 4, 2, -1)


class TestRoundUp(TestCase):

    def test_round_up(self):
        self.assertEqual(1.5, round_up(1.495))
        self.assertEqual(2.15, round_up(2.146))
        self.assertEqual(0.03, round_up(0.032))
        self.assertEqual(-4.56, round_up(-4.5589))
