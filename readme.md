# Shopping Basket Pricer

A solution to the Shopping Basket Pricer challenge.

### Dependencies:

* Python3.8
* Make (optional)

### Usage:

The basket pricer can be imported directly via: `from shopping_basket.pricer import BasketPricer`  
It needs to be initialised with a basket, catalogue and offers argument.  
It can then be called without any arguments returning the subtotal, discount and total values.

Example:
```python
from collections import namedtuple

from shopping_basket.pricer import BasketPricer

# These are just stubs, as they are implemented by a different team.
offer = namedtuple("Offer", ["name", "x", "y", "percentage"])
basket = {"Baked Beans": 2}
catalogue = {"Baked Beans": 0.99}
offers = {"Baked Beans": offer("discount_percentage", 0, 0, 0.25)}

pricer = BasketPricer(basket, catalogue, offers)

subtotal, discount, total = pricer()
```

### Tests:

* Run `make run_tests` or alternatively `python3.8 -m unittest discover` from the project root.

### Considerations:

* Assumed that the the job of the basket pricer is to perform the required calculations 
and return the values, leaving the formatting and displaying to a separate specialised component.
* Used the Offers examples to implement, different offers will require further changes.
* Attempted to not use any 3rd party libraries.
* Assumed that baskets will always have items that exists in the catalogue.
* Assumed a basket to be a dictionary with item as key and quantity as value.
* Under the Behaviour section it states that a "Basket cannot have a negative price", I'm assuming it means that a basket cannot have a negative quantity of items as well as the basket pricer cannot have a negative total.
* Given that the objective of the challenge is the implementation of the basket pricer and the interface leaves much to be intepreted, I have assumed basket, catalogue and offers to be as simple as possible and they exist only within tests.
* Assumed that it's the job of the team implementing basket to ensure it doesn't have a negative quantity.


### Potential Improvements:

* Use https://code.google.com/archive/p/python-money/
* Create specialised exceptions
* Use `mock.patch` on a number of unit tests rather than letting them calculate the promotion.
* Refactor `_calculate_discount` a better implementation of offers would allow the removal of the conditionality