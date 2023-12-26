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
            self.response_json = {}
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

    @staticmethod
    def format_price(price):
        return round(float(price[1:].replace(",", "")), 2)

    def __str__(self):
        return f"\nStatus code: {self.response_status} \n" \
               f"Requested url: {self.response.url} \n" \
               f"Response body: {self.response_text}"
