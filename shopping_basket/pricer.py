from typing import NamedTuple

from shopping_basket.promotions import (
    calculate_percentage_discount,
    calculate_bogof,
    round_up,
)


class BasketPricer(object):
    """ A class that calculates the price of goods including any applicable discounts
    """

    mapped_offers = {
        "discount_percentage": calculate_percentage_discount,
        "BuyXgetYfree": calculate_bogof,
    }

    def __init__(self, basket, catalogue, offers):
        """ BasketPricer object initialiser

        :param basket: A collection of goods a customer wishes to buy
        :param catalogue: The products currently sold by the supermarket
        :param offers: These are pricing rules which under some circumstances
                       may cause one or more items in the basket to be discounted
        """
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def _calculate_subtotal(self) -> float:
        """ Helper that generates the total price for all items in the basket prior to
            any discount being applied

        :return: The subtotal price
        """
        subtotal = 0.0
        for item, quantity in self.basket.items():
            subtotal += self.catalogue[item] * quantity

        return round_up(subtotal)

    def _calculate_discount(self, item: str, quantity: int) -> float:
        """ Calculates a discount available for an item by identifying
            known discounts with offers available.

        :param item: Item present in a given basket
        :param quantity: The quantity of given item present in the basket
        :return: A discount value
        """

        offer = self.offers[item]

        if "discount_percentage" == offer.name:
            price = self.catalogue[item] * quantity
            return self.mapped_offers[offer.name](price, offer.percentage)

        elif "BuyXgetYfree" == offer.name:
            price = self.catalogue[item]
            return self.mapped_offers[offer.name](price, quantity, offer.x, offer.y)

        else:
            raise Exception(f"Unable to calculate offer: {offer.name}")

    def _calculate_total_discounts(self) -> float:
        """ Calculates total value of promotions to be deducted from subtotal

        :return: Total discounts
        """
        discounts = 0.0
        for item, quantity in self.basket.items():
            if item in self.offers.keys():
                discounts += self._calculate_discount(item, quantity)
        return discounts

    def __call__(self):
        if not self.basket:
            return 0.0, 0.0, 0.0

        subtotal = self._calculate_subtotal()
        discount = self._calculate_total_discounts()
        total = subtotal - discount

        return subtotal, discount, total
