from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configuracion
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

#Importar vistas
from eduven.views.auth import auth
app.register_blueprint(auth)

from eduven.views.inventory import invent
app.register_blueprint(invent)

db.create_all()