from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

UPLOAD_FOLDER_IMG = os.path.abspath('eduven/static/img/uploat/')

#Configuracion
app.config.from_object('config.DevelopmentConfig')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_IMG
db = SQLAlchemy(app)

#Importar vistas
from eduven.views.auth import auth
app.register_blueprint(auth)

from eduven.views.inventory import invent
app.register_blueprint(invent)

from eduven.views.index import home
app.register_blueprint(home)

from eduven.views.user import user
app.register_blueprint(user)

db.create_all()