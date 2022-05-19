from flask import Flask, render_template, request, redirect, url_for, flash, session
# from db import Session, engine
from models.user import Usuario
import psycopg2
# from flask_login import LoginManager, login_user, logout_user, login_required

# from config import config

# session = Session()

app = Flask(__name__)
app.secret_key = 'super secret key'

db = psycopg2.connect(
    user = 'zjusxcfmfwujtd',
    password = 'bcaa13a0feeb9138b0d8c5a0d0c366bb59e2463b764b9ca246d339b839f288ea',
    host = "ec2-3-228-235-79.compute-1.amazonaws.com", 
    port = '5432',
    database = 'd102ukg1pnng0u')

# login_manager_app = LoginManager(app)

# @login_manager_app.user_loader
# def load_user(id):
#     return Usuario.get_by_id(id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        user_post     = request.form['username']
        password_post = request.form['password']
        
        user_post = user_post.lower()
        
        user_logged = Usuario.user_logg(db, user_post)
        
        if user_logged != None:
            if user_post == user_logged[0] and password_post == '':
                flash('Ingresa la contraseña.')
                return redirect(url_for('login'))
            elif user_post == user_logged[0] and password_post != user_logged[1]:
                flash('Contraseña Incorrecta.')
                return redirect(url_for('login'))
            elif user_post == user_logged[0] and password_post == user_logged[1]:
                return render_template('home/home.html')
            else:
                flash('Ocurrio un error.')
            return redirect(url_for('login'))  
        elif user_post == '' and password_post == '':
            flash('Por favor ingrese los datos.')
            return redirect(url_for('login'))
        elif user_post == '' and password_post != '':
            flash('Datos ingresados de manera incorrecta.')
            return redirect(url_for('login'))
        else:
            flash('Usuario Invalido.')
            return redirect(url_for('login'))             
    else:
        return render_template('auth/login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method =='POST':
        user           = request.form['new_username']
        password       = request.form['new_password']
        check_password = request.form['conf_password']
        full_name      = request.form['full_name']
        
        user = user.lower()
        
        user_checking = Usuario.user_logg(db, user)
        
        if user_checking:
            flash('El usuario ya existe en el Sistema.')
            return redirect(url_for('register'))
        elif user_checking == None:
            if user == '' or full_name == '' or password == '' or check_password == '':
                flash('Debe ingresas todos los datos')
                return redirect(url_for('register'))
            elif password != check_password:
                flash('Las contraseñas no coinciden.')
                return redirect(url_for('register'))
            else:
                user_res = (user_lower, password, full_name)
                try:
                    Usuario.user_res(db, user_res)
                    flash('Usuario registrado con éxito.')
                    return redirect(url_for('login'))
                except Exception as ex:
                    print(ex)
                    return redirect(url_for('login'))              
        else:
            flash('Ocurrio un error.')
            return redirect(url_for('register'))      
    else:
        return render_template('auth/register.html')
    
@app.route('/home')
def home():
    return render_template('home/home.html')
    
if __name__=='__main__':
    # app.config.from_object(config['development'])
    app.run(port=5555)