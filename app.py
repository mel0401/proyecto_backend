
# Importa las clases Flask, jsonify y request del módulo flask
from flask import Flask, jsonify, request
# Importa la clase CORS del módulo flask_cors
from flask_cors import CORS
# Importa la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa la clase Marshmallow del módulo flask_marshmallow
from flask_marshmallow import Marshmallow

app=Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1:3306/promociones'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS']=False
db= SQLAlchemy(app)
ma=Marshmallow(app)

class Producto(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    foto=db.Column(db.String(400))
    descripcion=db.Column(db.String(200))
    precio=db.Column(db.Integer)

    def __init__(self, nombre, foto, descripcion, precio):
        self.nombre = nombre
        self.foto = foto
        self.descripcion = descripcion
        self.precio = precio

with app.app_context():
    db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id', 'nombre', 'foto', 'descripcion', 'precio')

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

@app.route('/productos', methods=['GET'])
def get_Productos():
    all_productos = Producto.query.all()
    result = productos_schema.dump(all_productos)

    return jsonify(result)

@app.route("/productos/<id>", methods=["GET"])
def get_producto(id):
    producto = Producto.query.get(id)  
    return producto_schema.jsonify(producto)

@app.route("/productos/<id>", methods=["DELETE"])
def delete_producto(id):
    producto = Producto.query.get(id)  
    db.session.delete(producto)  
    db.session.commit()  
    return producto_schema.jsonify(producto)

@app.route("/productos", methods=["POST"])  # Endpoint para crear un producto
def create_producto():
    nombre = request.json["nombre"] 
    foto = request.json["foto"]  
    descripcion = request.json["descripcion"]  
    precio = request.json["precio"]  
    new_producto = Producto(nombre, foto, descripcion, precio)  
    db.session.add(new_producto)  
    db.session.commit()  
    return producto_schema.jsonify(new_producto)

@app.route("/productos/<id>", methods=["PUT"])
def update_producto(id):
    producto = Producto.query.get(id)

    nombre = request.json["nombre"]
    foto = request.json ["foto"]
    descripcion = request.json["descripcion"]
    precio = request.json ["precio"]

    producto.nombre = nombre
    producto.foto = foto
    producto.descripcion = descripcion
    producto.precio = precio

    db.session.commit()  # Guarda los cambios en la base de datos
    return producto_schema.jsonify(producto)

# Programa Principal
if __name__ == "__main__":
    app.run(debug=True, port=5000)