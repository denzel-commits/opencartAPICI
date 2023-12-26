from http import HTTPStatus

import allure
import pytest

from src.utilities.data_manager import DataManager
from src.pydantic_schemas.cart import Cart
from src.pydantic_schemas.error import Error
from src.pydantic_schemas.success import Success


@allure.feature("Cart")
@allure.story("Remove from cart")
class TestRemoveFromCart:
    test_products = DataManager().get_test_products_from_db()

    @allure.title("Remove single product from cart")
    @pytest.mark.parametrize("setup_products_in_cart", [test_products[0]], indirect=True)
    def test_remove_single_product_from_card_successfully(self, class_cart_client, remove_all_items_from_cart,
                                                          setup_products_in_cart):

        cart_items = class_cart_client.get_products_api().response_json["products"]

        class_cart_client.remove_product_api(cart_id=cart_items[0]["cart_id"]).\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.get_products_api().\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Cart).\
            assert_cart_is_empty()

    @allure.title("Remove one of the products from cart")
    @pytest.mark.parametrize("setup_products_in_cart", [[test_products[1], test_products[2]]], indirect=True)
    def test_remove_one_of_the_products_from_card_successfully(self, class_cart_client, remove_all_items_from_cart,
                                                               setup_products_in_cart):

        cart_items = class_cart_client.get_products_api().response_json["products"]

        product_to_remove = cart_items[0]
        initial_cart_totals = class_cart_client.get_products_api().response_json["totals"]

        class_cart_client.remove_product_api(cart_id=product_to_remove["cart_id"]). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.get_products_api(). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Cart). \
            assert_product_is_not_in_cart(product_to_remove["product_id"]). \
            assert_cart_total_decreased(initial_cart_totals, product_to_remove)


@allure.feature("Cart")
@allure.story("Remove from cart negative")
class TestRemoveFromCartNegative:
    @allure.title("Remove non existent product")
    @pytest.mark.xfail(reason="Expect 404 not found")
    @pytest.mark.parametrize("cart_id", [100015])
    def test_remove_from_cart_non_existent_cart_item(self, cart_id, class_cart_client, remove_all_items_from_cart):

        class_cart_client.remove_product_api(cart_id=cart_id). \
            assert_status_code(HTTPStatus.NOT_FOUND). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

    @allure.title("Remove product from cart invalid cart id")
    @pytest.mark.parametrize("cart_id", [-1, 0, ''])
    @pytest.mark.xfail(reason="Expect 404 not found")
    def test_remove_from_cart_invalid_cart_id(self, cart_id, class_cart_client):
        class_cart_client.remove_product_api(cart_id=cart_id). \
            assert_status_code(HTTPStatus.NOT_FOUND). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

    @allure.title("Remove product from cart with no cart_id key")
    @pytest.mark.xfail(reason="Expect 404 not found")
    def test_remove_from_cart_no_cart_id_key(self, class_cart_client):
        class_cart_client.remove_product_api(). \
            assert_status_code(HTTPStatus.NOT_FOUND). \
            validate_schema(Error)
