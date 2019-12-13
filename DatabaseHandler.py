import configparser
import psycopg2.extras


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
        connected_cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cursor = connected_cursor

    def get_products_array(self):

        self.cursor.execute("SELECT * FROM products;")
        fetched_array = self.cursor.fetchall()

        return fetched_array

    def insert_new_product(self):
        return 'ok'

    def add_new_best_price(self):
        return 'ok'

    def update_product(self):
        return 'ok'