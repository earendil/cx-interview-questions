from unittest import TestCase
from collections import defaultdict, namedtuple

from shopping_basket.pricer import BasketPricer


class TestBasketPricer(TestCase):

    def setUp(self):

        self.basket = defaultdict(int)
        self.catalogue = {
            "Baked Beans": 0.99,
            "Biscuits": 1.20,
            "Sardines": 1.89,
            "Shampoo": 2.00,
            "Corona Vaccine": 1000000000.00
        }

        offer = namedtuple("Offer", ["name", "x", "y", "percentage"])

        self.offers = {
            "Baked Beans": offer("BuyXgetYfree", 2, 1, 0.0),
            "Sardines": offer("discount_percentage", 0, 0, 0.25),
            "Shampoo": offer("BuyXgetYfree", 3, 1, 0.0),
            "Corona Vaccine": offer("BuyForFree", 0, 0, 1.0)

        }

    def test_empty_basket(self):
        """ An empty basket has a sub-total, discount and total each of zero.
        """

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)
        subtotal, discounts, total = pricer()

        self.assertEqual([0.0, 0.0, 0.0], [subtotal, discounts, total])

    def test_calculate_subtotal(self):
        """ sub-total: The undiscounted cost of items in a basket.
        """

        self.basket["Biscuits"] += 2
        self.basket["Shampoo"] += 2

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)

        self.assertEqual(6.4, pricer._calculate_subtotal())

    def test_calculate_total_discounts(self):
        """ The amount of money which must be subtracted from the subtotal
         in order to calculate the final price of the goods in the basket.
        """

        self.basket["Baked Beans"] += 4
        self.basket["Sardines"] += 1

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)

        self.assertEqual(1.46, pricer._calculate_total_discounts())

    def test_no_discounts(self):

        self.basket["Biscuits"] += 2

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)

        self.assertEqual(0.0, pricer._calculate_total_discounts())

    def test_calculate_discount_percentage(self):

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)

        self.assertEqual(0.95, pricer._calculate_discount("Sardines", 2))

    def test_calculate_discount_buyXgetY(self):

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)

        self.assertEqual(2.0, pricer._calculate_discount("Shampoo", 4))

    def test_calculate_discount_unknown_discount(self):

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)

        with self.assertRaises(Exception):
            self.assertEqual(2.0, pricer._calculate_discount("Corona Vaccine", 1))

    def test_assignment_example_one(self):

        self.basket["Baked Beans"] += 4
        self.basket["Biscuits"] += 1

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)

        self.assertEqual((5.16, 0.99, 4.17), pricer())

    def test_assignment_example_two(self):

        self.basket["Baked Beans"] += 2
        self.basket["Biscuits"] += 1
        self.basket["Sardines"] += 2

        pricer = BasketPricer(self.basket, self.catalogue, self.offers)

        self.assertEqual((6.96, 0.95, 6.01), pricer())
