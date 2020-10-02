#Importar LIbrerías
import os
from flask import Flask, request, render_template,jsonify,redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

# Crear un objeto de tipo Flask
app = Flask(__name__)

# Datos para la conexión a mysql
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestioncontactos'

'''
Crear un objeto de tipo MyQL y se pasa como parametro el objeto
de tipo Flask con la configuración
'''
mysql = MySQL(app)
app.config['UPLOAD_FOLDER'] = './Fotos'

@app.route('/')
def Index():
    return render_template('FrmContactos.html')

@app.route('/agregarContacto', methods=['POST'])
def agregar():
    """[summary]
    Función que agrega un contacto a la base de datos
    Returns:
        [json]: [Retorna un objeto de tipo json con 3 datos]
    """
    if request.method == 'POST':
        identificacion = request.form['txtIdentificacion']
        nombres = request.form['txtNombres']
        apellidos = request.form['txtApellidos']
        correo = request.form['txtCorreo']
        fechaNacimiento = request.form['txtFechaNacimiento']
        #se crea una tupla con los datos del contacto a agregar
        contacto=(identificacion,nombres,apellidos,correo,fechaNacimiento)
        if(identificacion and nombres and apellidos and correo and fechaNacimiento):
            cursor = mysql.connection.cursor()
            consulta = "INSERT INTO contactos VALUES (null, %s,%s,%s,%s,%s)"
            resultado= cursor.execute(consulta, contacto)
            mysql.connection.commit()  
            cursor.close()          
            if (resultado):
                #subir la foto si se agregó el contacto a la base de datos
                # obtenemos el archivo del input "archivo"
                f = request.files['fileFoto']
                filename = secure_filename(f.filename)
                extension = filename.rsplit('.', 1)[1].lower()
                nuevoNombre = identificacion + "." + extension
                # Guardamos el archivo en el directorio "Archivos PDF"
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], nuevoNombre))
                return jsonify({"estado":True, "datos":None, "mensaje":"Contacto Agregado Correctamente"})
            else:
                return jsonify({"estado":False, "datos":None, "mensaje":"Problemas al agregar"}) 
        else:
            return jsonify({"estado":False, "mensaje":"Faltan Datos por Ingresar"})                  
        

@app.route("/consultarContacto", methods=['POST'])
def consultar():
    """[summary]
    Función que consult un contacto en la base de datos por su identificación
    Returns:
        [json]: [Retorna un objeto json con los datos del contacto consultado si existe
        de lo contrario retorna null]
    """
    if request.method == 'POST':
        identificacion = request.form['identificacion']
        if(identificacion):
            cursor = mysql.connection.cursor()
            consulta = 'SELECT * FROM contactos WHERE conIdentificacion = %s'
            #se crea una tupla con el parametro a enviar a la consulta
            contacto = (identificacion,)
            cursor.execute(consulta,contacto)        
            resultado = cursor.fetchone()            
            if(resultado):
                if (cursor.rowcount>0):
                    cursor.close()
                    return jsonify({"estado":True, "datos":resultado, "mensaje":"Datos del Contacto"})
                else:
                    return jsonify({"estado":False, "datos":resultado, "mensaje":"No existe aprendiz con esa identificación"})
            else:
                return jsonify({"estado":False, "datos":resultado, "mensaje":"No existe aprendiz"})
            

@app.route("/actualizarContacto", methods=['POST'])
def actualizar():
    """[summary]
    Función que actualiza un contacto en la base de datos
    Returns:
        [json]: [Objeto json con 3 atributos donde se informa si pudo o no pudo actualizar]
    """
    if request.method == 'POST':
        idContacto = request.form['idContacto']
        identificacion = request.form['txtIdentificacion']
        nombres = request.form['txtNombres']
        apellidos = request.form['txtApellidos']
        correo = request.form['txtCorreo']
        fechaNacimiento = request.form['txtFechaNacimiento']
        #se crea una tupla con los datos del contacto a actualizar
        #tengan en cuenta que la tupla se crea de acuerdo a como se van a ubicar en la consulta
        #por lo tanto el idContacto se coloca de último
        contacto=(identificacion,nombres,apellidos,correo,fechaNacimiento,idContacto)        
        if(idContacto and identificacion and nombres and apellidos and correo and fechaNacimiento):
            cursor = mysql.connection.cursor()
            consulta= ''' 
                    UPDATE contactos set conIdentificacion = %s, conNombres= %s,
                    conApellidos = %s, conCorreo = %s, conFechaNacimiento = %s WHERE idContacto = %s 
                    '''
            resultado= cursor.execute(consulta,contacto)
            mysql.connection.commit()  
            cursor.close()          
            if(resultado):
                return jsonify({"estado":True, "datos":resultado, "mensaje":"Contacto Actualizado"})
            else:
                return jsonify({"estado":False, "datos":resultado, "mensaje":"Problemas al Actualizar"})

@app.route("/listarContactos", methods=['POST'])
def listar():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM contactos')        
        resultado = cursor.fetchall()
        cursor.close()        
        if(resultado):
            return jsonify({"estado":True, "datos":resultado, "mensaje":"Listado de Contactos"})
        else:
            return jsonify({"estado":False, "datos":resultado, "mensaje":"Problemas al Consultar"})

@app.route("/eliminarContacto", methods=['POST'])
def eliminar():
    if request.method == 'POST':
        idContacto = request.form['idContacto']
        if(idContacto):
            #se crea la tupla con el dato a enviar a la consulta
            contacto = (idContacto,)
            cursor = mysql.connection.cursor()
            consulta = 'DELETE FROM contactos WHERE idContacto = %s'
            resultado= cursor.execute(consulta,contacto)      
            mysql.connection.commit()
            cursor.close()            
            if(resultado):
                return jsonify({"estado":True, "datos":resultado, "mensaje":"Contacto Eliminado"})
            else:
                return jsonify({"estado":False, "datos":resultado, "mensaje":"Problemas al Eliminar"})

@app.route("/subirArchivo", methods=['POST'])
def subirArchivo():
 if request.method == 'POST':
    # obtenemos el archivo del input "archivo"
    f = request.files['fileFoto']
    filename = secure_filename(f.filename)
    # Guardamos el archivo en el directorio "Archivos PDF"
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Retornamos una respuesta satisfactoria
    return "<h1>Archivo subido exitosamente</h1>"
	
@app.route("/subirArchivo2", methods=['POST'])
def subirArchivo2():
 if request.method == 'POST':
    # obtenemos el archivo del input "archivo"
    f = request.files['fileFoto']
    filename = secure_filename(f.filename)
    # Guardamos el archivo en el directorio "Archivos PDF"
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Retornamos una respuesta satisfactoria
    return "<h1>Archivo subido exitosamente</h1>"


if (__name__== "__main__"):
    app.run(port=3000,debug=True)