from flask import Flask, render_template
from config.config import Config
from functions import *


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    for config in app.config:
        print(config)
        print(app.config[config])
    # products = get_products_array()
    # print(products)

    # app.run(debug=True)
