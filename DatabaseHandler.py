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

    def select_products(self, product_id=None):
        if product_id:
            sql_query = "SELECT * FROM products WHERE id = {};".format(product_id)
        else:
            sql_query = "SELECT * FROM products ORDER BY id;"

        return self.query_db(sql_query)

    def select_current_prices(self, product_id=None):
        if product_id:
            sql_query = 'SELECT * FROM current_prices WHERE product_id = {};'.format(product_id)
        else:
            sql_query = 'SELECT * FROM current_prices ORDER BY id;'

        return self.query_db(sql_query)

    def update_product(self):
        raise NotImplementedError("Need to be implemented")

    def delete_product(self, product_id=None):
        if product_id is None:
            return ['error', 'ID not passed']

        exists = self.select_products(product_id)
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
        :param store: name of store to be inserted
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

        product_id = scraped_data['id']

        exists = self.select_products(product_id)
        if not exists:
            print('ERROR 00x1: Product ID received does not exist!')
            return ['error', 'ID does not exist in database']

        exists_current = self.select_current_prices(product_id)

        if not exists_current:
            print('Product not yet logged. Inserting new row.')

            for store in stores_analyzed:
                self.cursor.execute("INSERT INTO current_prices ("
                                     "product_id, "
                                     "current_price, "
                                     "current_price_cash,"
                                     "installments, "
                                     "store"
                                     ") VALUES (%s, %s, %s, %s, %s)",
                                     (
                                        product_id,
                                        scraped_data[store]['price'],
                                        scraped_data[store]['price_cash'],
                                        scraped_data[store]['installments'],
                                        store
                                     ))

        else:
            print('Product already logged. Updating prices from last scraping.')
            for store in stores_analyzed:
                self.cursor.execute("UPDATE public.current_prices "
                                    "SET product_id = %s, "
                                     "current_price = %s, "
                                     "current_price_cash = %s,"
                                     "installments = %s, "
                                     "store = %s, "
                                     "last_update = now() "
                                     "WHERE product_id = %s "
                                     "AND store = %s;",
                                    (
                                        product_id,
                                        scraped_data[store]['price'],
                                        scraped_data[store]['price_cash'],
                                        scraped_data[store]['installments'],
                                        store,
                                        product_id,
                                        store
                                    ))

        return 'ok'

    def products_info_and_prices(self):
        """
        This method returns the correct array to be used by jinja when loading the index page
        :return:
        """

        query = "SELECT prods.id, prods.product_name, prods.product_type, prods.product_description, " \
                     "best.price AS best_price, best.price_cash AS best_cash, best.installments AS best_installment, " \
                     "best.store AS best_store " \
                "FROM products AS prods " \
                "JOIN (SELECT DISTINCT ON (id_product) *  " \
                "FROM best_prices " \
                "ORDER BY id_product, date DESC) AS best " \
                "ON prods.id = best.id_product;"

        db_return = self.query_db(query)

        complete_array = dict()
        current_prices = self.create_current_prices_array()
        for row in db_return:
            complete_array[row['id']] = dict({
                'product_name': row['product_name'],
                'product_type': row['product_type'],
                'product_description': row['product_description'],
                'best_price': row['best_price'],
                'best_cash': row['best_cash'],
                'best_installment': row['best_installment'],
                'best_store': row['best_store'],
                'current_prices': current_prices[row['id']]
                }
            )

        return complete_array

    def create_current_prices_array(self):
        """
        This method returns array like      item[ID][store] = prices[cash/installment/price] # TODO needs better comment
        :return:
        """
        current_prices = dict()

        current_prices_db_data = self.select_current_prices()

        for row in current_prices_db_data:

            if not current_prices.get(row['product_id']):
                current_prices[row['product_id']] = dict()
            current_prices[row['product_id']][row['store']] = dict()
            current_prices[row['product_id']][row['store']]['price'] = row['current_price']
            current_prices[row['product_id']][row['store']]['price_cash'] = row['current_price_cash']
            current_prices[row['product_id']][row['store']]['installments'] = row['installments']
            current_prices[row['product_id']][row['store']]['last_update'] = row['last_update']

        return current_prices

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
