import os
from flask import render_template, Blueprint, url_for, current_app

bp = Blueprint("routes", __name__)



#HOME PAGE
@bp.route ('/')
def login():
    return render_template('login.html', title='Login')