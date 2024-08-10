import pymysql
from flask import Flask, render_template, redirect, request, session

app = Flask(__name__, template_folder="template")

# Configuración de la conexión a la base de datos
def get_db_connection():
    return pymysql.connect(
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
    if 'logueado' in session:
        return render_template('admin.html')
    else:
        return redirect('/')

# Función de login
@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        _correo = request.form.get('txtCorreo')
        _password = request.form.get('txtPassword')

        if _correo and _password:
            try:
                connection = get_db_connection()
                with connection.cursor() as cur:
                    cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
                    account = cur.fetchone()

                    if account:
                        session['logueado'] = True
                        session['id'] = account['id']
                        return redirect('/admin')
                    else:
                        error = "Correo o contraseña incorrectos."
            except Exception as e:
                print(f"Error al ejecutar la consulta: {e}")
                error = "Error de conexión con la base de datos."
            finally:
                connection.close()
        else:
            error = "Por favor, complete ambos campos."

    return render_template('index.html', error=error)

if __name__ == "__main__":
    app.secret_key = "Santiago123"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)