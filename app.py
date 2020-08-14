from flask import Flask, request, jsonify, session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker



app = Flask(__name__)

app.config['SECRET_KEY'] = 'YOUR-SECRET'

db = create_engine("postgres+psycopg2://postgres:yogesh5201@localhost/project")
db_session = scoped_session(sessionmaker(bind=db))

from routes import *


if __name__ == '__main__':
    app.run(debug=True)