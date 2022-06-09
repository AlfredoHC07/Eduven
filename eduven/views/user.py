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
    image = Image.query.filter_by(author=id).first()
    record = get_user(id)
    
    if request.method == 'POST':
        record.fullname = request.form.get('full_name')
        record.password = request.form.get('new_password')
        conf_password = request.form.get('conf_password')
        
        record.password = generate_password_hash(record.password)
        
        if record.fullname == '' or record.password == '':
            flash('Debe ingresas todos los datos')
            
        else:
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('inventory.records'))
        
    if image:    
        if os.path.exists(os.path.abspath(f'{app.config["UPLOAD_FOLDER"]}/{image.filename}')):
            record_image = {'image':f'img/uploat/{image.filename}'}   
        else:
            write_file(data=image.image, direc=app.config["UPLOAD_FOLDER"], filename=image.filename)
            record_image = {'image':f'img/uploat/{image.filename}'}
    else:
        record_image = None
               
    return render_template('user/profile.html', record=record, record_image=record_image)

@user.route("/user/image", methods=('GET','POST'))
@login_required
def image():
    if request.method == 'POST':
        image = request.files["image"]
        
        if not image:
            flash('Debe ingresar una imagen.')
            return redirect(f'/user/profile/{g.user.id}')
        else:     
            filename = secure_filename(image.filename)
            
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            bd = open_file(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            
            record_image = Image(g.user.id, bd, filename)        
            
            db.session.add(record_image)
            db.session.commit()
            
            return redirect(f'/user/profile/{g.user.id}')
    
    return redirect(url_for('inventory.records'))

@user.route("/user/image-update/<int:id>", methods=('GET','POST'))
@login_required
def imageUpdate(id):
    record = Image.query.filter_by(author=id).first()
    
    if request.method == 'POST':
        image = request.files["image_new"]
        
        if not image:
            flash('Debe ingresar una imagen.')
            return redirect(f'/user/profile/{g.user.id}')
        else:     
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], record.filename))
            record.image = open_file(os.path.join(app.config["UPLOAD_FOLDER"], record.filename))
                  
            db.session.add(record)
            db.session.commit()
            
            return redirect(f'/user/profile/{g.user.id}')
    
    return redirect(url_for('inventory.records'))
    
# Esta funcion lo que hace es tranformar la imagen que ingrese el usuario a binario
def open_file(filename):
    with open(filename, 'rb') as f:
        bd = f.read()
    return bd

# Esta la convierte de binario nuevamente a un archivo legible
def write_file(data, direc, filename):
    with open(f'{direc}/{filename}', 'wb') as f:
        f.write(data)