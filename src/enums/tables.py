from enum import Enum


class Tables(str, Enum):
    PREFIX = "oc_"
    CART = "cart"
    PRODUCT = "product"
    TAXES = "tax_rate"

    def __str__(self):
        return self.value
