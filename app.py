# #! Importamos los modulos que serán necesarios para realizar lo login
#! pymysql = Coneccion a la base de datos MySQL desde python
#! Flask = framework web que permite contruir la aplicación
#! render_template = Permite renderizar plantillas HTML (archivos .html) y devolverlas como respuesta al cliente.
#! redirect = Redirige a otra URL dentro de la aplicación.
#! request = Permite acceder a los datos enviados por el cliente (por ejemplo, a través de formularios).
#! session = Se utiliza para manejar sesiones, almacenando datos entre peticiones (como la información de inicio de sesión del usuario).
import pymysql
from flask import Flask, render_template, redirect, request, session

#* Configuracion de la aplicacion Flask
#* Crea una instancia de la aplicación Flask. Aquí se le indica a Flask que busque las plantillas HTML en la carpeta "template".
app = Flask(__name__, template_folder="template")

# Configuración de la conexión a la base de datos
#? Esta función establece una conexión a la base de datos MySQL utilizando pymysql.connect
def get_db_connection():
    return pymysql.connect(
        #? La dirección del servidor de base de datos (en este caso, localhost, que significa que está en la misma máquina donde corre la aplicación).
        host='localhost',
        #? Credenciales de acceso a la base de datos
        user='root',
        password='',
        #? Nombre de la base de datos
        db='login',
        #? Conjuntos de caracteres a utilizar
        charset='utf8mb4',
        #? Permite que los resultados de las consultas se devuelvan como diccionarios en lugar de tuplas.
        cursorclass=pymysql.cursors.DictCursor
    )

# Ventana inicial por defecto
@app.route('/')
def home():
    return render_template('index.html')

# Ventana de admin
# Esta ruta es accesible solo para usuarios logueados correctamente
# Si no fue logueado lo devuelve a la ventana de inicio
@app.route('/admin')
def admin():
    if 'logueado' in session:
        return render_template('admin.html')
    else:
        return redirect('/')

# Función de login
# TODOS: Define una ruta para la URL /acceso-login. (En el html)Esta ruta maneja tanto las solicitudes GET (cuando se carga la página) 
# TODOS: como POST (cuando se envían datos desde un formulario).
@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    error = None
    # TODOS: Verifica si la solicitud es POST (es decir, si se enviaron datos desde un formulario).
    if request.method == "POST":
        # TODOS: Estas variables almacenas las respuestas enviadas por los usuarios en los text input
        # TODOS: En los apartados "txtCorreo" y "txtPassword" (En el html)
        _correo = request.form.get('txtCorreo')
        _password = request.form.get('txtPassword')

        # TODOS: Verifica que ambos campos estén completos, que el usuario los haya diligenciado y no estén vacios.
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
        # TODOS: Si el usuario dejo alguno de los dos campos sin diligenciar le alerta que debe completarlos
        else:
            error = "Por favor, complete ambos campos."

    return render_template('index.html', error=error)

if __name__ == "__main__":
    app.secret_key = "Santiago123"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)