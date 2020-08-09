from math import floor


def round_up(number: float):
    """ Round half up to 2 decimal places. Avoids python 3 default rounding behaviour.

    :param number: Just a float value.
    :return: A number rounded half up to 2 decimal places.
    """

    return floor(number * 100 + 0.5) / 100


def calculate_percentage_discount(price: float, percentage: float) -> float:
    """ Calculates a percentage of given price up to 2 decimal places.

    :param price: A base price
    :param percentage: A given percentage from 0 to 100 represented as a float.
    :return: The discounted price
    """

    assert 0.0 < percentage < 1.0, "A discount must be between 0.0 and 1.0"
    return round_up(price * percentage)


def calculate_bogof(price: float, quantity: int, needed_items: int, free_items: int):
    """ Calculates the discount price, of a buy x get y promotion.
        bogof acronym => https://en.wikipedia.org/wiki/Buy_one,_get_one_free

    :param price: Default price of promotional item
    :param quantity: Number of the same items in a basket
    :param needed_items: Required amount of items to activate promotion
    :param free_items: Number of items given for free

    :return: Total price of free items earned
    """
    # Don't allow negative values
    assert not any([x for x in [price, quantity, needed_items, free_items] if x < 0.0])
    return price * int((quantity / needed_items) * free_items)
