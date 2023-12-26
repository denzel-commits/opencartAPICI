import logging
import allure
from requests import Response
from typing_extensions import Self

from src.baseclasses.baseresponse import BaseResponse


class CartAssertHelper(BaseResponse):
    def __init__(self, response: Response, logger: logging):
        super().__init__(response, logger)

    @allure.step("Validate product is in cart")
    def assert_product_is_in_cart(self, product_data: dict) -> Self:
        self.logger.info(f"Validate {product_data} is in cart")

        assert product_data["product_id"] in [int(cart_item["product_id"]) for cart_item in
                                              self.response_json["products"]], \
            f"Product with id {product_data['product_id']} is not in cart"

        return self

    @allure.step("Validate product is not in cart")
    def assert_product_is_not_in_cart(self, product_id: int) -> Self:
        self.logger.info(f"Validate {product_id} is in cart")

        assert product_id not in [int(cart_item["product_id"]) for cart_item in self.response_json["products"]], \
            f"Product with id {product_id} is not in cart"

        return self

    @allure.step("Validate product quantity in cart")
    def assert_product_quantity_in_cart(self, product_data: dict) -> Self:
        self.logger.info(f"Validate product quantity for {product_data} ")

        cart_item_quantity = [int(cart_item["quantity"]) for cart_item in self.response_json["products"]
                              if int(cart_item["product_id"]) == int(product_data["product_id"])][0]

        assert product_data["quantity"] == cart_item_quantity, \
            f"Product quantity in cart {cart_item_quantity} does not match expected quantity {product_data['quantity']}"

        return self

    @allure.step("Validate cart is empty")
    def assert_cart_is_empty(self) -> Self:
        expected_total = 0.00

        formatted_cart_total = round(float(self.response_json["totals"][-1]["text"][1:].replace(",", "")), 2)

        self.logger.info("Validate cart is empty")
        assert len(self.response_json["products"]) == 0, \
            "Cart is not empty"

        self.logger.info(f"Validate cart total is {expected_total}")
        assert expected_total == formatted_cart_total, \
            f"Cart total {formatted_cart_total} != {expected_total}"

        return self

    @allure.step("Validate cart total")
    def assert_cart_total(self, product_data: dict, price: float) -> Self:
        expected_total = round(product_data["quantity"] * price, 2)

        self.logger.info(f"Validate cart total is {expected_total}")

        cart_total = self.get_cart_total()

        assert expected_total == cart_total, \
            f"Cart total {cart_total} != {expected_total}"

        return self

    @allure.step("Validate cart total")
    def assert_cart_total_decreased(self, initial_cart_totals: dict, product_data: dict) -> Self:
        cart_total = self.get_cart_total()

        product_cost = int(product_data["quantity"]) * self.format_price(product_data["price"])

        initial_cart_total = self.format_price(initial_cart_totals[-1]["text"])
        expected_total = initial_cart_total - product_cost

        self.logger.info(f"Validate cart total is {expected_total}")

        assert cart_total == expected_total, \
            f"Cart total {cart_total} != {expected_total}"

        return self

    @allure.step("Validate cart total")
    def assert_cart_total_increased(self, initial_cart_totals: dict, product_data: dict) -> Self:
        cart_total = self.get_cart_total()

        product_cost = int(product_data["quantity"]) * self.format_price(product_data["price"])

        initial_cart_total = self.format_price(initial_cart_totals[-1]["text"])
        expected_total = initial_cart_total + product_cost

        self.logger.info(f"Validate cart total is {expected_total}")

        assert cart_total == expected_total, \
            f"Cart total {cart_total} != {expected_total}"

        return self

    def get_cart_total(self):
        return self.format_price(self.response_json["totals"][-1]["text"])
