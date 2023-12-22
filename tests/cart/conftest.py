import os
import hashlib
from socket import socket

import mysql.connector as mysql
import pytest
from configuration import TEST_DATA_PATH, MYSQL_CREDENTIALS
from src.utilities.utilities import csv_reader


@pytest.fixture(scope="class")
def taxes_reset_to_zero(db_connection):
    taxes_table = "oc_tax_rate"
    cursor = db_connection.cursor(dictionary=True)

    select_taxes_query = f"SELECT tax_rate_id, rate FROM {taxes_table}"
    cursor.execute(select_taxes_query)

    tax_rates = cursor.fetchall()

    update_taxes_query = f"UPDATE {taxes_table} SET rate = %s"
    cursor.execute(update_taxes_query, (0.0,))

    db_connection.commit()

    yield

    for tax_rate in tax_rates:
        restore_taxes_query = f"UPDATE {taxes_table} SET rate = %s WHERE tax_rate_id = %s"
        cursor.execute(restore_taxes_query, (tax_rate["rate"], tax_rate["tax_rate_id"]))

    db_connection.commit()


@pytest.fixture()
def remove_all_items_from_cart(db_connection, api_token):
    def remove_all():
        delete_query = "DELETE FROM oc_cart WHERE session_id=%s"
        db_connection.cursor().execute(delete_query, (api_token,))
        db_connection.commit()

    remove_all()
    yield
    remove_all()


# @pytest.fixture(scope="session", autouse=True)
# def setup_db_products_deprecated(db_connection, request):
#     products_tables = "oc_product", "oc_product_description", "oc_product_to_store", "oc_product_to_category"
#
#     def teardown():
#         select_query = "SELECT product_id FROM oc_product WHERE model LIKE %s"
#         cursor.execute(select_query, ("%testdata%",))
#         product_ids = cursor.fetchall()
#
#         product_ids_tuple = tuple(product_id[0] for product_id in product_ids)
#
#         for product_table in products_tables:
#             delete_query = f"DELETE FROM {product_table} WHERE product_id IN ({', '.join(['%s']*len(product_ids_tuple))})"
#             cursor.execute(delete_query, product_ids_tuple)
#
#     request.addfinalizer(teardown)
#
#     cursor = db_connection.cursor()
#     # должен создать новые продукты и получить их id, потом с этим id добавить данные в другие таблицы
#     # после создания каждого продукта добавить в другие таблицы
#
#     # создать товар сделать коммит
#     # получить список row_id
#     # использовать его в запросах дальше, подставлять на первое место
#     # по одному продукту, а не по одной таблице
#     product_ids = []
#     for product_table in products_tables[0]:
#         for row in csv_reader(filename=os.path.join(TEST_DATA_PATH, f"{product_table}.csv")):
#             columns_placeholder = ", ".join(row.keys())
#             values_placeholder = ", ".join(["%s"]*len(row))
#
#             import_query = f"INSERT INTO {product_table} ({columns_placeholder}) VALUES({values_placeholder})"
#             print("import_query = ", import_query)
#             cursor.execute(import_query, tuple(row.values()))
#             product_ids.append(cursor.lastrowid)
#
#     db_connection.commit()
#
#     for product_table in products_tables[1:]:
#         for row in csv_reader(filename=os.path.join(TEST_DATA_PATH, f"{product_table}.csv")):
#             columns_placeholder = ", ".join(row.keys())
#             values_placeholder = ", ".join(["%s"]*len(row.keys()))
#
#             import_query = f"INSERT INTO {product_table} ({columns_placeholder}) VALUES({values_placeholder})"
#             print("import_query = ", import_query)
#             cursor.execute(import_query, product_ids[k], tuple(row.values()))
#
#     db_connection.commit()
#
#     cursor.close()

