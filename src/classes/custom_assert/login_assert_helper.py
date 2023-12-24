import logging
import allure
from requests import Response
from typing_extensions import Self

from src.baseclasses.baseresponse import BaseResponse


class LoginAssertHelper(BaseResponse):
    def __init__(self, response: Response, logger: logging):
        super().__init__(response, logger)

    @allure.step("Checking receipt of API token")
    def assert_api_token_received(self) -> Self:
        self.logger.info("Checking receipt of API token " + self.response_json["api_token"])

        assert self.response_json["api_token"], f"API token was not received {self}"

        return self

    @allure.step("Checking receipt of API token")
    def assert_api_token_is_not_received(self) -> Self:
        self.logger.info(f"Checking receipt of API token {self.response_text}")

        assert not self.response_json, f"API token received {self}"

        return self
