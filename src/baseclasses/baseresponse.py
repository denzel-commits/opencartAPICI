import allure
from pydantic import ValidationError


class BaseResponse:
    def __init__(self, response, logger):
        self.response = response
        self.response_json = response.json()
        self.response_status = response.status_code
        self.logger = logger

    @allure.step("Verify response status code to be {status_code}")
    def assert_status_code(self, status_code):
        self.logger.info(f"Verify response status code {self.response_status} to be {status_code}")
        assert self.response_status == status_code, f"{self.response_status} is not equal to {status_code}"
        return self

    @allure.step("Validate response JSON schema")
    def validate_schema(self, schema):
        self.logger.info(f"Validate response JSON schema")
        if isinstance(self.response_json, list):
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


    def __str__(self):
        return f"\nStatus code: {self.response_status} \n" \
               f"Requested url: {self.response.url} \n" \
               f"Response body: {self.response_json}"