from flask import(
    render_template, Blueprint, flash, g, redirect, request, url_for
)

from werkzeug.exceptions import abort

from eduven.models.inventory import Inventory
from eduven.models.user import User

from eduven.views.auth import login_required

from eduven import db

invent = Blueprint('inventory', __name__)

#Obtener un usuario
def get_user(id):
    user = User.query.get_or_404(id)
    return user 

#records
@invent.route("/inventory/records")
@login_required
def records():
    records = Inventory.query.all()
    db.session.commit()
    return render_template('inventory/records.html', records = records, get_user = get_user)

#Crear registro
@invent.route('/inventory/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        objectt = request.form.get('object')
        description = request.form.get('description')
        state = request.form.get('state')
        
        record = Inventory(g.user.id, objectt, description, state)
        
        if objectt == '' or description == '' or state == '':
            flash('Debe ingresas todos los datos')
            
        else:
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('inventory.records'))
        
    return render_template('inventory/create.html')

#Obtener registro
def get_record(id, check_author = True):
    record = Inventory.query.get(id)
    
    if record == None:
        abort(404, f'Id {id} de la publicacion no existe.')
        return redirect(url_for('inventory.records'))
    elif check_author and record.author != g.user.id:
        abort(404)
        return redirect(url_for('inventory.records'))
    else:
        return record

#Actualizar
@invent.route("/inventory/update/<int:id>", methods=('GET','POST'))
@login_required
def update(id):
    record = get_record(id)
    
    if request.method == 'POST':
        record.objectt = request.form.get('object')
        record.description = request.form.get('description')
        record.state = request.form.get('state')
        
        if record.objectt == '' or record.description == '' or record.state == '':
            flash('Debe ingresas todos los datos')
            
        else:
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('inventory.records'))
        
    return render_template('inventory/update.html', record=record)

#Eliminar
@invent.route('/inventory/delete/<int:id>')
@login_required
def delete(id):
    record = get_record(id)
    db.session.delete(record)
    db.session.commit()
    
    return redirect(url_for('inventory.records'))