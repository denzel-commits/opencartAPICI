from enum import Enum


class Routes(str, Enum):
    LOGIN = "/index.php?route=api/login"
    CART = "/index.php?route=api/cart"
    ORDER = "/index.php?route=api/order"  # not tested
    CURRENCY = "/index.php?route=api/currency"  # not tested

    def __str__(self):
        return self.value
