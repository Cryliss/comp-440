from flask import Flask
from flask_cors import CORS, cross_origin

# Code help: https://webdamn.com/create-restful-api-using-python-mysql/
# Create a new Flask app and enable CORS on it
app = Flask(__name__)
CORS(app)
