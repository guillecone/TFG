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

@app.route('/nuevos_pacientes', methods=['GET'])
def get_nuevos_pacientes():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT fecha_registro AS fecha, COUNT(id_paciente) AS total_pacientes
        FROM pacientes
        WHERE fecha_registro IS NOT NULL
        GROUP BY fecha_registro
        ORDER BY fecha_registro DESC
        LIMIT 10;
    """
    
    cursor.execute(query)
    pacientes = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(pacientes)


# 🔹 Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
