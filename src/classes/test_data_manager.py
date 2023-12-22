import random

import mysql.connector as mysql

from configuration import MYSQL_CREDENTIALS


class TestDataManager:
    def __init__(self):
        self.connection = mysql.connect(**MYSQL_CREDENTIALS)
        self.cursor = self.connection.cursor(dictionary=True)

        self.db_prefix = "oc_"
        self.product_table = "product"
        self.currency_table = "currency"

    def get_test_products_from_db(self) -> list[tuple]:
        with self.connection:
            select_query = f"SELECT product_id, price FROM {self.db_prefix}{self.product_table} " \
                           f"WHERE model LIKE %s AND quantity > %s LIMIT 3"
            self.cursor.execute(select_query, ("%Product%", 7))
            products = self.cursor.fetchall()

            return [(product["product_id"], random.randint(1, 20), float(product["price"])) for product in products]

    def get_invalid_test_products_from_db(self) -> list[tuple]:
        with self.connection:
            select_query = f"SELECT product_id FROM {self.db_prefix}{self.product_table} " \
                           f"WHERE model LIKE %s AND quantity > %s LIMIT 3"
            self.cursor.execute(select_query, ("%Product%", 7))
            products = self.cursor.fetchall()

            quantity = [-1, 0, '']

            return [(product["product_id"], quantity.pop(0)) for product in products]

    def get_currencies_from_db(self) -> list[str]:
        with self.connection:
            select_query = f"SELECT code FROM {self.db_prefix}{self.currency_table}"
            self.cursor.execute(select_query)
            currency_codes = self.cursor.fetchall()

            return [code[0] for code in currency_codes]
