import json
import logging
from typing_extensions import Self

import allure
from pydantic import ValidationError, BaseModel
from requests import Response


class BaseResponse:
    def __init__(self, response: Response, logger: logging) -> None:
        self.logger = logger
        self.response = response
        self.response_status = response.status_code
        self.response_text = response.text

        try:
            self.response_json = response.json()
        except json.JSONDecodeError as e:
            self.logger.error(f"Response json decode error '{e}'")

    @allure.step("Verify response status code is {status_code}")
    def assert_status_code(self, status_code: int) -> Self:
        self.logger.info(f"Verify response status code {self.response_status} is {status_code}")
        assert self.response_status == status_code, f"{self.response_status} is not equal to {status_code}"

        return self

    @allure.step("Validate response JSON schema")
    def validate_schema(self, schema: BaseModel) -> Self:
        self.logger.info("Validate response JSON schema")
        if self.response_json and isinstance(self.response_json, list):
            for item in self.response_json:
                try:
                    schema.model_validate(item)
                except ValidationError as e:
                    self.logger.error("Response json schema didn't pass validation", exc_info=True)
                    raise AssertionError(e)
        else:
            try:
                schema.model_validate(self.response_json)
            except ValidationError as e:
                self.logger.error("Response json schema didn't pass validation", exc_info=True)
                raise AssertionError(e)

        return self

    @allure.step("Validate success message")
    def assert_success_message(self, message: str) -> Self:
        self.logger.info(f"Validate success message is {message}")
        assert self.response_json["success"] == message, "Response message is " + self.response_json["success"]

        return self

    @allure.step("Validate error message")
    def assert_error_message(self, message: str) -> Self:
        self.logger.info("Validate error message is {message}")
        assert self.response_json["error"]["store"] == message, \
            "Response message " + self.response_json["error"]["store"] + f" is not expected {message}"

        return self

    @allure.step("Validate warning message")
    def assert_warning_message(self, message: str) -> Self:
        self.logger.info(f"Validate warning message is {message}")
        assert self.response_json["error"]["warning"] == message, \
            "Response message " + self.response_json["error"]["store"] + f" is not expected {message}"

        return self

    @allure.step("Validate product is in cart")
    def assert_product_is_in_cart(self, product_data: dict) -> Self:
        self.logger.info(f"Validate {product_data} is in cart")

        assert product_data["product_id"] in [int(cart_item["product_id"]) for cart_item in self.response_json["products"]], \
            f"Product with id {product_data['product_id']} is not in cart"

        return self

    @allure.step("Validate product quantity in cart")
    def assert_product_quantity_in_cart(self, product_data: dict) -> Self:
        self.logger.info(f"Validate {product_data} quantity")

        cart_item_quantity = [int(cart_item["quantity"]) for cart_item in self.response_json["products"]
                              if int(cart_item["product_id"]) == product_data["product_id"]][0]

        assert product_data["quantity"] == cart_item_quantity, \
            f"Product quantity in cart {cart_item_quantity} does not match with quantity added {product_data['quantity']}"

        return self

    @allure.step("Validate product is not in cart")
    def assert_product_is_not_in_cart(self, product_data: dict) -> Self:
        self.logger.info(f"Validate {product_data} is added to cart")

        assert product_data["product_id"] not in [int(cart_item["product_id"]) for cart_item in self.response_json["products"]], \
            f"Product with id {product_data['product_id']} is not added to cart"

        return self

    @allure.step("Validate cart total")
    def assert_cart_total(self, product_data: dict, price: float) -> Self:
        expected_total = round(product_data["quantity"] * price, 2)

        self.logger.info(f"Validate cart total is {expected_total}")

        formatted_cart_total = round(float(self.response_json["totals"][-1]["text"][1:].replace(",", "")), 2)

        assert expected_total == formatted_cart_total, \
            f"Cart total {formatted_cart_total} != {expected_total}"

        return self

    def __str__(self):
        return f"\nStatus code: {self.response_status} \n" \
               f"Requested url: {self.response.url} \n" \
               f"Response body: {self.response_text}"
