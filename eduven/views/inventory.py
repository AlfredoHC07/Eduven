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

@invent.route("/")
@login_required
def index():
    records = Inventory.query.all()
    db.session.commit()
    return render_template('inventory/index.html', records = records)

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
            return redirect(url_for('inventory.index'))
        
    return render_template('inventory/create.html')