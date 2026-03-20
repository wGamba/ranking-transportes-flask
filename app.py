from flask import Flask, jsonify, render_template, request
import pymysql

app = Flask(__name__)

def conectar_bd():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        db='ranking_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transportes', methods=['GET'])
def obtener_transportes():
    try:
        conexion = conectar_bd()
        with conexion.cursor() as cursor:
            sql = """
                SELECT id, metodo, 
                CAST(velocidad_kmh AS DOUBLE) as velocidad_kmh, 
                CAST((velocidad_kmh / 5.0) AS DOUBLE) AS equivalencia_caminar 
                FROM ranking_transporte 
                ORDER BY equivalencia_caminar DESC
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()
        conexion.close()
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/transportes', methods=['POST'])
def agregar_transporte():
    try:
        datos = request.json
        conexion = conectar_bd()
        with conexion.cursor() as cursor:
            sql = "INSERT INTO ranking_transporte (metodo, velocidad_kmh) VALUES (%s, %s)"
            cursor.execute(sql, (datos.get('metodo'), datos.get('velocidad')))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "OK"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# NUEVA RUTA PARA ELIMINAR
@app.route('/api/transportes/<int:id>', methods=['DELETE'])
def eliminar_transporte(id):
    try:
        conexion = conectar_bd()
        with conexion.cursor() as cursor:
            sql = "DELETE FROM ranking_transporte WHERE id = %s"
            cursor.execute(sql, (id,))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
