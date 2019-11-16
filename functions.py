import configparser


def get_ini():
    ini_data = configparser.ConfigParser()
    ini_data.read_file(open('products.ini'))

    return ini_data

