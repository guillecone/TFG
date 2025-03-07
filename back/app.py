from flask import Flask, jsonify, request
from flask_cors import CORS  # Importar CORS
import mysql.connector

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

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


@app.route('/citas_por_doctores', methods=['GET'])
def get_citas_por_doctores():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Consulta para obtener citas agrupadas por doctor
    query = """
    SELECT d.nombre AS doctor, COUNT(c.id_cita) AS total_citas
    FROM citas c
    JOIN doctores d ON c.id_doctor = d.id_doctor
    GROUP BY d.id_doctor
    ORDER BY total_citas DESC;
    """
    cursor.execute(query)
    citas_por_doctor = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(citas_por_doctor)

@app.route('/material_por_clinica', methods=['GET'])
def get_material_por_clinica():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT c.nombre AS clinica, m.nombre AS material, m.cantidad
    FROM material_dental m
    JOIN clinicas c ON m.id_clinica = c.id_clinica
    ORDER BY c.nombre, m.nombre;
    """
    cursor.execute(query)
    material_por_clinica = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(material_por_clinica)

@app.route('/pacientes_por_tratamientos', methods=['GET'])
def get_pacientes_por_tratamientos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT t.nombre AS tratamiento, COUNT(pt.id_paciente) AS total_pacientes
    FROM pacientes_tratamientos pt
    JOIN tratamientos t ON pt.id_tratamiento = t.id_tratamiento
    GROUP BY t.id_tratamiento
    ORDER BY total_pacientes DESC;
    """
    cursor.execute(query)
    pacientes_por_tratamiento = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(pacientes_por_tratamiento)

@app.route('/medicamentos_por_tratamiento_paciente', methods=['GET'])
def get_medicamentos_por_tratamiento_paciente():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT t.nombre AS tratamiento, p.nombre AS paciente, m.nombre AS medicamento
    FROM pacientes_medicamentos pm
    JOIN pacientes p ON pm.id_paciente = p.id_paciente
    JOIN tratamientos_medicamentos tm ON pm.id_medicamento = tm.id_medicamento
    JOIN tratamientos t ON tm.id_tratamiento = t.id_tratamiento
    JOIN medicamentos m ON pm.id_medicamento = m.id_medicamento
    ORDER BY t.nombre, p.nombre, m.nombre;
    """
    cursor.execute(query)
    medicamentos_por_tratamiento_paciente = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(medicamentos_por_tratamiento_paciente)

@app.route('/proveedores_por_clinica', methods=['GET'])
def get_proveedores_por_clinica():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT c.nombre AS clinica, p.nombre AS proveedor, p.email, p.telefono, p.tipo_material
    FROM proveedores_dentales p
    JOIN clinicas c ON p.id_clinica = c.id_clinica
    ORDER BY c.nombre, p.nombre;
    """
    cursor.execute(query)
    proveedores_por_clinica = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(proveedores_por_clinica)


@app.route('/finanzas', methods=['GET'])
def get_finanzas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT MONTH(fecha) AS mes, SUM(ingresos) AS total_ingresos, SUM(gastos) AS total_gastos
    FROM facturacion
    GROUP BY mes
    ORDER BY mes;
    """
    cursor.execute(query)
    finanzas = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(finanzas)

@app.route('/tendencias_tratamientos', methods=['GET'])
def get_tendencias_tratamientos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT t.nombre AS tratamiento, COUNT(pt.id_paciente) AS total
    FROM pacientes_tratamientos pt
    JOIN tratamientos t ON pt.id_tratamiento = t.id_tratamiento
    GROUP BY t.id_tratamiento
    ORDER BY total DESC;
    """
    cursor.execute(query)
    tendencias = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(tendencias)

@app.route('/pacientes_nuevos_recurrentes', methods=['GET'])
def get_pacientes_nuevos_recurrentes():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT 
        COUNT(CASE WHEN fecha_registro >= DATE_SUB(NOW(), INTERVAL 1 YEAR) THEN 1 END) AS nuevos,
        COUNT(CASE WHEN fecha_registro < DATE_SUB(NOW(), INTERVAL 1 YEAR) THEN 1 END) AS recurrentes
    FROM pacientes;
    """
    cursor.execute(query)
    pacientes = cursor.fetchone()

    cursor.close()
    connection.close()
    
    return jsonify(pacientes)

@app.route('/tiempo_espera', methods=['GET'])
def get_tiempo_espera():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT c.nombre AS clinica, AVG(TIMESTAMPDIFF(MINUTE, c.fecha_reserva, c.fecha_atencion)) AS tiempo_espera
    FROM citas c
    JOIN clinicas cl ON c.id_clinica = cl.id_clinica
    WHERE c.fecha_atencion IS NOT NULL
    GROUP BY cl.id_clinica;
    """
    cursor.execute(query)
    tiempo_espera = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(tiempo_espera)

@app.route('/facturacion_clinicas', methods=['GET'])
def get_facturacion_clinicas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT c.nombre AS clinica, SUM(f.monto) AS total_facturacion
    FROM facturacion f
    JOIN clinicas c ON f.id_clinica = c.id_clinica
    GROUP BY c.id_clinica;
    """
    cursor.execute(query)
    facturacion = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(facturacion)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
