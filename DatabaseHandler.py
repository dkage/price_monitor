import configparser
import psycopg2.extras
from re import search


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

    def select_from_db(self, select_statement):

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
            print('this is and edit')
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
                                    form_data['kabum_link'],
                                    form_data['pichau_link'],
                                    form_data['terabyte_link']
                                ))

        return 'ok'

    def select_all_products(self):
        sql = "SELECT * FROM products;"
        return self.select_from_db(sql)

    def select_product_by_id(self, product_id):  # TODO MERGE THIS AND ABOVE INTO ONE USING DEFAULT
        sql = "SELECT * FROM products WHERE id = {}".format(product_id)
        return self.select_from_db(sql)

    def add_new_best_price(self):
        raise NotImplementedError("Need to be implemented")

    def update_product(self):
        raise NotImplementedError("Need to be implemented")

    @staticmethod
    def trim_link(link_to_trim):
        """

        :param link_to_trim: URL to trim
        :return: only parts of that should go to database, removing parts that repeat for every product
        """

        if 'kabum' in link_to_trim:
            trimmed_link = search(r"(\d{5,})", link_to_trim)[0]  # Grab only product code number
        elif 'pichau' in link_to_trim:
            base_url = 'https://www.pichau.com.br/'
            trimmed_link = link_to_trim.replace(base_url, '')
        elif 'terabyte' in link_to_trim:
            base_url = 'https://www.terabyteshop.com.br/produto/'
            trimmed_link = link_to_trim.replace(base_url, '')
        else:
            trimmed_link = 'Invalid link given.'

        return trimmed_link
