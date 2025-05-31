from flask import Flask, render_template, url_for, request, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from cryptography.fernet import Fernet
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ferremasdb'

mysql = MySQL(app)

if not os.path.exists("secret.key"):
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

with open("secret.key", "rb") as key_file:
    key = key_file.read()

app.secret_key = key

fernet = Fernet(key)
@app.route('/')
def index():
    return render_template('index.html')

def form():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template('login.html')

        if request.method == 'POST':
            name = request.form['username']
            password = request.form['password'].encode()
            cursor = mysql.connection.cursor()

            cursor.execute("SELECT * FROM USERS WHERE NOMBRE = %s", (name,))
            user = cursor.fetchone()

            if user:
                encrypted_pass_db = user[2].encode()
                decrypted_pass = fernet.decrypt(encrypted_pass_db).decode()

                if password.decode() == decrypted_pass:
                    session['user'] = name
                    cursor.close()
                    return render_template('index.html')
                else:
                    cursor.close()
                    return render_template('login.html', error="Credenciales incorrectas")

            encrypted_pass = fernet.encrypt(password)
            cursor.execute("INSERT INTO USERS (NOMBRE, PASSWORD) VALUES (%s, %s)", (name, encrypted_pass.decode()))
            mysql.connection.commit()
            session['user'] = name
            cursor.close()
            return render_template('index.html')

    except Exception as ex:
        print('ERROR AL INGRESAR USUARIO:', ex)
        return render_template('login.html', error=f"Error: {str(ex)}")

@app.route('/ferreteria')
def ferreteria():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM ITEMS")
    items = cursor.fetchall()
    cursor.close()
    return render_template('ferreteria.html', items=items)

@app.route('/construccion')
def construccion():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM ITEMS WHERE CATEGORIA = 'Construcción'")
    items = cursor.fetchall()
    cursor.close()
    return render_template('construccion.html', items=items)

@app.route('/electricidad')
def electricidad():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM ITEMS WHERE CATEGORIA = 'Electricidad'")
    items = cursor.fetchall()
    cursor.close()
    return render_template('electricidad.html', items=items)

@app.route('/servicios')
def servicios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM ITEMS WHERE CATEGORIA = 'Servicios'")
    items = cursor.fetchall()
    cursor.close()
    return render_template('servicios.html', items=items)

@app.route('/comprar', methods=['POST'])
def comprar():
    try:
        data = request.get_json()
        productos = data['productos']
        user_name = session.get('user')

        if not user_name:
            return jsonify({'success': False, 'error': 'Usuario no autenticado'})

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT ID_USER FROM USERS WHERE NOMBRE = %s", (user_name,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'})

        id_user = user[0]
        fecha_actual = date.today()

        for p in productos:
            id_item = p['id']
            cantidad = p.get('cantidad', 1)

            # Insertar venta
            cursor.execute("""
                INSERT INTO VENTAS (ID_USER, ID_ITEM, CANTIDAD, FECHA)
                VALUES (%s, %s, %s, %s)
            """, (id_user, id_item, cantidad, fecha_actual))

            # Restar stock
            cursor.execute("""
                UPDATE ITEMS SET CANTIDAD = CANTIDAD - %s WHERE ID_ITEM = %s AND CANTIDAD >= %s
            """, (cantidad, id_item, cantidad))

        mysql.connection.commit()
        cursor.close()
        return jsonify({'success': True})
    except Exception as e:
        print("ERROR EN COMPRA:", e)
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)