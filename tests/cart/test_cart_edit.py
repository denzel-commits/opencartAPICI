from http import HTTPStatus

import allure
import pytest

from src.utilities.data_manager import DataManager
from src.pydantic_schemas.cart import Cart
from src.pydantic_schemas.error import Error
from src.pydantic_schemas.success import Success


@allure.feature("Cart")
@allure.story("Edit cart item")
class TestEditCart:
    test_products = DataManager().get_test_products_from_db(quantity=3)

    @allure.title("Decrease the quantity of a single product in cart")
    @pytest.mark.parametrize("setup_products_in_cart", [test_products[0]], indirect=True)
    def test_decrease_single_product_from_card_successfully(self, class_cart_client, remove_all_items_from_cart,
                                                            taxes_reset_to_zero, setup_products_in_cart):

        decrease_value = 1
        cart = class_cart_client.get_products_api().response_json

        product_to_edit = cart["products"][0]
        new_quantity = int(product_to_edit["quantity"]) - decrease_value

        initial_cart_totals = cart["totals"]

        data = {
            "key": cart["products"][0]["cart_id"],
            "quantity": new_quantity
        }

        class_cart_client.edit_product_api(product_data=data).\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.get_products_api().\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Cart).\
            assert_product_quantity_in_cart({"product_id": product_to_edit["product_id"],
                                             "quantity": new_quantity}).\
            assert_cart_total_decreased(initial_cart_totals, {"price": product_to_edit["price"],
                                                              "quantity": decrease_value})

    @allure.title("Increase the quantity of a single product in cart")
    @pytest.mark.parametrize("setup_products_in_cart", [test_products[0]], indirect=True)
    def test_increase_single_product_from_card_successfully(self, class_cart_client, remove_all_items_from_cart,
                                                            taxes_reset_to_zero, setup_products_in_cart):
        increase_value = 1
        cart = class_cart_client.get_products_api().response_json

        product_to_edit = cart["products"][0]
        new_quantity = int(product_to_edit["quantity"]) + increase_value

        initial_cart_totals = cart["totals"]

        data = {
            "key": cart["products"][0]["cart_id"],
            "quantity": new_quantity
        }

        class_cart_client.edit_product_api(product_data=data). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.get_products_api(). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Cart). \
            assert_product_quantity_in_cart({"product_id": product_to_edit["product_id"],
                                             "quantity": new_quantity}). \
            assert_cart_total_increased(initial_cart_totals, {"price": product_to_edit["price"],
                                                              "quantity": increase_value})

    @allure.title("Decrease the quantity of one of the products in cart")
    @pytest.mark.parametrize("setup_products_in_cart", [[test_products[1], test_products[2]]], indirect=True)
    def test_decrease_one_of_the_products_from_card_successfully(self, class_cart_client, remove_all_items_from_cart,
                                                                 taxes_reset_to_zero, setup_products_in_cart):

        decrease_value = 1
        cart = class_cart_client.get_products_api().response_json

        product_to_edit = cart["products"][0]
        new_quantity = int(product_to_edit["quantity"]) - decrease_value

        initial_cart_totals = cart["totals"]

        data = {
            "key": cart["products"][0]["cart_id"],
            "quantity": new_quantity
        }

        class_cart_client.edit_product_api(product_data=data). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.get_products_api(). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Cart). \
            assert_product_quantity_in_cart({"product_id": product_to_edit["product_id"],
                                             "quantity": new_quantity}). \
            assert_cart_total_decreased(initial_cart_totals, {"price": product_to_edit["price"],
                                                              "quantity": decrease_value})

    @allure.title("Increase the quantity of one of the products in cart")
    @pytest.mark.parametrize("setup_products_in_cart", [[test_products[1], test_products[2]]], indirect=True)
    def test_increase_one_of_the_products_from_card_successfully(self, class_cart_client, remove_all_items_from_cart,
                                                                 taxes_reset_to_zero, setup_products_in_cart):
        increase_value = 1
        cart = class_cart_client.get_products_api().response_json

        product_to_edit = cart["products"][0]
        new_quantity = int(product_to_edit["quantity"]) + increase_value

        initial_cart_totals = cart["totals"]

        data = {
            "key": cart["products"][0]["cart_id"],
            "quantity": new_quantity
        }

        class_cart_client.edit_product_api(product_data=data). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.get_products_api(). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Cart). \
            assert_product_quantity_in_cart({"product_id": product_to_edit["product_id"],
                                             "quantity": new_quantity}). \
            assert_cart_total_increased(initial_cart_totals, {"price": product_to_edit["price"],
                                                              "quantity": increase_value})


@allure.feature("Cart")
@allure.story("Edit cart item negative")
class TestEditCartNegative:
    test_products = DataManager().get_test_products_from_db(quantity=3)

    @allure.title("Edit non existent product")
    @pytest.mark.xfail(reason="Expect 404 not found")
    @pytest.mark.parametrize("setup_products_in_cart", [[test_products[1], test_products[2]]], indirect=True)
    def test_edit_from_cart_non_existent_cart_item(self, class_cart_client, remove_all_items_from_cart,
                                                   setup_products_in_cart):
        cart_id = 100015

        data = {
            "key": cart_id,
            "quantity": 1
        }

        class_cart_client.edit_product_api(product_data=data). \
            assert_status_code(HTTPStatus.NOT_FOUND). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

    @allure.title("Edit product from cart invalid cart id")
    @pytest.mark.xfail(reason="Expect 404 not found")
    @pytest.mark.parametrize("setup_products_in_cart", [[test_products[1], test_products[2]]], indirect=True)
    def test_edit_from_cart_invalid_cart_id(self, class_cart_client, setup_products_in_cart):
        cart_id = 0

        data = {
            "key": cart_id,
            "quantity": 1
        }

        class_cart_client.edit_product_api(product_data=data). \
            assert_status_code(HTTPStatus.NOT_FOUND). \
            validate_schema(Success). \
            assert_success_message("Success: You have modified your shopping cart!")

    @allure.title("Edit product from cart with no cart_id key")
    @pytest.mark.xfail(reason="Expect 404 not found")
    def test_edit_from_cart_no_cart_id_key(self, class_cart_client):
        class_cart_client.remove_product_api(). \
            assert_status_code(HTTPStatus.NOT_FOUND). \
            validate_schema(Error)
