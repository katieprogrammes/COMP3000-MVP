import os
from flask import render_template, Blueprint, url_for, current_app, redirect, flash
from models import User
from forms import RegistrationForm
from extenstions import db

bp = Blueprint("routes", __name__)




#HOME PAGE
@bp.route ('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Add User to Table
    if form.validate_on_submit():
        # Check if Email is Already in Use
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email is already in use. Please choose a different one.', 'custom-error')
     # Add User to Table
    if form.validate_on_submit():
        # Check if Email is Already in Use
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email is already in use. Please choose a different one.', 'custom-error')

        # Check if Passwords Match
        elif form.password.data != form.password2.data:
            flash('Passwords do not match. Please try again.', 'custom-error')

        else:
            # Add User to Table
            user = User(name=form.name.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
        
    return render_template('register.html', title='Register', form=form)


#PLACEHOLDER ROUTE
@bp.route ('/placeholder')
def placeholder():
    return render_template('placeholder.html', title='Placeholder')