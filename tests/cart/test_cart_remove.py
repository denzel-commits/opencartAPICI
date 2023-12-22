import random
from http import HTTPStatus

import allure
import pytest

from src.classes.data_manager import DataManager
from src.pydantic_schemas.cart import Cart
from src.pydantic_schemas.error import Error
from src.pydantic_schemas.success import Success


@allure.feature("Cart")
@allure.story("Remove from cart")
class TestRemoveFromCart:
    test_products = DataManager().get_test_products_from_db()

    @allure.title("Remove product from cart parametrized")
    @pytest.mark.parametrize("product_id, quantity, price", [random.choice(test_products)])
    def test_remove_from_card_successfully(self, product_id, quantity, price, class_cart_client,
                                           remove_all_items_from_cart):
        data = {
            'product_id': product_id,
            'quantity': quantity
        }

        class_cart_client.add_product_api(product_data=data). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        cart_items = class_cart_client.get_products_api().response_json["products"]

        class_cart_client.remove_product_api(cart_id=cart_items[0]["cart_id"]).\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.get_products_api().\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Cart).\
            assert_product_is_not_in_cart(data)

    @allure.title("Remove several products from cart")
    @pytest.mark.parametrize("product_id, quantity, price", [*test_products])
    def test_remove_from_card_successfully_double(self, product_id, quantity, price, class_cart_client,
                                                  remove_all_items_from_cart):
        data = {
            'product_id': product_id,
            'quantity': quantity
        }

        class_cart_client.add_product_api(product_data=data). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.add_product_api(product_data=data). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        cart_items = class_cart_client.get_products_api().response_json["products"]

        class_cart_client.remove_product_api(cart_id=cart_items[0]["cart_id"]). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.get_products_api(). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Cart). \
            assert_product_is_not_in_cart(data)


@allure.feature("Cart")
@allure.story("Remove from cart invalid cart items")
class TestRemoveFromCartNegative:
    @allure.title("Remove non existent product")
    @pytest.mark.parametrize("cart_id", [100015])
    def test_remove_from_cart_non_existent_cart_item(self, cart_id, class_cart_client, remove_all_items_from_cart):

        class_cart_client.remove_product_api(cart_id=cart_id). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

    @allure.title("Remove product from cart invalid cart id")
    @pytest.mark.parametrize("cart_id", [-1, 0, ''])
    def test_remove_from_cart_invalid_cart_id(self, cart_id, class_cart_client):
        class_cart_client.remove_product_api(cart_id=cart_id). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

    @allure.title("Remove product from cart without cart_id key")
    def test_remove_from_cart_no_cart_id_key(self, class_cart_client):
        class_cart_client.remove_product_api(). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Error)