@pytest.fixture(scope="session")
def setup_db_products(db_connection, request, logger):
    products_tables = "oc_product", "oc_product_description", "oc_product_to_store", "oc_product_to_category"

    def finalizer():
        select_query = "SELECT product_id FROM oc_product WHERE model LIKE %s"
        cursor.execute(select_query, ("%testdata%",))
        product_ids = cursor.fetchall()

        product_ids = tuple(product_id[0] for product_id in product_ids)
        logger.info(f"Delete products from db with product id {product_ids}")
        for product_table in products_tables:
            delete_query = f"DELETE FROM {product_table} WHERE product_id IN ({', '.join(['%s']*len(product_ids))})"
            cursor.execute(delete_query, product_ids)

        db_connection.commit()

    request.addfinalizer(finalizer)

    cursor = db_connection.cursor()
    for row in csv_reader(filename=os.path.join(TEST_DATA_PATH, f"products.csv")):
        # insert product columns
        product_columns = ["model", "sku", "upc", "ean", "jan", "isbn", "mpn", "location", "quantity",
                           "stock_status_id", "image", "manufacturer_id", "shipping", "price", "points", "tax_class_id",
                           "date_available", "weight", "weight_class_id", "length", "width", "height",
                           "length_class_id", "subtract", "minimum", "sort_order", "status", "viewed", "date_added",
                           "date_modified"]
        columns_placeholder = ", ".join(product_columns)
        values_placeholder = ", ".join(["%s"]*len(product_columns))
        values = tuple(row[column] for column in product_columns)

        product_query = f"INSERT INTO oc_product ({columns_placeholder}) VALUES({values_placeholder})"
        logger.info(f"query = {product_query}")
        cursor.execute(product_query, values)

        row["product_id"] = cursor.lastrowid

        # insert product description columns
        product_desc_columns = ["product_id", "language_id", "name", "description", "tag", "meta_title",
                                "meta_description", "meta_keyword"]
        columns_placeholder = ", ".join(product_desc_columns)
        values_placeholder = ", ".join(["%s"]*len(product_desc_columns))
        values = tuple(row[column] for column in product_desc_columns)

        product_desc_query = f"INSERT INTO oc_product_description ({columns_placeholder}) VALUES({values_placeholder})"
        logger.info(f"query = {product_desc_query}")
        cursor.execute(product_desc_query, values)

        # insert product category columns
        product_cat_columns = ["product_id", "category_id"]
        columns_placeholder = ", ".join(product_cat_columns)
        values_placeholder = ", ".join(["%s"]*len(product_cat_columns))
        values = tuple(row[column] for column in product_cat_columns)

        product_cat_query = f"INSERT INTO oc_product_to_category ({columns_placeholder}) VALUES({values_placeholder})"
        logger.info(f"query = {product_cat_query}")
        cursor.execute(product_cat_query, values)

        # insert product store_id columns
        product_store_columns = ["product_id", "store_id"]
        columns_placeholder = ", ".join(product_store_columns)
        values_placeholder = ", ".join(["%s"]*len(product_store_columns))
        values = tuple(row[column] for column in product_store_columns)

        product_store_query = f"INSERT INTO oc_product_to_store ({columns_placeholder}) VALUES({values_placeholder})"
        logger.info(f"query = {product_store_query}")
        cursor.execute(product_store_query, values)

    db_connection.commit()


@pytest.fixture()
def test_products(db_connection):
    cursor = db_connection.cursor()
    products_query = "SELECT product_id FROM oc_product WHERE model LIKE %s"
    cursor.execute(products_query, ("%testdata%",))
    product_ids = cursor.fetchall()

    return [{"product_id": product_id[0], "quantity": 1} for product_id in product_ids]


# def pytest_generate_tests(metafunc):
#
#     if 'product_data' not in metafunc.fixturenames:
#         return
#
#     if metafunc.function.__name__ == "test_add_to_cart":
#         print("Get test data")
#         connection = mysql.connect(**MYSQL_CREDENTIALS)
#         with connection:
#             cursor = connection.cursor()
#             products_query = "SELECT product_id FROM oc_product WHERE model LIKE %s LIMIT 1"
#             cursor.execute(products_query, ("%testdata%",))
#             product_ids = cursor.fetchall()
#
#             data = [{"product_id": product_id[0], "quantity": 1} for product_id in product_ids]
#
#             metafunc.parametrize("product_data", data[0])
#
#     elif metafunc.function.__name__ == "test_add_to_cart2":
#         connection = mysql.connect(**MYSQL_CREDENTIALS)
#         with connection:
#             cursor = connection.cursor()
#             products_query = "SELECT product_id FROM oc_product WHERE model LIKE %s"
#             cursor.execute(products_query, ("%testdata%",))
#             product_ids = cursor.fetchall()
#
#             data = [{"product_id": product_id[0], "quantity": 1} for product_id in product_ids]
#
#             metafunc.parametrize("product_data", data)


@pytest.fixture()
def create_admin_user(db_connection, faker, request):
    def teardown():
        tquery = "DELETE FROM oc_user WHERE username=%s"
        db_connection.cursor().execute(tquery, (username,))
        db_connection.commit()
    request.addfinalizer(teardown)

    query = "INSERT INTO oc_user " \
            "(user_group_id, username, password, salt, firstname, lastname, email, image, code, ip, status," \
            " date_added) " \
            "VALUES (1, %s, %s, %s, %s, %s, %s, '', '', %s, 1, NOW());"

    username = faker.profile(fields=["username"])["username"]  # faker.safe_email().split("@")[0]
    test_password = "admin!32"
    salt = "VGNUpQvgV"
    ip = socket.gethostbyname(socket.gethostname())

    db_connection.execute(query, (
        username,
        hashlib.md5(test_password.encode()).hexdigest(),
        salt,
        faker.first_name(),
        faker.last_name(),
        faker.safe_email(),
        ip
    ))

    return username, test_password
