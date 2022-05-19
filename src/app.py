from flask import Flask, render_template, request, redirect, url_for, flash
from db import Session, engine
from models.user import Usuario 
# from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

session = Session()

app = Flask(__name__)

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
        
        user_logged = Usuario.user_logg(user_post)
        
        if user_logged != None:
            if user_post == user_logged[0] and password_post == '':
                flash('Ingresa la contraseña.')
                return redirect(url_for('login'))
            elif user_post == user_logged[0] and password_post != user_logged[1]:
                flash('Contraseña Incorrecta.')
                return redirect(url_for('login'))
            elif user_post == user_logged[0] and password_post == user_logged[1]:
                # login_user(user_logged)
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
        
        user_checking = Usuario.user_logg(user)
        
        if user_checking:
            flash('El usuario ya existe en el Sistema.')
            return redirect(url_for('register'))
        elif user_checking == None:
            if password != check_password:
                flash('Las contraseñas no coinciden.')
                return redirect(url_for('register'))
            else:
                with engine.connect() as con:
                    new_user = Usuario(
                        user_name=user, 
                        password=password, 
                        full_name=full_name
                    )
                    session.add(new_user)
                    session.commit()
                    
                    flash('Usuario registrado con éxito.')
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
    app.config.from_object(config['development'])
    app.run(port=3333)