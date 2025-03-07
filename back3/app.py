from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# 🔹 Función para conectar con MySQL con Manejo de Errores
def get_db_connection():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='admin',
            password='Pa$$w0rd',
            database='conedental',
            pool_name="mypool",
            pool_size=5  # Pool de conexiones para mejorar rendimiento
        )
    except mysql.connector.Error as err:
        print(f"❌ Error de conexión a MySQL: {err}")
        return None

# 🔹 Función auxiliar para evitar duplicación de código en rutas
def fetch_from_db(query, params=None):
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Error de conexión con la base de datos"}), 500
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(result)

# 🔹 API: Obtener Todas las Tablas Principales
@app.route('/clinicas', methods=['GET'])
def get_clinicas():
    return fetch_from_db("SELECT * FROM clinicas")

@app.route('/pacientes', methods=['GET'])
def get_pacientes():
    return fetch_from_db("SELECT * FROM pacientes")

@app.route('/doctores', methods=['GET'])
def get_doctores():
    return fetch_from_db("SELECT * FROM doctores")

@app.route('/citas', methods=['GET'])
def get_citas():
    return fetch_from_db("SELECT * FROM citas")

@app.route('/empleados', methods=['GET'])
def get_empleados():
    return fetch_from_db("SELECT * FROM empleados")

@app.route('/material_dental', methods=['GET'])
def get_material_dental():
    return fetch_from_db("SELECT * FROM material_dental")

@app.route('/medicamentos', methods=['GET'])
def get_medicamentos():
    return fetch_from_db("SELECT * FROM medicamentos")

@app.route('/proveedores_dentales', methods=['GET'])
def get_proveedores():
    return fetch_from_db("SELECT * FROM proveedores_dentales")

@app.route('/tratamientos', methods=['GET'])
def get_tratamientos():
    return fetch_from_db("SELECT * FROM tratamientos")

@app.route('/pacientes_tratamientos', methods=['GET'])
def get_pacientes_tratamientos():
    return fetch_from_db("SELECT * FROM pacientes_tratamientos")

@app.route('/pacientes_medicamentos', methods=['GET'])
def get_pacientes_medicamentos():
    return fetch_from_db("SELECT * FROM pacientes_medicamentos")

@app.route('/tratamientos_medicamentos', methods=['GET'])
def get_tratamientos_medicamentos():
    return fetch_from_db("SELECT * FROM tratamientos_medicamentos")

# 🔹 API: Reportes y Estadísticas
@app.route('/citas_por_doctores', methods=['GET'])
def get_citas_por_doctores():
    query = """
        SELECT d.nombre AS doctor, COUNT(c.id_cita) AS total_citas 
        FROM citas c
        JOIN doctores d ON c.id_doctor = d.id_doctor
        GROUP BY d.nombre
    """
    return fetch_from_db(query)

@app.route('/pacientes_por_tratamientos', methods=['GET'])
def get_pacientes_por_tratamientos():
    query = """
        SELECT t.nombre AS tratamiento, COUNT(pt.id_paciente) AS total_pacientes 
        FROM pacientes_tratamientos pt
        JOIN tratamientos t ON pt.id_tratamiento = t.id_tratamiento
        GROUP BY t.nombre
    """
    return fetch_from_db(query)

@app.route('/citas_detalladas', methods=['GET'])
def get_citas_detalladas():
    query = """
        SELECT c.id_cita, c.fecha_hora, p.nombre AS paciente, d.nombre AS doctor, c.motivo 
        FROM citas c
        JOIN pacientes p ON c.id_paciente = p.id_paciente
        JOIN doctores d ON c.id_doctor = d.id_doctor
        ORDER BY c.fecha_hora DESC
    """
    return fetch_from_db(query)

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


@app.route('/empleados_por_clinica', methods=['GET'])
def get_empleados_por_clinica():
    query = """
        SELECT c.nombre AS clinica, COUNT(e.id_empleado) AS total_empleados 
        FROM empleados e
        JOIN clinicas c ON e.id_clinica = c.id_clinica
        GROUP BY c.nombre
    """
    return fetch_from_db(query)

@app.route('/medicamentos_por_paciente', methods=['GET'])
def get_medicamentos_por_paciente():
    query = """
        SELECT p.nombre AS paciente, COUNT(pm.id_medicamento) AS total_medicamentos 
        FROM pacientes_medicamentos pm
        JOIN pacientes p ON pm.id_paciente = p.id_paciente
        GROUP BY p.nombre
    """
    return fetch_from_db(query)

@app.route('/tratamientos_con_protesis', methods=['GET'])
def get_tratamientos_con_protesis():
    query = """
        SELECT t.nombre AS tratamiento, COUNT(p.id_protesis) AS total_protesis
        FROM protesis_dentales p
        JOIN tratamientos t ON p.id_tratamiento = t.id_tratamiento
        GROUP BY t.nombre
    """
    return fetch_from_db(query)

@app.route('/proveedores_por_clinica', methods=['GET'])
def get_proveedores_por_clinica():
    query = """
        SELECT c.nombre AS clinica, COUNT(p.id_proveedor) AS total_proveedores 
        FROM proveedores_dentales p
        JOIN clinicas c ON p.id_clinica = c.id_clinica
        GROUP BY c.nombre
    """
    return fetch_from_db(query)

@app.route('/citas_por_tiempo', methods=['GET'])
def get_citas_por_tiempo():
    query = """
        SELECT DATE(c.fecha_hora) AS fecha, COUNT(c.id_cita) AS total_citas 
        FROM citas c
        GROUP BY DATE(c.fecha_hora)
        ORDER BY fecha DESC
        LIMIT 7
    """
    return fetch_from_db(query)

# 🔹 Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
