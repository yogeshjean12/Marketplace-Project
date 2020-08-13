from flask import Flask, request, jsonify, session
from sqlalchemy import create_engine



app = Flask(__name__)

app.config['SECRET_KEY'] = 'NOTHING-SECRET'

db = create_engine("postgres+psycopg2://postgres:yogesh5201@localhost/project")


from routes import *


if __name__ == '__main__':
    app.run(debug=