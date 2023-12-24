from http import HTTPStatus

import allure
import pytest

from src.utilities.data_manager import DataManager
from src.enums.routes import Routes
from src.pydantic_schemas.cart import Cart
from src.pydantic_schemas.success import Success
from src.pydantic_schemas.error import Error


@allure.feature("Cart")
@allure.story("Add to cart")
class TestAddToCart:
    test_products = DataManager().get_test_products_from_db()

    @allure.title("Add product to cart base session")
    @pytest.mark.session
    @pytest.mark.skip(reason="session test case")
    @pytest.mark.parametrize("product_id, quantity, price", [test_products[0]])
    def test_add_to_cart(self, product_id, quantity, price, opencart_base_url, api_token, api_session):
        params = {"api_token": api_token}
        data = {
            "product_id": product_id,
            "quantity": quantity
        }
        print(f"data = {data}")
        add_result = api_session.post(f"{opencart_base_url}/{Routes.CART}/add", params=params, data=data)

        print(add_result.text)

        check_result = api_session.post(f"{opencart_base_url}/{Routes.CART}/products", params=params)
        print(api_session.cookies.get_dict())
        print(check_result.text)

        assert True

    @allure.title("Add product to cart base session2")
    @pytest.mark.session
    @pytest.mark.skip(reason="session test case")
    @pytest.mark.parametrize("product_id, quantity, price", [*test_products])
    def test_add_to_cart2(self, product_id, quantity, price, opencart_base_url, api_token, api_session):
        params = {"api_token": api_token}
        data = {
            "product_id": product_id,
            "quantity": quantity
        }

        add_result = api_session.post(f"{opencart_base_url}/{Routes.CART}/add", params=params, data=data)

        print(add_result.text)

        check_result = api_session.post(f"{opencart_base_url}/{Routes.CART}/products", params=params)
        print(api_session.cookies.get_dict())
        print(check_result.text)

        assert True

    @allure.title("Add product to cart base")
    @pytest.mark.smoke
    @pytest.mark.parametrize("product_id, quantity, price", [test_products[0]])
    def test_add_to_cart_successfully_added(self, product_id, quantity, price, class_cart_client,
                                            remove_all_items_from_cart, taxes_reset_to_zero):
        data = {
            'product_id': product_id,
            'quantity': quantity
        }

        class_cart_client.add_product_api(product_data=data).\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Success).\
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.get_products_api().\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Cart).\
            assert_product_is_in_cart(data). \
            assert_product_quantity_in_cart(data). \
            assert_cart_total(data, price)

    @allure.title("Add product to cart parametrized")
    @pytest.mark.parametrize("product_id, quantity, price", [*test_products])
    def test_add_to_cart_successfully_added_multi(self, product_id, quantity, price, class_cart_client,
                                                  remove_all_items_from_cart, taxes_reset_to_zero):
        data = {
            'product_id': product_id,
            'quantity': quantity
        }

        class_cart_client.add_product_api(product_data=data).\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Success).\
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.get_products_api().\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Cart).\
            assert_product_is_in_cart(data). \
            assert_product_quantity_in_cart(data). \
            assert_cart_total(data, price)

    @allure.title("Add product to cart twice")
    @pytest.mark.parametrize("product_id, quantity, price", [*test_products])
    def test_add_to_cart_successfully_added_twice(self, product_id, quantity, price, class_cart_client,
                                                  remove_all_items_from_cart, taxes_reset_to_zero):
        data = {
            'product_id': product_id,
            'quantity': quantity
        }

        class_cart_client.add_product_api(product_data=data).\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Success).\
            assert_success_message("Success: You have modified your shopping cart!")

        class_cart_client.add_product_api(product_data=data).\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Success).\
            assert_success_message("Success: You have modified your shopping cart!")

        expected_data = {
            'product_id': product_id,
            'quantity': quantity*2
        }

        class_cart_client.get_products_api().\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Cart).\
            assert_product_is_in_cart(expected_data). \
            assert_product_quantity_in_cart(expected_data). \
            assert_cart_total(expected_data, price)


@allure.feature("Cart")
@allure.story("Add to cart negative")
class TestAddToCartNegative:
    test_products = DataManager().get_invalid_test_products_from_db()

    @allure.title("Add product to cart not existing product")
    @pytest.mark.parametrize("product_id, quantity", [(10001, 1), (0, 1)])
    def test_add_to_cart_non_existent_product(self, product_id, quantity, class_cart_client, remove_all_items_from_cart):
        data = {
            "product_id": product_id,
            "quantity": quantity
        }

        class_cart_client.add_product_api(product_data=data). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Error). \
            assert_error_message("Product can not be bought from the store you have choosen!")

        class_cart_client.get_products_api(). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Cart).\
            assert_product_is_not_in_cart(data["product_id"])

    @allure.title("Add product to cart with invalid product id")
    @pytest.mark.parametrize("product_id, quantity", [(-6, 1), (0, 1)])
    def test_add_to_cart_invalid_product(self, product_id, quantity, class_cart_client, remove_all_items_from_cart):
        data = {
            "product_id": product_id,
            "quantity": quantity
        }

        class_cart_client.add_product_api(product_data=data). \
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Error).\
            assert_error_message("Product can not be bought from the store you have choosen!")

        class_cart_client.get_products_api(). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Cart).\
            assert_product_is_not_in_cart(data["product_id"])

    @allure.title("Add product to cart with invalid quantity")
    @pytest.mark.xfail(reason="Returned: Success: You have modified your shopping cart - but was not added to cart")
    @pytest.mark.parametrize("product_id, quantity", [*test_products])
    def test_add_to_cart_invalid_quantity(self, product_id, quantity, class_cart_client,
                                          remove_all_items_from_cart):
        data = {
            'product_id': product_id,
            'quantity': quantity
        }

        class_cart_client.add_product_api(product_data=data).\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Success).\
            assert_success_message("Success: You have modified your shopping cart!")

        expected_data = {
            'product_id': product_id,
            'quantity': 1
        }
        class_cart_client.get_products_api(). \
            assert_status_code(HTTPStatus.OK). \
            validate_schema(Cart).\
            assert_product_is_in_cart(expected_data)

    @allure.title("Add product to cart unauthorized")
    @pytest.mark.parametrize("product_id, quantity", [test_products[0]])
    def test_add_to_cart_unauthorized(self, product_id, quantity, class_cart_client_unauthorized):
        data = {
            'product_id': product_id,
            'quantity': quantity
        }

        class_cart_client_unauthorized.add_product_api(product_data=data).\
            assert_status_code(HTTPStatus.OK).\
            validate_schema(Error).\
            assert_warning_message("Warning: You do not have permission to access the API!")
