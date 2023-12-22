from src.baseclasses.baserequest import BaseRequest
from src.baseclasses.baseresponse import BaseResponse
from src.enums.routes import Routes


class CartClient:
    def __init__(self, api_client: BaseRequest):
        self.api_client = api_client

    def add_product_api(self, product_data: dict) -> BaseResponse:
        return self.api_client.post(Routes.CART + "/add", data=product_data)

    def remove_product_api(self, cart_id=None) -> BaseResponse:

        data = {"key": cart_id} if cart_id is not None else {}

        return self.api_client.post(Routes.CART + "/remove", data=data)

    def get_products_api(self) -> BaseResponse:
        return self.api_client.post(Routes.CART + '/products')
