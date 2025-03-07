from flask import Flask, jsonify, request
from flask_cors import CORS  # Importar CORS
import mysql.connector

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

# 🔹 Función para conectar con MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='admin',
        password='Pa$$w0rd',
        database='conedental'
    )

# 🔹 API: Obtener Clínicas
@app.route('/clinicas', methods=['GET'])
def get_clinicas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clinicas')
    clinicas = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(clinicas)

# 🔹 API: Obtener Pacientes
@app.route('/pacientes', methods=['GET'])
def get_pacientes():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM pacientes')
    pacientes = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(pacientes)

# 🔹 API: Obtener Doctores
@app.route('/doctores', methods=['GET'])
def get_doctores():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM doctores')
    doctores = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(doctores)

# 🔹 API: Obtener Citas
@app.route('/citas', methods=['GET'])
def get_citas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM citas')
    citas = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(citas)

# 🔹 API: Obtener Empleados
@app.route('/empleados', methods=['GET'])
def get_empleados():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM empleados')
    empleados = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(empleados)

# 🔹 API: Obtener Material Dental
@app.route('/material_dental', methods=['GET'])
def get_material_dental():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM material_dental')
    material = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(material)

# 🔹 API: Obtener Medicamentos
@app.route('/medicamentos', methods=['GET'])
def get_medicamentos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM medicamentos')
    medicamentos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(medicamentos)

# 🔹 API: Obtener Proveedores Dentales
@app.route('/proveedores_dentales', methods=['GET'])
def get_proveedores():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM proveedores_dentales')
    proveedores = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(proveedores)

# 🔹 API: Obtener Tratamientos
@app.route('/tratamientos', methods=['GET'])
def get_tratamientos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tratamientos')
    tratamientos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(tratamientos)

# 🔹 API: Obtener Pacientes en Tratamientos
@app.route('/pacientes_tratamientos', methods=['GET'])
def get_pacientes_tratamientos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM pacientes_tratamientos')
    pacientes_tratamientos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(pacientes_tratamientos)

# 🔹 API: Obtener Pacientes y Medicamentos
@app.route('/pacientes_medicamentos', methods=['GET'])
def get_pacientes_medicamentos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM pacientes_medicamentos')
    pacientes_medicamentos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(pacientes_medicamentos)

# 🔹 API: Obtener Tratamientos y Medicamentos
@app.route('/tratamientos_medicamentos', methods=['GET'])
def get_tratamientos_medicamentos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tratamientos_medicamentos')
    tratamientos_medicamentos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(tratamientos_medicamentos)

@app.route('/citas_por_doctores', methods=['GET'])
def get_citas_por_doctores():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.nombre AS doctor, COUNT(c.id_cita) AS total_citas 
        FROM citas c
        JOIN doctores d ON c.id_doctor = d.id_doctor
        GROUP BY d.nombre
    """)
    citas = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(citas)

@app.route('/pacientes_por_tratamientos', methods=['GET'])
def get_pacientes_por_tratamientos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.nombre AS tratamiento, COUNT(pt.id_paciente) AS total_pacientes 
        FROM pacientes_tratamientos pt
        JOIN tratamientos t ON pt.id_tratamiento = t.id_tratamiento
        GROUP BY t.nombre
    """)
    pacientes = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(pacientes)

# 🔹 API: Obtener Citas con Doctores y Pacientes
@app.route('/citas_detalladas', methods=['GET'])
def get_citas_detalladas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id_cita, c.fecha_hora, p.nombre AS paciente, d.nombre AS doctor, c.motivo 
        FROM citas c
        JOIN pacientes p ON c.id_paciente = p.id_paciente
        JOIN doctores d ON c.id_doctor = d.id_doctor
        ORDER BY c.fecha_hora DESC
    """)
    citas = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(citas)

# 🔹 API: Obtener Material Dental por Clínica
@app.route('/material_por_clinica', methods=['GET'])
def get_material_por_clinica():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.nombre AS clinica, COUNT(m.id_material) AS total_material 
        FROM material_dental m
        JOIN clinicas c ON m.id_clinica = c.id_clinica
        GROUP BY c.nombre
    """)
    materiales = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(materiales)

# 🔹 API: Obtener Empleados por Clínica
@app.route('/empleados_por_clinica', methods=['GET'])
def get_empleados_por_clinica():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.nombre AS clinica, COUNT(e.id_empleado) AS total_empleados 
        FROM empleados e
        JOIN clinicas c ON e.id_clinica = c.id_clinica
        GROUP BY c.nombre
    """)
    empleados = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(empleados)

# 🔹 API: Obtener Medicamentos por Paciente
@app.route('/medicamentos_por_paciente', methods=['GET'])
def get_medicamentos_por_paciente():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.nombre AS paciente, COUNT(pm.id_medicamento) AS total_medicamentos 
        FROM pacientes_medicamentos pm
        JOIN pacientes p ON pm.id_paciente = p.id_paciente
        GROUP BY p.nombre
    """)
    medicamentos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(medicamentos)

# 🔹 API: Obtener Tratamientos con Prótesis Dentales
@app.route('/tratamientos_con_protesis', methods=['GET'])
def get_tratamientos_con_protesis():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.nombre AS tratamiento, COUNT(p.id_protesis) AS total_protesis
        FROM protesis_dentales p
        JOIN tratamientos t ON p.id_tratamiento = t.id_tratamiento
        GROUP BY t.nombre
    """)
    tratamientos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(tratamientos)

# 🔹 API: Obtener Proveedores por Clínica
@app.route('/proveedores_por_clinica', methods=['GET'])
def get_proveedores_por_clinica():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.nombre AS clinica, COUNT(p.id_proveedor) AS total_proveedores 
        FROM proveedores_dentales p
        JOIN clinicas c ON p.id_clinica = c.id_clinica
        GROUP BY c.nombre
    """)
    proveedores = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(proveedores)

# 🔹 API: Citas por Día y Semana
@app.route('/citas_por_tiempo', methods=['GET'])
def get_citas_por_tiempo():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT DATE(c.fecha_hora) AS fecha, COUNT(c.id_cita) AS total_citas 
        FROM citas c
        GROUP BY DATE(c.fecha_hora)
        ORDER BY fecha DESC
        LIMIT 7
    """)
    citas_tiempo = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(citas_tiempo)

# 🔹 Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
