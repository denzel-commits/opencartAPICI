import random

import mysql.connector as mysql

from configuration import MYSQL_CREDENTIALS
from src.enums.tables import Tables


class DataManager:
    def __init__(self):
        self.connection = mysql.connect(**MYSQL_CREDENTIALS)
        self.cursor = self.connection.cursor(dictionary=True)

    def get_test_products_from_db(self, quantity=1) -> list[tuple]:
        with self.connection:
            select_query = f"SELECT product_id, price FROM {Tables.PREFIX}{Tables.PRODUCT} " \
                           f"WHERE model LIKE %s AND quantity > %s LIMIT 3"
            self.cursor.execute(select_query, ("%Product%", 7))
            products = self.cursor.fetchall()

            return [(product["product_id"], quantity, float(product["price"])) for product in products]

    def get_invalid_test_products_from_db(self) -> list[tuple]:
        with self.connection:
            select_query = f"SELECT product_id FROM {Tables.PREFIX}{Tables.PRODUCT} " \
                           f"WHERE model LIKE %s AND quantity > %s LIMIT 3"
            self.cursor.execute(select_query, ("%Product%", 7))
            products = self.cursor.fetchall()

            quantity = [-1, 0, '']

            return [(product["product_id"], quantity.pop(0)) for product in products]

    def get_currencies_from_db(self) -> list[str]:
        """
        not used
        Get currency codes from DB
        :return: list of currency codes
        """
        with self.connection:
            select_query = f"SELECT code FROM {Tables.PREFIX}{Tables.CURRENCY}"
            self.cursor.execute(select_query)
            currency_codes = self.cursor.fetchall()

            return [code["code"] for code in currency_codes]
