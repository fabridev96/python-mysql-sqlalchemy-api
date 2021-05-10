from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Tareas(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(70), unique=True)
    descripcion = db.Column(db.String(255))

    def __init__(self, titulo, descripcion):
        self.titulo = titulo
        self.descripcion = descripcion
    
db.create_all()


class TareaSchema(ma.Schema):
    class Meta:
        fields: ('id', 'titulo', 'descripcion')

tarea_schema = TareaSchema()
tareas_schema = TareaSchema(many=True)

@app.route('/', methods=['GET'])
def index():
    return "Hola, bienvenide a la API Python, Flask, MySQL, SQLAlchemy"

"""
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    titulo = request.json['titulo']
    descripcion = request.json['descripcion']
    nueva_tarea = Tareas(titulo, descripcion)
    db.session.add(nueva_tarea)
    db.session.commit()
    return tarea_schema.jsonify(nueva_tarea)
"""

@app.route('/tareas', methods=['POST'])
def crear_tarea():

    try:
        titulo = request.json['titulo']
        descripcion = request.json['descripcion']
    except:
        return "Hubo un error al procesar los datos solicitados"
    
    try:
        nueva_tarea = Tareas(titulo, descripcion)
        db.session.add(nueva_tarea)
        db.session.commit()
        return tarea_schema.jsonify(nueva_tarea)
    except:
        return "Hubo un error al crear la nueva tarea"


@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    tareas = Tareas.query.all()
    resultado = tareas_schema.dump(tareas)
    return jsonify(resultado)

"""
@app.route('/tareas/<id>', methods=['PUT'])
def actualizar_tarea(id):
    return id
    tarea = Tareas.query.get(id)
    titulo = request.json['titulo']
    descripcion = request.json['descripcion']
    tarea.titulo = titulo
    tarea.descripcion = descripcion
    db.session.commit()
    return tarea_schema.jsonify(tarea)
"""

@app.route('/tareas/<id>', methods=['PUT'])
def actualizar_tarea(id):
    try:
        tarea = Tareas.query.get(id)
        titulo = request.json['titulo']
        descripcion = request.json['descripcion']
    except:
        return "Error al obtener los datos obtenidos por JSON"

    try:
        tarea.titulo = titulo
        tarea.descripcion = descripcion
        db.session.commit()
        return tarea_schema.jsonify(tarea)
    except:
        return "Error al actualizar la tarea"

@app.route('/tareas/<id>', methods=['GET'])
def obtener_tarea(id):
    tarea = Tareas.query.get(id)
    return tarea_schema.jsonify(tarea)

@app.route('/tareas/<id>', methods=['DELETE'])
def eliminar_tarea(id):
    try:
        tarea = Tareas.query.get(id)
        db.session.delete(tarea)
        db.session.commit()
        return tarea_schema.jsonify(tarea)
    except:
        return "Hubo un error al eliminar la tarea"

if __name__ == '__main__':
    app.run(debug=True)