from http import HTTPStatus

import mysql.connector as mysql
import pytest
import requests

from configuration import MYSQL_CREDENTIALS, API_KEY, API_USERNAME
from src.baseclasses.baserequest import BaseRequest
from src.classes.cart_client import CartClient
from src.enums.routes import Routes
from src.utilities.logger import Logger


def pytest_addoption(parser):
    parser.addoption("--logging_level", default="WARNING")
    parser.addoption("--base_url", default="http://192.168.1.127:8081")


@pytest.fixture(scope="session")
def class_cart_client(api_token, logger, request):
    base_url = request.config.getoption("--base_url")
    api_client = BaseRequest(base_url=base_url, logger=logger, token=api_token)

    return CartClient(api_client)


@pytest.fixture(scope="session")
def api_token(request):

    base_url = request.config.getoption("--base_url")

    response = requests.post(f"{base_url}{Routes.LOGIN}",
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
def api_session(request):

    base_url = request.config.getoption("--base_url")

    session = requests.Session()
    response = session.post(f"{base_url}{Routes.LOGIN}",
                            data={'username': API_USERNAME, 'key': API_KEY})

    assert response.status_code == HTTPStatus.OK

    print(response.json()["success"], response.json()["api_token"])
    print(session.cookies.get_dict())
    yield session


@pytest.fixture()
def opencart_base_url(request):
    return request.config.getoption("--base_url")


@pytest.fixture()
def opencart_api(logger, request):
    base_url = request.config.getoption("--base_url")
    return BaseRequest(base_url=base_url, logger=logger)
