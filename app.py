from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL

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

@app.route('/login', methods = ['POST', 'GET'])

# Login
def login():
    try:
        if request.method == 'GET':
            return render_template('login.html')

        if request.method == 'POST':
            name = request.form['username']
            password = request.form['password']
            cursor = mysql.connection.cursor()

            # Verificar si el usuario ya existe
            cursor.execute("SELECT * FROM USERS WHERE NOMBRE = %s", (name,))
            existing_user = cursor.fetchone()

            if existing_user:
                # Si existe, solo redirige al index
                cursor.close()
                return render_template('index.html')

            # Si no existe, lo crea
            cursor.execute('''INSERT INTO USERS (NOMBRE, PASSWORD) VALUES (%s, %s)''', (name, password))
            mysql.connection.commit()
            cursor.close()
            return render_template('index.html')
    # Excepciones
    except Exception as ex:
        print('ERROR AL INGRESAR USUARIO', ex)
        return render_template('login.html')

@app.route('/ferreteria')
def ferreteria():
    return render_template('ferreteria.html')

@app.route('/construccion')
def construccion():
    return render_template('construccion.html')

@app.route('/electricidad')
def electricidad():
    return render_template('electricidad.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')


if __name__ == '__main__':
    app.run(debug=True)