import configparser
import psycopg2.extras
from re import search
from static.static_vars import *


class DatabaseHandler:

    def __init__(self):
        # Grab db connection string values
        db_info = configparser.ConfigParser()
        db_info.read_file(open('config/db_info.ini'))
        self.db_info = db_info

        # Connect to DB and return connected cursor
        connection = psycopg2.connect(database=self.db_info.get('database_connection', 'database'),
                                      host=self.db_info.get('database_connection', 'host'),
                                      port=self.db_info.get('database_connection', 'port'),
                                      user=self.db_info.get('database_connection', 'username'),
                                      password=self.db_info.get('database_connection', 'password'))
        connection.autocommit = True
        connected_cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cursor = connected_cursor

    def query_db(self, select_statement):

        self.cursor.execute(select_statement)
        # TODO ADD ERROR HANDLING TRY EXCEPTION
        fetched_array = self.cursor.fetchall()

        return fetched_array

    def product_manager(self, form_data, product_id=None):
        """
        Function to add new products directly to database.

        :param product_id: if editing an already
        :param form_data: data submitted from user using the form product_editor.html
        :return: ok message # TODO improve return message
        """

        if product_id:
            self.cursor.execute("UPDATE public.products "
                                "SET product_type = %s, "
                                "product_name = %s, "
                                "product_description = %s, "
                                "link_kabum = %s, "
                                "link_pichau = %s, "
                                "link_terabyte = %s "
                                "WHERE id = %s;",
                                (
                                    form_data['product_type'],
                                    form_data['product_name'],
                                    form_data['product_desc'],
                                    self.trim_link(form_data['kabum_link']),
                                    self.trim_link(form_data['pichau_link']),
                                    self.trim_link(form_data['terabyte_link']),
                                    product_id
                                ))

        else:
            # TODO add function to trim links string of not needed parts of URL
            self.cursor.execute("INSERT INTO products ("
                                "product_type, "
                                "product_name, "
                                "product_description,"
                                "link_kabum, "
                                "link_pichau, "
                                "link_terabyte"
                                ") VALUES (%s, %s, %s, %s, %s, %s)",
                                (
                                    form_data['product_type'],
                                    form_data['product_name'],
                                    form_data['product_desc'],
                                    self.trim_link(form_data['kabum_link']),
                                    self.trim_link(form_data['pichau_link']),
                                    self.trim_link(form_data['terabyte_link'])
                                ))

        return 'ok'

    def select_all_products(self):
        sql = "SELECT * FROM products ORDER BY id;"
        return self.query_db(sql)

    def select_product_by_id(self, product_id):  # TODO MERGE THIS AND ABOVE INTO ONE USING DEFAULT
        sql = "SELECT * FROM products WHERE id = {}".format(product_id)
        return self.query_db(sql)

    def update_product(self):
        raise NotImplementedError("Need to be implemented")

    def delete_product(self, product_id=None):
        if product_id is None:
            return ['error', 'ID not passed']

        exists = self.select_product_by_id(product_id)
        if not exists:
            return ['error', 'ID does not exist in database']

        self.cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))

        return ['success', 'Entry successfully deleted']

    def grab_best_price(self, product_id):
        query = "SELECT price FROM best_prices WHERE id_product = {} ORDER BY date DESC".format(product_id)

        db_return = self.query_db(query)
        if not db_return:
            return 0
        else:
            current_best_price = db_return[0][0]  # First row, and first element
            return current_best_price

    def insert_best_price(self, product_id, best_price_dict, store):
        """
        This function is the only one that is gonna interact with best_prices table, no update will be done on the rows,
        that way it is possible to store the history of product price. Always add new best.

        :param product_id: id of product in table 'products'
        :param best_price_dict: contains data got from scraper, product name, price, price in cash, and installments
        :return: 'ok'
        """
        print('new best price')
        print(product_id)
        print(best_price_dict)

        db_return = self.cursor.execute("INSERT INTO best_prices ("
                                            "id_product, "
                                            "price, "
                                            "price_cash,"
                                            "installments, "
                                            "store"
                                            ") VALUES (%s, %s, %s, %s, %s)",
                                            (
                                                product_id,
                                                float(best_price_dict['price']),
                                                float(best_price_dict['price_cash']),
                                                best_price_dict['installments'],
                                                store
                                            ))
        if not db_return:
            return 'placeholder'
        else:
            return Exception

    def insert_current_prices(self, scraped_data):

        return 'ok'

    @staticmethod
    def trim_link(link_to_trim):
        """

        :param link_to_trim: URL to trim
        :return: only parts of that should go to database, removing parts that repeat for every product
        """
        print(link_to_trim)
        if 'kabum' in link_to_trim:
            try:
                trimmed_link = search(r"(\d{5,})", link_to_trim)[0]  # Grab only product code number
            except TypeError:
                trimmed_link = 'Invalid link given.'
        elif 'pichau' in link_to_trim:
            trimmed_link = link_to_trim.replace(pichau_base_url, '')
        elif 'terabyte' in link_to_trim:
            trimmed_link = link_to_trim.replace(terabyte_base_url, '')
        else:
            trimmed_link = 'Invalid link given.'

        return trimmed_link
