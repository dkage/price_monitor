from app.flask_app import app
from app.routes import *
from functions import *

import os


if __name__ == "__main__":
    app.run(debug=True)
