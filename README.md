# 🛠️ FERREMAS - Sistema de Gestión para Ferretería

FERREMAS es una aplicación web para gestionar productos, usuarios y ventas en una ferretería. Desarrollada con **Flask**, usa tecnologías como **HTML**, **CSS**, **JavaScript** y **Python**, además de una base de datos **MySQL** levantada con XAMPP.

---

## 🚀 Tecnologías utilizadas

- HTML5 / CSS3 / JavaScript
- Python 3.x
- Flask
- MySQL (a través de XAMPP)
- Flask-MySQLdb
- Cryptography

---

## 🔧 Requisitos

- Python instalado
- [XAMPP](https://www.apachefriends.org/es/index.html)
- `virtualenv` instalado (`pip install virtualenv`)

---

## ⚙️ Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/Rodrigo0000000/ferremasWeb
   cd ferremasWeb
   ```

2. **Crea y activa un entorno virtual:**

   ```bash
   virtualenv venv
   # En Windows
   call venv\Scripts\activate.bat
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instala las dependencias necesarias:**

   ```bash
   pip install flask
   pip install flask_mysqldb
   pip install cryptography
   pip install mysqlclient
   ```

4. **Configura XAMPP:**

   - Abre el archivo `my.ini` dentro de la carpeta de instalación de XAMPP (`xampp/mysql/bin/my.ini`).
   - Cambia el puerto a `3307`:

     ```ini
     [mysqld]
     port=3307
     ```

   - Inicia el servidor MySQL desde el panel de XAMPP.

5. **Carga la base de datos desde MySQL:**

   - Abre una mySQL WorkBench 8.0
   - Crea y usa la base de datos:

     ```sql
     CREATE DATABASE ferremasdb;
     USE ferremasdb;
     ```

   - Copia y pega el contenido del archivo `.sql` ubicado en la carpeta `DB/` para crear las tablas e insertar los datos.

---

## ▶️ Ejecutar el proyecto

Dentro del entorno virtual, corre el servidor con:

```bash
python app.py
```

Luego visita en tu navegador:

```
http://127.0.0.1:5000/
```

---

## 📁 Estructura del proyecto

```
ferremas/
├── app.py
├── templates/
├── static/
├── DB/
│   └── CREATE_TABLE
│   └── INSERT_DATA
└── ...
```

