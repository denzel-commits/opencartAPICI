from src.baseclasses.baserequest import BaseRequest
from src.classes.custom_assert.login_assert_helper import LoginAssertHelper
from src.enums.routes import Routes


class LoginClient:
    def __init__(self, api_client: BaseRequest):
        self.api_client = api_client

    def login_api(self, credentials: dict):
        return LoginAssertHelper(*self.api_client.post(Routes.LOGIN, data=credentials))
