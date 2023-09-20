from decouple import config
from flask import Flask
app = Flask(__name__)
app.secret_key = config('secret_key', default="Is this unique enough?")