from flask import Flask, jsonify, request
from flask_cors import CORS 
from flask_mysqldb import MySQL

from config import config

app = Flask(__name__)
CORS(app)
con = MySQL(app)

def fila_a_diccionario(cursor,fila):
    columnas=[columna[0] for columna in cursor.description]
    return dict(zip(columnas,fila))

@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = "select * from alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno = {
                "matricula": fila[0],
                "nombre": fila[1],
                "apaterno": fila[2],
                "amaterno": fila[3],
                "correo": fila[4]
            }
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': "Lista de alumnos", 'exito': True})

    except Exception as ex:
        return jsonify({'mensaje': "error {}".format(ex), 'exito': False})

@app.route("/alumnos/<string:matricula>", methods=['GET'])
def leer_alumnos(matricula):
    cursor=None
    try:
        cursor=con.connection.cursor()
        cursor.execute("""SELECT * FROM alumnos WHERE matricula=%s""",(matricula,))
        fila=cursor.fetchone()
        if fila is None:
            
            return jsonfy({
               'mensaje':'Alumno no encontrado',
               'exito':False
            }), 404
        alumno=fila_a_diccionario(cursor,fila)
        return jsonify({
            'alumno':alumno,
            'exito':True
        }),200
    except Exception as ex:
        return jsonify({
            'mensaje':'Error al consultar alumno',
            'exito':False
        }),500
    finally:
        if cursor is not None:
            cursor.close()  

@app.route("/alumnos",methods=['POST'])
def regristrar_alumno():
    datos=request.get_json(silent=True)
    if not isinstance(datos,dict):
        return jsonify({
            'mensaje':'Se requiere objeto JSON',
            'exito':False
        }),400
    campos=[
        'matricula','nombre','apaterno','amaterno','correo'    
    ]
    if any(
        campo not in datos
        or not isinstance(datos[campo],str)
        or not datos[campo].strip()
        for campo in campos
    ):
        return jsonify({
            'mensaje':'Faltan campos obligatorios',
            'exito':False
        }),400
    cursor=None
    try:
        cursor=con.connection.cursor()
        cursor.execute(
            "SELECT matricula FROM alumnos WHERE matricula=%s",
            (datos['matricula'].strip(),)
        )
        if cursor.fetchone() is not None:
            return jsonify({
                'mensaje':'Lamtricula ya exite',
                'exito':False
            }),409
            
        cursor.execute(""" INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo)
        VALUES (%s, %s, %s, %s, %s)
         """, tuple(datos[campo].strip() for campo in campos))
 
        con.connection.commit()
 
        return jsonify({
            'mensaje':'Alumno Registrado Correctamente',
            'exito': True
        }),201
 
    except Exception as ex:
        con.connection.rollback()
        return jsonify({
            'mensaje':'Error al registrar alumno: {}'.format(ex),
            'exito': False
        }),500
    finally:
        if cursor is not None:
            cursor.close()

@app.route("/alumnos/<string:matricula>",methods=['PUT'])
def modificar_alumno(matricula):
    datos=request.get_json()
    if not datos:
        return jsonify({
            "mensaje":"No se recibieron datos para modificar"
        }), 400
    
    nombre=datos.get('nombre')
    apterno=datos.get('apaterno')
    amaterno=datos.get('amaterno')
    correo=datos.get('correo')
    
    if not nombre or not apaterno or not correo:
        return jsonify({
            "mensaje":"Nombre, apellido paterno y correo son obligatorios"
        }), 400
    cursor=None
    try:
        cursor=con.connection.corsor()
        cursor.execute(
            "SELECT matricula FROM alumnos WHERE matricula=%s",
            (matricula,)
        ) 
           
        alumno=cursor.fectchone()
        if not alumno:
            return jsonify({
                "mensaje":"No existe alumno con esa matricula"
            }),404
        sql = """UPDATE alumnos SET nombre=%s,
        apaterno=%s,
        amaterno=%s,
        correo=%s WHERE matricula=%s"""
        
        cursor.execute(sql, {
            apaterno,
            amaterno,
            correo,
            matricula
        })
        con,connection.commit()
        return jsonify({
            "mensaje": "Alumno modificado correctamente",
            "matricula":matricula
        }),200
        
    except Exception as e:
            

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>", 404

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)