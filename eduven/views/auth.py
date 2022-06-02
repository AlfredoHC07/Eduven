from flask import(
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from eduven.models.user import User

from eduven import db

import functools

auth = Blueprint('auth', __name__, url_prefix='/auth')

#Registrar un usuario
@auth.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        fullname = request.form.get('full_name')
        username = request.form.get('new_username')
        password = request.form.get('new_password')
        conf_password = request.form.get('conf_password')
        
        SpecialSym =['#', '$', '%', '&', '*', '+', '.', '@'] 
        val = True
        val2 = True
        
        user_lower = username.lower()
        
        user = User(user_lower, generate_password_hash(password), fullname)
        
        user_name = User.query.filter_by(username = user_lower).first()
        
        if user_lower == '' or fullname == '' or password == '' or conf_password == '':
            flash('Debe ingresas todos los datos')

        elif user_name == None:             
            if len(password) < 6: 
                flash('La longitud de la contraseña debe ser de al menos 6 digitos.') 
                val = False
                
            if len(password) > 20: 
                flash('La longitud de la contraseña no debe ser superior a 8 digitos.') 
                val = False
                
            if not any(char.isdigit() for char in password): 
                flash('La contraseña debe tener al menos un número.') 
                val = False
                
            if not any(char.isupper() for char in password): 
                flash('La contraseña debe tener al menos una letra mayúscula.') 
                val = False
                
            if not any(char.islower() for char in password): 
                flash('La contraseña debe tener al menos una letra minúscula.') 
                val = False
                
            if not any(char in SpecialSym for char in password): 
                flash('La contraseña debe tener al menos uno de estos caracteres # $ % & * + . @') 
                val = False
            
            for i in user_lower:
                if i == ' ':
                    flash('El usuario no puede poseer espacios.')
            for i in password:
                if i == ' ':
                    flash('La contraseña no puede poseer espacios.')

            if val:            
                if password != conf_password:
                    flash('Las contraseñas no coinciden.')
                elif any(char.isdigit() for char in fullname): 
                    flash('El nombre no puede tener numeros.')
                else:
                    db.session.add(user)
                    db.session.commit()
                    flash('Usuario registrado correctamente.')
                    return redirect(url_for('auth.login'))
            else:
                flash('La contraseña no cumple con las especificaciones.')
                
        elif user_name:
            flash(f'El usuario {username} ya esta registrado.')
    
    return render_template('auth/register.html')

#Ingresar
@auth.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_lower = username.lower()
        
        user = User.query.filter_by(username = user_lower).first()
        
        if user_lower == '' or password == '':
            flash('Debe ingresas todos los datos')

        elif user_lower and password:
            if user == None:
                flash(f'El usuario {username} no existe en el sistema.')
            elif not check_password_hash(user.password, password):
                flash('Contraseña incorrecta.')
            else:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('inventory.index'))
    
    return render_template('auth/login.html')

#sesion
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)
        
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inventory.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
           return redirect(url_for('auth.login')) 
        return view(**kwargs)
    return wrapped_view
    