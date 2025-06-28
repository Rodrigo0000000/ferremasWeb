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
            print("🟡 Intentando login con:", name)
            cursor = mysql.connection.cursor()

            cursor.execute("SELECT * FROM USERS WHERE NOMBRE = %s", (name,))
            user = cursor.fetchone()

            if user:
                encrypted_pass_db = user[2].encode()
                try:
                    decrypted_pass = fernet.decrypt(encrypted_pass_db).decode()
                except Exception as e:
                    print("Error al desencriptar contraseña:", e)
                    print("Contraseña ingresada:", password.decode())
                    return render_template('login.html', error="Error con la contraseña del usuario.")

                if password.decode().strip() == decrypted_pass.strip():
                    session['user'] = name
                    print("Comparando:", repr(password.decode().strip()), "vs", repr(decrypted_pass.strip()))

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

from collections import Counter

from collections import Counter

@app.route('/comprar', methods=['POST'])
def comprar():
    try:
        print("===> INICIO /comprar")
        data = request.get_json()
        print("===> JSON recibido:", data)
        productos = data['productos']
        print("===> Productos en carrito (con duplicados):", productos)

        user_name = session.get('user')
        print("===> Usuario en sesión:", user_name)

        if not user_name:
            return jsonify({'success': False, 'error': 'Usuario no autenticado'})

        cursor = mysql.connection.cursor()

        # Obtener ID del usuario
        cursor.execute("SELECT ID_USER FROM USERS WHERE NOMBRE = %s", (user_name,))
        user = cursor.fetchone()
        print("===> Resultado SELECT ID_USER:", user)

        if not user:
            cursor.close()
            print("===> ERROR: Usuario no encontrado en la base de datos")
            return jsonify({'success': False, 'error': 'Usuario no encontrado'})

        id_user = user[0]
        print("===> ID del usuario:", id_user)

        fecha_actual = date.today()
        print("===> Fecha actual:", fecha_actual)

        # Contar ocurrencias de cada producto en la lista (si llegan duplicados)
        from collections import Counter
        conteo_productos = Counter(int(p['id']) for p in productos)
        print("===> Conteo de productos:", conteo_productos)

        # Iniciar transacción
        mysql.connection.begin()
        print("===> Transacción iniciada")

        total_solicitado = sum(conteo_productos.values())
        total_comprado = 0

        for id_item, cantidad_solicitada in conteo_productos.items():
            print(f"===> Procesando ID_ITEM {id_item} - Cantidad solicitada: {cantidad_solicitada}")
            cursor.execute("SELECT CANTIDAD FROM ITEMS WHERE ID_ITEM = %s FOR UPDATE", (id_item,))
            row = cursor.fetchone()

            if not row:
                print(f"===> ERROR: Producto {id_item} no existe")
                mysql.connection.rollback()
                cursor.close()
                return jsonify({'success': False, 'error': f'Producto con ID {id_item} no existe'})

            stock_disponible = row[0]
            print(f"===> Stock disponible para {id_item}: {stock_disponible}")

            cantidad_a_comprar = min(stock_disponible, cantidad_solicitada)
            print(f"===> Comprados {cantidad_a_comprar} de {cantidad_solicitada}")

            if cantidad_a_comprar > 0:
                cursor.execute(
                    "UPDATE ITEMS SET CANTIDAD = CANTIDAD - %s WHERE ID_ITEM = %s",
                    (cantidad_a_comprar, id_item)
                )
                cursor.execute(
                    "INSERT INTO VENTAS (ID_USER, ID_ITEM, CANTIDAD, FECHA) VALUES (%s, %s, %s, %s)",
                    (id_user, id_item, cantidad_a_comprar, fecha_actual)
                )

            total_comprado += cantidad_a_comprar

        mysql.connection.commit()
        print("===> Commit a la transacción")
        cursor.close()

        faltantes = total_solicitado - total_comprado
        print(f"===> Totales - Solicitado: {total_solicitado}, Comprado: {total_comprado}, Faltantes: {faltantes}")

        if faltantes > 0:
            return jsonify({
                'success': True,
                'mensaje': (
                    f"No se compraron todos los items seleccionados "
                    f"[Comprados: {total_comprado} / Solicitados: {total_solicitado} / Faltantes por stock: {faltantes}]"
                )
            })
        else:
            return jsonify({
                'success': True,
                'mensaje': "Compra exitosa"
            })

    except Exception as e:
        mysql.connection.rollback()
        import traceback
        print("ERROR EN COMPRA:", e)
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Error al procesar la compra: {str(e)}'})



if __name__ == '__main__':
    app.run(debug=True)