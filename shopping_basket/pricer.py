from typing import NamedTuple

from shopping_basket.promotions import calculate_percentage_discount, calculate_bogof


class BasketPricer(object):
    """ A class that calculates the price of goods including any applicable discounts
    """

    mapped_offers = {
        "discount": calculate_percentage_discount,
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

        return subtotal

    def _apply_offer(self, item: str, quantity: int, offer: NamedTuple):

        if "discount" == offer.name:
            price = self.catalogue[item] * quantity
            return self.mapped_offers[offer.name](price, offer.percentage)

        elif "BuyXgetYfree" == offer.name:
            price = self.catalogue[item]
            return self.mapped_offers[offer.name](price, quantity, offer.x, offer.y)

        else:
            raise Exception(f"Unable to calculate offer: {offer.name}")

    def _calculate_total_discounts(self):

        discounts = 0.0
        for item, quantity in self.basket.items():
            if item in self.offers.keys():
                discounts += self._apply_offer(item, quantity, self.offers[item])
        return discounts

    def __call__(self):
        if not self.basket:
            return 0.0, 0.0, 0.0

        subtotal = self._calculate_subtotal()
        discount = self._calculate_total_discounts()

        return subtotal, discount, 0.0
