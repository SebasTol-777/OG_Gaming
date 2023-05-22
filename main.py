from flask import Flask, request, render_template, redirect, flash
from Cone import * #Importando conexion BD
import controlador_juegos


app = Flask(__name__) 

@app.route('/') 
def Inicio(): 
    return render_template('public/pagina.html')

@app.route('/pagina1.html') 
def Registro_Contactanos(): 
    return render_template('public/pagina1.html')

@app.route('/Registro.html') 
def Registro_Clientes(): 
    return render_template('public/Registro.html')

@app.route('/aboutus.html') 
def aboutus(): 
    return render_template('public/aboutus.html')

@app.route('/login.html') 
def login(): 
    return render_template('public/login.html')

@app.route('/registroUsuario', methods=['GET', 'POST'])
def registroUsuario():
    msg =''
    if request.method == 'POST':
        Nombre              = request.form['Nombre']
        Apellido             = request.form['Apellido']
        Telefono              = request.form['Telefono']
        Email         = request.form['Email']
        Contrasena         = request.form['Contrasena']
        
        conexion_MySQLdb = connectionBD()
        cursor           = conexion_MySQLdb.cursor(dictionary=True)
        
        '''
        cursor.execute('INSERT INTO registro_usuario (Nombre, Apellido, Telefono , Email, Contrasena) VALUES (%s, %s, %s, %s, %s)', (Nombre, Apellido, Telefono , Email, Contrasena))
        ResultInsert = conexion_MySQLdb.commit()
        '''
            
        sql         = ("INSERT INTO registro_usuario (Nombre, Apellido, Telefono , Email, Contrasena) VALUES (%s, %s, %s, %s, %s)")
        valores     = (Nombre, Apellido, Telefono , Email, Contrasena)
        cursor.execute(sql, valores)
        conexion_MySQLdb.commit()
        
        cursor.close() #Cerrando conexion SQL
        conexion_MySQLdb.close() #cerrando conexion de la BD
        msg = 'Registro con exito'
        
        print(cursor.rowcount, "registro insertado")
        print("1 registro insertado", cursor.lastrowid)
  
        return render_template('public/Registro.html', msg='Formulario enviado')
    else:
        return render_template('public/Regisro.html', msg = 'Metodo HTTP incorrecto')


@app.route('/registrarForm', methods=['GET', 'POST'])
def registrarForm():
    msg =''
    if request.method == 'POST':
        Nombre              = request.form['Nombre']
        Email              = request.form['Email']
        Mensaje         = request.form['Mensaje']
        
        conexion_MySQLdb = connectionBD()
        cursor           = conexion_MySQLdb.cursor(dictionary=True)
        
        '''
        cursor.execute('INSERT INTO form_contacto (Nombre, Email, Mensaje) VALUES (%s, %s, %s)', (Nombre, Email, Mensaje))
        ResultInsert = conexion_MySQLdb.commit()
        '''
            
        sql         = ("INSERT INTO form_contacto (Nombre, Email, Mensaje) VALUES (%s, %s, %s)")
        valores     = (Nombre, Email, Mensaje)
        cursor.execute(sql, valores)
        conexion_MySQLdb.commit()
        
        cursor.close() #Cerrando conexion SQL
        conexion_MySQLdb.close() #cerrando conexion de la BD
        msg = 'Registro con exito'
        
        print(cursor.rowcount, "registro insertado")
        print("1 registro insertado, id", cursor.lastrowid)
  
        return render_template('public/pagina1.html', msg='Formulario enviado')
    else:
        return render_template('public/pagina1.html', msg = 'Metodo HTTP incorrecto')

#############
########
##### RUTAS AGREGAR JUEGOS
########
#############

@app.route("/agregar_juego")
def formulario_agregar_juego():
    return render_template("agregar_juego.html")


@app.route("/guardar_juego", methods=["POST"])
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/juegos")


@app.route("/juegos")
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)


@app.route("/eliminar_juego", methods=["POST"])
def eliminar_juego():
    controlador_juegos.eliminar_juego(request.form["id"])
    return redirect("/juegos")


@app.route("/formulario_editar_juego/<int:id>")
def editar_juego(id):
    # Obtener el juego por ID
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)


@app.route("/actualizar_juego", methods=["POST"])
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")

if __name__ == '__main__': 
    app.run(debug=True, port=5000) 

    