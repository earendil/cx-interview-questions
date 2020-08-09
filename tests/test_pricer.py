from unittest import TestCase
from collections import defaultdict

from shopping_basket.pricer import BasketPricer


class TestBasketPricer(TestCase):

    def setUp(self) -> None:

        self.basket = defaultdict(int)
        self.catalogue = {
            "Baked Beans": 0.99,
            "Biscuits": 1.20,
            "Sardines": 1.89,
            "Shampoo": 2.00
        }
        self.offers = {
            "Baked Beans": ("BuyXgetYfree", (2, 1)),
            "Sardines": ("discount", 0.25),
        }

    def test_empty_basket(self):
        """ An empty basket has a sub-total, discount and total each of zero.
        """

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)
        subtotal, discounts, total = pricer()

        self.assertEqual([0.0, 0.0, 0.0], [subtotal, discounts, total])

    def test_subtotal(self):
        """ sub-total: The undiscounted cost of items in a basket.
        """

        self.basket["Biscuits"] += 2
        self.basket["Shampoo"] += 2

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)
        subtotal, discounts, total = pricer()

        self.assertEqual(6.4, subtotal)
