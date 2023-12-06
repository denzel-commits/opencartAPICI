import pytest

from src.baseclasses.baserequest import BaseRequest
from src.utilities.logger import Logger


def pytest_addoption(parser):
    parser.addoption("--logging-level", default="WARNING")


@pytest.fixture()
def logger(request):
    log_level = request.config.getoption("--logging-level")

    return Logger(request.node.name, log_level).get_logger()


@pytest.fixture()
def opencart_api(logger):
    return BaseRequest(base_url="http://myopencart.example.com/index.php", logger=logger)