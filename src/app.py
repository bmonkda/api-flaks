from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

from config import config

app = Flask(__name__)

# CORS(app)
CORS (app, resources={r"/api/contactos/*": {"origins": "http://localhost"}})

conexion = MySQL(app)

@app.route('/')
def index():
    return 'Hola mundo'

@app.route('/api/contactos/', methods=['GET'])
def getAllContacts():
    try:
        cur = conexion.connection.cursor()
        sql = "SELECT * FROM contactos"
        cur.execute(sql)
        datos = cur.fetchall()
        contactos = []
        for contact in datos:
            contacto = {
                "id" : contact[0],
                "nombre" : contact[1],
                "apellido" : contact[2],
                "telefono" : contact[3],
                "direccion" : contact[4],
                "email" : contact[5]
            }
            contactos.append(contacto)
        return jsonify({
            'contactos': contactos,
            'message': 'Lista de contactos.',
            'status': 'success',
            'code_status': 200
        })

    except Exception as e:
        return jsonify({
            'message': 'Error al obtener la lista de contactos.',
            'status': 'error',
            'code_status': 500
        })

@app.route('/api/contactos/<id>/', methods=['GET'])
def getContact(id):
    try:
        cur = conexion.connection.cursor()
        sql = "SELECT * FROM contactos WHERE id = '{0}'".format(id)
        # print(sql)
        cur.execute(sql)
        data = cur.fetchone()
        # print(data)
        contacto = {}
        # print(contacto)
        if data != None:
            contacto = {
                "id" : data[0],
                "nombre" : data[1],
                "apellido" : data[2],
                "telefono" : data[3],
                "direccion" : data[4],
                "email" : data[5]
            }
            return jsonify({
                'contacto': contacto,
                'message': 'Contacto encontrado.',
                'status': 'success',
                'code_status': 200
            })
        else:
            return jsonify({
                'contacto': contacto,
                'message': 'Contacto no encontrado.',
                'status': 'success',
                'code_status': 200
            })
    except Exception as e:
        return jsonify({
            'message': 'Error al obtener el contacto.',
            'status': 'error',
            'error': str(e),
            'code_status': 500
        })

@app.route('/api/contactos/', methods=['POST'])
def storeContact():
    if 'id' in request.json:
        updateContact()
    else:
        createContact()
    return 'ok'

# @app.route('/api/contactos/', methods=['POST']) # esta línea se puede borrar. Se contempla en storeContact
def createContact():
    """ Guardar o salvar contacto """
    # return request.json['nombre']
    cur = conexion.connection.cursor()
    cur.execute("INSERT INTO contactos(nombre, apellido, telefono, direccion, email) VALUES(%s, %s, %s, %s, %s)",
            (request.json['nombre'], request.json['apellido'], request.json['telefono'], request.json['direccion'], request.json['email']))
    conexion.connection.commit()
    return 'Contacto Guardado'

@app.route('/api/contactos/', methods=['PUT']) # esta línea se puede borrar y funciona todo con POST en storeContact. La dejo para contemplar el método PUT 
def updateContact():
    """ Actualizar contacto """
    # return request.json['nombre']
    cur = conexion.connection.cursor()
    cur.execute("UPDATE contactos SET nombre = %s, apellido = %s, telefono = %s, direccion = %s, email = %s WHERE id = %s",
        (request.json['nombre'], request.json['apellido'], request.json['telefono'], request.json['direccion'], request.json['email'], request.json['id']))
    conexion.connection.commit()
    return 'Contacto Actualizado'




def pagina_no_encontrada(error):
    return 'Pagina no encontrada', 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
