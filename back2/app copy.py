from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Configurar la conexión con la base de datos MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='admin',
        password='Pa$$w0rd',
        database='conedental'
    )
    return connection

# Ruta para obtener las clínicas
@app.route('/clinicas', methods=['GET'])
def get_clinicas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clinicas')
    clinicas = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(clinicas)

# Ruta para obtener los pacientes
@app.route('/pacientes', methods=['GET'])
def get_pacientes():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM pacientes')
    pacientes = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(pacientes)

# Ruta para obtener los doctores
@app.route('/doctores', methods=['GET'])
def get_doctores():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM doctores')
    doctores = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(doctores)

# Ruta para obtener los materiales dentales
@app.route('/material_dental', methods=['GET'])
def get_material_dental():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM material_dental')
    material = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(material)

# Ruta para obtener las prótesis dentales
@app.route('/protesis_dentales', methods=['GET'])
def get_protesis_dentales():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM protesis_dentales')
    protesis = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(protesis)

# Ruta para obtener los proveedores dentales
@app.route('/proveedores_dentales', methods=['GET'])
def get_proveedores_dentales():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM proveedores_dentales')
    proveedores = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(proveedores)

# Ruta para obtener los tratamientos
@app.route('/tratamientos', methods=['GET'])
def get_tratamientos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tratamientos')
    tratamientos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(tratamientos)

# Ruta para obtener los tratamientos de un paciente
@app.route('/pacientes_tratamientos', methods=['GET'])
def get_pacientes_tratamientos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Ajustamos los nombres de las columnas en el JOIN
    cursor.execute('''
        SELECT pacientes.nombre AS paciente, tratamientos.nombre AS tratamiento
        FROM pacientes
        JOIN pacientes_tratamientos ON pacientes.id_paciente = pacientes_tratamientos.id_paciente
        JOIN tratamientos ON pacientes_tratamientos.id_tratamiento = tratamientos.id_tratamiento
    ''')
    
    tratamientos = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(tratamientos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
