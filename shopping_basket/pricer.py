from math import floor
from typing import NamedTuple


def round_up(number: float):
    """ Round half up to 2 decimal places.
    """
    return floor(number * 100 + 0.5) / 100


def calculate_discount(price: float, percentage: float):
    return round_up(price * (1 - percentage))


def calculate_bogof(quantity: int, needed_items: int, free_items: int):
    """ https://en.wikipedia.org/wiki/Buy_one,_get_one_free
    """
    return int((quantity / needed_items) * free_items)


class BasketPricer(object):

    mapped_offers = {
        "discount": calculate_discount,
        "BuyXgetYfree": calculate_bogof,
    }

    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def _calculate_subtotal(self):

        subtotal = 0.0
        for item, quantity in self.basket.items():
            subtotal += self.catalogue[item] * quantity

        return subtotal

    def _apply_offer(self, item: str, quantity: int, offer: NamedTuple):

        if "discount" == offer.name:
            price = self.catalogue[item] * quantity
            return self.mapped_offers[offer.name](price, offer.percentage)

        elif "BuyXgetYfree" == offer.name:
            free_items = self.mapped_offers[offer.name](quantity, offer.x, offer.y)
            return self.catalogue[item] * free_items

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

        return subtotal, 0.0, 0.0
