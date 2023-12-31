from http import HTTPStatus

import mysql.connector as mysql
import pytest
import requests

from configuration import MYSQL_CREDENTIALS, API_KEY, API_USERNAME, DEFAULT_LOGGING_LEVEL, DEFAULT_BASE_URL
from src.baseclasses.baserequest import BaseRequest
from src.classes.cart_client import CartClient
from src.classes.login_client import LoginClient
from src.enums.routes import Routes
from src.utilities.logger import Logger


def pytest_addoption(parser):
    parser.addoption("--logging_level", default=DEFAULT_LOGGING_LEVEL, choices=("INFO", "WARNING", "ERROR"),)
    parser.addoption("--base_url", default=DEFAULT_BASE_URL)


@pytest.fixture(scope="session")
def class_cart_client(api_token, opencart_base_url, logger):
    api_client = BaseRequest(base_url=opencart_base_url, logger=logger, token=api_token)

    return CartClient(api_client)


@pytest.fixture(scope="session")
def class_cart_client_unauthorized(logger, opencart_base_url):
    api_client = BaseRequest(base_url=opencart_base_url, logger=logger)

    return CartClient(api_client)


@pytest.fixture(scope="session")
def class_login_client(logger, opencart_base_url):
    api_client = BaseRequest(base_url=opencart_base_url, logger=logger)

    return LoginClient(api_client)


@pytest.fixture(scope="session")
def api_token(opencart_base_url):

    response = requests.post(f"{opencart_base_url}{Routes.LOGIN}",
                             data={'username': API_USERNAME, 'key': API_KEY})

    assert response.status_code == HTTPStatus.OK
    assert response.json().get("api_token")

    return response.json()["api_token"]


@pytest.fixture(scope="session")
def db_connection():
    connection = mysql.connect(**MYSQL_CREDENTIALS)
    yield connection
    connection.close()


@pytest.fixture(scope="session")
def logger(request):
    log_level = request.config.getoption("--logging_level")

    return Logger(request.node.name, log_level).logger


@pytest.fixture(scope="session")
def opencart_base_url(request):
    return request.config.getoption("--base_url")


@pytest.fixture(scope="session")
def api_session(request):

    base_url = request.config.getoption("--base_url")

    session = requests.Session()
    response = session.post(f"{base_url}{Routes.LOGIN}",
                            data={'username': API_USERNAME, 'key': API_KEY})

    assert response.status_code == HTTPStatus.OK

    print(response.json()["success"], response.json()["api_token"])
    print(session.cookies.get_dict())
    yield session
