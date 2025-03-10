from flask import Flask, jsonify
from flask_cors import CORS  # 📌 Importamos CORS
import mysql.connector
import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Permite acceso desde cualquier origen

# Configuración de la base de datos
db_config = {
    "host": "localhost",
    "user": "conesa_admin",
    "password": "Pa$$w0rd",
    "database": "ConesaDental"
}

# Función para conectar a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 📊 NUEVOS PACIENTES (Ahora maneja bien las fechas)
@app.route('/api/nuevos_pacientes')
def nuevos_pacientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 🔹 Asegurar que la consulta obtiene las fechas correctas
    cursor.execute("SELECT MIN(fecha_registro) AS min_fecha, MAX(fecha_registro) AS max_fecha FROM pacientes")
    fechas = cursor.fetchone()
    
    if not fechas["min_fecha"]:
        return jsonify([])  # Si no hay datos en la base

    start_date = fechas["min_fecha"]
    end_date = fechas["max_fecha"]

    # 🔹 Nueva consulta asegurando que usa solo `DATE(fecha_registro)`
    cursor.execute("""
        SELECT DATE(fecha_registro) AS dia, COUNT(*) AS nuevos_pacientes
        FROM pacientes
        WHERE DATE(fecha_registro) BETWEEN %s AND %s
        GROUP BY dia
        ORDER BY dia;
    """, (start_date, end_date))
    
    data = cursor.fetchall()

    # 🔹 Rellenar los días sin datos con 0
    full_data = []
    data_dict = {item["dia"]: item["nuevos_pacientes"] for item in data}
    
    current_date = start_date
    while current_date <= end_date:
        full_data.append({
            "dia": current_date.strftime('%Y-%m-%d'),
            "nuevos_pacientes": data_dict.get(current_date.strftime('%Y-%m-%d'), 0)
        })
        current_date += datetime.timedelta(days=1)

    cursor.close()
    conn.close()
    return jsonify(full_data)


# 📊 Distribución de tratamientos realizados
@app.route('/api/tratamientos_realizados')
def tratamientos_realizados():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.nombre_tratamiento, COUNT(tr.id_tratamiento_realizado) AS cantidad_realizada
        FROM tratamientos_realizados tr
        JOIN tratamientos t ON tr.id_tratamiento = t.id_tratamiento
        GROUP BY t.nombre_tratamiento
        ORDER BY cantidad_realizada DESC;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# 📊 Número de consultas realizadas por dentista
@app.route('/api/consultas_por_dentista')
def consultas_por_dentista():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.nombre, d.apellido, COUNT(c.id_cita) AS consultas_realizadas
        FROM citas c
        JOIN doctores d ON c.id_doctor = d.id_doctor
        WHERE c.estado = 'Completada'
        GROUP BY d.id_doctor
        ORDER BY consultas_realizadas DESC;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# 📊 Nivel de stock de materiales
@app.route('/api/nivel_stock')
def nivel_stock():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT nombre_material, stock_actual, stock_minimo,
            CASE 
                WHEN stock_actual < stock_minimo THEN 'Bajo' 
                ELSE 'Suficiente' 
            END AS nivel_stock
        FROM materiales
        ORDER BY stock_actual ASC;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# 📊 Ingresos Generados por Tratamiento
@app.route('/api/ingresos_por_tratamiento')
def ingresos_por_tratamiento():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.nombre_tratamiento, SUM(t.costo) AS total_ingresos
        FROM tratamientos_realizados tr
        JOIN tratamientos t ON tr.id_tratamiento = t.id_tratamiento
        GROUP BY t.nombre_tratamiento
        ORDER BY total_ingresos DESC;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# 📊 Horas Pico de Consultas
@app.route('/api/horas_pico')
def horas_pico():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT HOUR(fecha_cita) AS hora, COUNT(*) AS cantidad_citas
        FROM citas
        GROUP BY hora
        ORDER BY hora;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# 📊 Proveedores con Más Materiales Suministrados
@app.route('/api/materiales_por_proveedor')
def materiales_por_proveedor():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.nombre_proveedor, COUNT(m.id_material) AS cantidad_materiales
        FROM materiales m
        JOIN proveedores p ON m.id_proveedor = p.id_proveedor
        GROUP BY p.nombre_proveedor
        ORDER BY cantidad_materiales DESC;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# Ruta principal
@app.route('/')
def home():
    return jsonify({"mensaje": "API de ConesaDental funcionando correctamente 🚀"})

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
