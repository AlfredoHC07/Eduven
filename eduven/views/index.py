from flask import(
    render_template, Blueprint, flash, g, redirect, request, url_for
)

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('home/home.html')