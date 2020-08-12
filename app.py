from flask import Flask, request, jsonify
from sqlalchemy import create_engine


app = Flask(__name__)

app.config['SECRET_KEY'] = 'YOUR-SECRET'
def connect_db():
    DATABASE_URL = "postgres+psycopg2://postgres:yogesh5201@localhost/postgres"
    return create_engine(DATABASE_URL)


db = connect_db()


from routes import *


if __name__ == '__main__':
    app.run(debug=True)