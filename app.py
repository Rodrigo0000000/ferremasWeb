from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
from cryptography.fernet import Fernet


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ferremasdb'

mysql = MySQL(app)

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

            # Verificar si el usuario ya existe
            cursor.execute("SELECT * FROM USERS WHERE NOMBRE = %s", (name,))
            user = cursor.fetchone()

            if user:
                encrypted_pass_db = user[2].encode()
                decrypted_pass = Fernet.decrypt(encrypted_pass_db).decode()

                if password.decode() == decrypted_pass:
                    cursor.close()
                    return render_template('index.html')
                else:
                    cursor.close()
                    return render_template('login.html')

            # Si no existe, lo crea
            encrypted_pass = Fernet.encrypt(password)
            cursor.execute("INSERT INTO USERS (NOMBRE, PASSWORD) VALUES (%s, %s)", (name, encrypted_pass.decode()))
            mysql.connection.commit()
            cursor.close()
            return render_template('index.html')
    except Exception as ex:
        print('ERROR AL INGRESAR USUARIO:', ex)
        return render_template('login.html')


@app.route('/ferreteria')
def ferreteria():
    return render_template('ferreteria.html')

@app.route('/construccion')
def construccion():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ITEMS")
    items = cursor.fetchall()
    cursor.close()
    return render_template('construccion.html', items=items)

@app.route('/electricidad')
def electricidad():
    return render_template('electricidad.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')


if __name__ == '__main__':
    app.run(debug=True)