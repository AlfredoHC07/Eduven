from flask import(
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)
from eduven.views.auth import login_required

from eduven.views.inventory import get_user

from eduven.models.user import User

from eduven.models.image import Image

from eduven import db, app

from werkzeug.utils import secure_filename

from werkzeug.security import check_password_hash, generate_password_hash

import os

user = Blueprint('user', __name__)

@user.route("/user/profile/<int:id>", methods=('GET','POST'))
@login_required
def profile(id):
    record = get_user(id)
    
    if request.method == 'POST':
        record.fullname = request.form.get('full_name')
        record.password = request.form.get('new_password')
        conf_password = request.form.get('conf_password')
        image = request.files["image"]
        
        record.password = generate_password_hash(record.password)
        
        if image:     
            filename = secure_filename(image.filename)
            
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            bd = open_file(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            
            record_image = Image(g.user.id, bd)
        
            if record.fullname == '' or record.password == '':
                flash('Debe ingresas todos los datos')
                
            else:
                db.session.add(record)
                db.session.commit()
                db.session.add(record_image)
                db.session.commit()
                
                return redirect(url_for('inventory.records'))
        else:
            if record.fullname == '' or record.password == '':
                flash('Debe ingresas todos los datos')
                
            else:
                db.session.add(record)
                db.session.commit()
                return redirect(url_for('inventory.records'))
        
    return render_template('user/profile.html', record=record)

# Esta funcion lo que hace es tranformar la imagen que ingrese el usuario a binario
def open_file(filename):
    with open(filename, 'rb') as f:
        bd = f.read()
    return bd

# Esta la convierte de binario nuevamente a un archivo legible
def write_file(data, direc, filename):
    with open(f'{direc}/{filename}', 'wb') as f:
        f.write(data)