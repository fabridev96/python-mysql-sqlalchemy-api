from flask import Flask
from flask_sqlalchemy import flask_SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(70), unique=True)
    descripcion = db.Column(db.String(255))

    def __init__(self, titulo, descripcion)
        self.titulo = titulo
        self.descripcion = descripcion
    
db.create_all()

class TareaSchema(ma.Schema)
    class Meta:
        fields: ('id', 'titulo', 'descripcion')

tarea_schema = TareaSchema()
tareas_schema = TareaSchema(many=True)