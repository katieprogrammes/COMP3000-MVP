import os
from flask import render_template, Blueprint, url_for, current_app, redirect, flash
from flask_login import current_user, login_user, login_required
from models import User, Pain
from forms import RegistrationForm, LoginForm, PainForm, SymptomsForm
from extenstions import db, login_manager
import sqlalchemy as sa

bp = Blueprint("routes", __name__)

@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


#REGISTRATION PAGE
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

@bp.route ('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.placeholder'))
    form = LoginForm()

    # Check if User Credentials are Entered Correctly
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        
    # Incorrect Entry
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('routes.login'))
        login_user(user, remember=form.remember_me.data)
        
        #Correct Entry
        flash('You are logged in!', 'success')
        return redirect(url_for('routes.placeholder'))

    return render_template('login.html', title='Login', form=form)

@bp.route ('/pain', methods=['GET', 'POST'])
@login_required
def pain():
    form = PainForm()
    if form.validate_on_submit():
        #Adding a New Pain Record
        pain_entry = Pain(
            user_id = current_user.id,
            date=form.date.data,
            neck=int(form.neck.data),
            shoulders=int(form.shoulders.data),
            upperback=int(form.upperback.data),
            lowerback=int(form.lowerback.data),
            chest=int(form.chest.data),
            hips=int(form.hips.data),
            arms=int(form.arms.data),
            elbows=int(form.elbows.data),
            legs=int(form.legs.data),
            knees=int(form.knees.data),
            overall=int(form.overall.data),
        )

        # Saving Log to Database
        db.session.add(pain_entry)
        db.session.commit()

        flash('Pain record saved successfully', 'success')
        return redirect(url_for("routes.placeholder"))
    return render_template('pain.html', title='Pain', form=form)

@bp.route ('/symptoms', methods=['GET', 'POST'])
@login_required
def symptoms():
    form = SymptomsForm()
    

    return render_template('symptoms.html', title='Symptoms', form=form)







#PLACEHOLDER ROUTE
@bp.route ('/placeholder')
def placeholder():
    return render_template('placeholder.html', title='Placeholder')