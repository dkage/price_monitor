from re import findall


def clear_string(subject_string):
    cleared_string = str(subject_string).replace(" ", "").replace("\n", "").replace("\t", "")

    return cleared_string


def only_numbers(soup_price):
    cleared_string = clear_string(soup_price)

    # Grabs every number and joins then
    price_as_number = ''.join(findall(r'\d+', cleared_string))

    # This put price number with a dotted cent, ex:  1234 = 12.34
    price_dotted_cents = '{:.2f}'.format(int(price_as_number) / 100.)

    return price_dotted_cents
