from flask import Flask
from flask import render_template, redirect, request, Response, session
from flask_mysqldb import MySQL, MySQLdb
from datetime import datetime


app = Flask(__name__,template_folder='template')

#crear base de datos
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='kx690'
app.config['MYSQL_PASSWORD']='admin'
app.config['MYSQL_DB']='login'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql=MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/acceso-login', methods=["GET","POST"])
def login():
    try:
        if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword':
            _correo = request.form['txtCorreo'] 
            _password = request.form['txtPassword']
            
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM usuario where correo = %s AND password = %s ',(_correo,_password,))
            account = cur.fetchone()
            
            if account:
                session['logueado'] =True
                session['idUsuario']=account['idUsuario']
                session['idRol']= account['idRol']
                
                if session['idRol']==1:
                    return render_template("admin2.html")
                elif session['idRol']==2:
                    return render_template('admin.html')

            else:
                
                return render_template('index.html', mensaje="Usuario incorrecto")

    except Exception as ex:
        return "Exploto todo"    
        
    
@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/crear-registro', methods=['GET','POST'])
def crear_registro():
    
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuario (correo, password, idRol) VALUES (%s, %s, '2')", (correo,password))
    mysql.connection.commit()
    
    return render_template('index.html', mensaje2="Usuario registrado exitosamente")

@app.route('/listar', methods=['GET','POST'])
def listar():
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario')
    usuarios = cur.fetchall()
    cur.close()
    
    return render_template('lista_usuario.html', usuarios=usuarios)

@app.route('/logs', methods=['GET','POST'])
def logs():
    log_data = request.get_json()
    if not log_data:
        return "Error: No se proporcionaron datos de log o no son JSON", 400

    print(f"Datos de log recibidos: {log_data}")
    log_data['received_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur = mysql.connection.cursor()
    cur.execute('''
        INSERT INTO logs (timestamp, nombre_servicio, nivel_log, mensaje, received_at)
        VALUES (%s, %s, %s, %s, %s)
    ''', (log_data['timestamp'], log_data['nombre_servicio'], log_data['nivel_log'], log_data['mensaje'], log_data['received_at']))
    mysql.connection.commit()
    cur.close()

    
    return "Funcionaaaa!!!!"

@app.route('/lista_logs')
def lista_logs():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM logs')
    logs = cur.fetchall()
    cur.close()
    
    return render_template('lista_logs.html', logs=logs)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000, threaded=True)
    
    