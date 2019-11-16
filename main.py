from flask import Flask, render_template
from functions import *


app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html', products_dict)


if __name__ == "__main__":
    products_dict = generate_prices_dict()
    app.run(debug=True)
