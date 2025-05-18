from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = '23iom23r2-jd2j0sj2r932jm390-rh2893ndr92'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.views import homepage
from app.models import Contato


