from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jgvdfgjdf34gy43y3'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
my_secret = os.environ['DB_Secret']

Base = declarative_base()
Session = sessionmaker()

db_connection_string = "mysql+pymysql://"+my_secret+"@aws.connect.psdb.cloud/tria"
engine = create_engine(
  db_connection_string, 
  connect_args={
        "ssl": {
            "ssl_ca": "ca.pem",
        }
    }, echo=False)
Base.metadata.create_all(bind=engine)
Session.configure(bind=engine)
session = Session()

from tria import routes


