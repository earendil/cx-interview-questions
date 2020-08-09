from unittest import TestCase
from collections import defaultdict, namedtuple

from shopping_basket.pricer import BasketPricer, calculate_discount, calculate_bogof


class TestBasketPricer(TestCase):

    def setUp(self) -> None:

        self.basket = defaultdict(int)
        self.catalogue = {
            "Baked Beans": 0.99,
            "Biscuits": 1.20,
            "Sardines": 1.89,
            "Shampoo": 2.00
        }

        offer = namedtuple("Offer", ["name", "x", "y", "percentage"])

        self.offers = {
            "Baked Beans": offer("BuyXgetYfree", 2, 1, 0.0),
            "Sardines": offer("discount", 0, 0, 0.25),
            "Shampoo": offer("BuyXgetYfree", 3, 1, 0.0),
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

        self.assertEqual(6.4, pricer._calculate_subtotal())

    def test_total_discount(self):
        """ The amount of money which must be subtracted from the subtotal
         in order to calculate the final price of the goods in the basket.
        """

        self.basket["Baked Beans"] += 4
        self.basket["Sardines"] += 1

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)

        self.assertEqual(3.4, pricer._calculate_total_discounts())


class TestDiscount(TestCase):

    def test_calculate_discount(self):
        self.assertEqual(1.42, calculate_discount(1.89, 0.25))
        self.assertEqual(0.5, calculate_discount(0.99, 0.5))


class TestBOGOF(TestCase):

    def test_calculate_bogof(self):
        self.assertEqual(0, calculate_bogof(1, 2, 1))
        self.assertEqual(1, calculate_bogof(2, 2, 1))
        self.assertEqual(3, calculate_bogof(6, 2, 1))
        self.assertEqual(2, calculate_bogof(6, 3, 1))
        self.assertEqual(1, calculate_bogof(5, 3, 1))

# TODO: * TEST ALL HELPER FUNCTIONS
# TODO: * MAYBE MOVE OFFER'S LOGIC ELSEWHERE
