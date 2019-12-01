from flask import Flask
from config.settings import Config
import os


template_dir = os.path.abspath('templates') + '/'
print(template_dir)

app = Flask(__name__, template_dir)
app.config.from_object(Config)
