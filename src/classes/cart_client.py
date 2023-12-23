from src.baseclasses.baserequest import BaseRequest
from src.classes.cart_assert_helper import CartAssertHelper
from src.enums.routes import Routes


class CartClient:
    def __init__(self, api_client: BaseRequest):
        self.api_client = api_client

    def add_product_api(self, product_data: dict) -> CartAssertHelper:
        return CartAssertHelper(*self.api_client.post(Routes.CART + "/add", data=product_data))

    def remove_product_api(self, cart_id=None) -> CartAssertHelper:

        data = {"key": cart_id} if cart_id is not None else {}

        return CartAssertHelper(*self.api_client.post(Routes.CART + "/remove", data=data))

    def get_products_api(self) -> CartAssertHelper:
        return CartAssertHelper(*self.api_client.post(Routes.CART + '/products'))
