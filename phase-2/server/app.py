from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin

# Code help: https://webdamn.com/create-restful-api-using-python-mysql/
# Create a new Flask app and enable CORS on it
app = Flask(__name__)
CORS(app)

def create_response(message, code):
    response = jsonify(message)
    response.status_code = code
    return response

def create_stdmsg(message, code):
    message = {
        "message": message,
        "status": code,
    }
    return message
