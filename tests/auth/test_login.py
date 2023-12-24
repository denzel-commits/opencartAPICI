from http import HTTPStatus

import allure
import pytest

from configuration import API_USERNAME, API_KEY
from src.pydantic_schemas.success_api_token import SuccessApiToken


@allure.feature("Login")
class TestLogin:
    @pytest.mark.parametrize("username, key", [(API_USERNAME, API_KEY)])
    def test_login_get_api_token_successfully(self, username, key, class_login_client):
        class_login_client.login_api({"username": username, "key": key}). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(SuccessApiToken). \
            assert_api_token_received()


@allure.feature("Login")
class TestLoginNegative:
    @pytest.mark.parametrize("username, key", [(API_USERNAME, "12345")])
    def test_login_get_api_token_failed(self, username, key, class_login_client):
        class_login_client.login_api({"username": username, "key": key}). \
            assert_status_code(HTTPStatus.OK). \
            assert_api_token_is_not_received()
