from flask import Flask
from flask_bootstrap import Bootstrap


app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = "Thisisasecret!"
bootstrap = Bootstrap(app)

from app import forms, views