from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

# 1. LISTAR MAESTROS (GET)
@maestros_bp.route("/", methods=['GET'])
def lista_maestros():
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM maestros"
        cursor.execute(sql)
        datos = cursor.fetchall()
        maestros = []
        for fila in datos:
            maestro = {
                "idmaestro": fila[0],
                "nombre": fila[1],
                "apaterno": fila[2],
                "amaterno": fila[3],
                "correo": fila[4]
            }
            maestros.append(maestro)
        return jsonify({'maestros': maestros, 'mensaje': "Lista de maestros", 'exito': True})

    except Exception as ex:
        return jsonify({'mensaje': "error {}".format(ex), 'exito': False})

# 2. LEER UN MAESTRO POR ID (GET)
@maestros_bp.route("/<string:idmaestro>", methods=['GET'])
def leer_maestro(idmaestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM maestros WHERE idmaestro = %s", (idmaestro,))
        fila = cursor.fetchone()
        if fila is None:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404
        maestro = fila_a_diccionario(cursor, fila)
        return jsonify({
            'maestro': maestro,
            'exito': True
        }), 200
    except Exception as ex:
        return jsonify({
            'mensaje': 'Error al consultar maestro',
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()  

# 3. REGISTRAR MAESTRO (POST)
@maestros_bp.route("/", methods=['POST'])
def registrar_maestro():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({
            'mensaje': 'Se requiere objeto JSON',
            'exito': False
        }), 400
        
    campos = ['idmaestro', 'nombre', 'apaterno', 'amaterno', 'correo']
    if any(
        campo not in datos
        or not isinstance(datos[campo], str)
        or not datos[campo].strip()
        for campo in campos
    ):
        return jsonify({
            'mensaje': 'Faltan campos obligatorios',
            'exito': False
        }), 400
        
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT idmaestro FROM maestros WHERE idmaestro = %s",
            (datos['idmaestro'].strip(),)
        )
        if cursor.fetchone() is not None:
            return jsonify({
                'mensaje': 'El idmaestro ya existe',
                'exito': False
            }), 409
            
        cursor.execute("""
            INSERT INTO maestros (idmaestro, nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s, %s)
        """, tuple(datos[campo].strip() for campo in campos))
 
        mysql.connection.commit()
 
        return jsonify({
            'mensaje': 'Maestro Registrado Correctamente',
            'exito': True
        }), 201
 
    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': 'Error al registrar maestro: {}'.format(ex),
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()

# 4. MODIFICAR MAESTRO (PUT)
@maestros_bp.route("/<string:idmaestro>", methods=['PUT'])
def modificar_maestro(idmaestro):
    datos = request.get_json()
    if not datos:
        return jsonify({
            "mensaje": "No se recibieron datos para modificar"
        }), 400
    
    nombre = datos.get('nombre')
    apaterno = datos.get('apaterno')
    amaterno = datos.get('amaterno')
    correo = datos.get('correo')
    
    if not nombre or not apaterno or not correo:
        return jsonify({
            "mensaje": "Nombre, apellido paterno y correo son obligatorios"
        }), 400
        
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT idmaestro FROM maestros WHERE idmaestro = %s",
            (idmaestro,)
        )
        maestro = cursor.fetchone()
        if not maestro:
            return jsonify({
                "mensaje": "No existe un maestro con ese idmaestro"
            }), 404
            
        sql = """
            UPDATE maestros 
            SET nombre = %s, apaterno = %s, amaterno = %s, correo = %s 
            WHERE idmaestro = %s
        """
        
        cursor.execute(sql, (nombre, apaterno, amaterno, correo, idmaestro))
        mysql.connection.commit()
        
        return jsonify({
            "mensaje": "Maestro modificado correctamente",
            "idmaestro": idmaestro
        }), 200
        
    except Exception as e:
        if mysql.connection:
            mysql.connection.rollback()
        return jsonify({
            "mensaje": "Error al modificar maestro",
            "exito": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close() 

# 5. ELIMINAR MAESTRO (DELETE)
@maestros_bp.route("/<string:idmaestro>", methods=['DELETE'])
def eliminar_maestro(idmaestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute(
            "SELECT idmaestro FROM maestros WHERE idmaestro = %s",
            (idmaestro,)
        )
        maestro = cursor.fetchone()
        if not maestro:
            return jsonify({
                "mensaje": "No existe un maestro con ese idmaestro"
            }), 404
            
        cursor.execute(
            "DELETE FROM maestros WHERE idmaestro = %s",
            (idmaestro,)
        )    
        
        mysql.connection.commit()
        
        return jsonify({
            "mensaje": "Maestro eliminado correctamente",
            "idmaestro": idmaestro
        }), 200
        
    except Exception as e:
        if mysql.connection:
            mysql.connection.rollback()
        return jsonify({
            "mensaje": "Error al eliminar maestro",
            "exito": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()