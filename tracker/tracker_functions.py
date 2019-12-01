def clear_string(soup_price):
    price_string = str(soup_price).replace(" ", "").replace("\n", "").replace("\t", "")

    return price_string

