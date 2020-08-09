

class BasketPricer(object):

    def __init__(self, basket, catalogue, offers):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers

    def _calculate_subtotal(self):

        subtotal = 0.0
        for item, quantity in self.basket.items():
            subtotal += self.catalogue[item] * quantity

        return subtotal

    def __call__(self):
        if not self.basket:
            return 0.0, 0.0, 0.0

        subtotal = self._calculate_subtotal()

        return subtotal, 0.0, 0.0
