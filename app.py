import pymysql
from flask import Flask, render_template, redirect, request, Response, session

app = Flask(__name__, template_folder="template")

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='login',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Ventana inicial por defecto
@app.route('/')
def home():
    return render_template('index.html')

# Ventana de admin
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Funcion de login
@app.route('/acceso-login', methods=["GET","POST"])
def login():
    if request.method == "POST" and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        try:
            with connection.cursor() as cur:
                cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
                account = cur.fetchone()

                if account:
                    session['logueado'] = True
                    session['id'] = account['id']
                    return render_template('admin.html')
                else:
                    return render_template('index.html', error="Correo o contraseña incorrectos")
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return render_template('index.html', error="Error de conexión con la base de datos")

if __name__ == "__main__":
    app.secret_key = "Santiago123"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)