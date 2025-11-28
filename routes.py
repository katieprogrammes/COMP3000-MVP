import os
from flask import render_template, Blueprint, url_for, current_app, redirect, flash, request
from flask_login import current_user, login_user, login_required
from models import User, Pain, Symptoms
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
    form1 = PainForm()
    form2 = SymptomsForm()
    if request.method == "POST":
        #Validation
        pain_valid = form1.validate()
        symptoms_valid = form2.validate()
        if pain_valid and symptoms_valid:
        #Adding a New Pain Record
            pain_entry = Pain(
                user_id = current_user.id,
                date=form1.date.data,
                neck=int(form1.neck.data),
                shoulders=int(form1.shoulders.data),
                upperback=int(form1.upperback.data),
                lowerback=int(form1.lowerback.data),
                chest=int(form1.chest.data),
                hips=int(form1.hips.data),
                arms=int(form1.arms.data),
                elbows=int(form1.elbows.data),
                legs=int(form1.legs.data),
                knees=int(form1.knees.data),
                overall=int(form1.overall.data),
            )

            # Saving Pain Log to Database
            db.session.add(pain_entry)

            #Adding a New Symptom Record
            symptom_entry = Symptoms(
                user_id = current_user.id,
                date=form1.date.data,
                fatigue=form2.fatigue.data,
                stiffness=form2.stiffness.data,
                sleepquality=form2.sleepquality.data,
                fibrofog=form2.fibrofog.data,
                ibs=form2.ibs.data,
                dizziness=form2.dizziness.data,
                bodytemp=form2.bodytemp.data,
                paraesthesia=form2.paraesthesia.data,
                allodynia=form2.allodynia.data,
                lightsens=form2.lightsens.data,
                depression=form2.depression.data,
                anxiety=form2.anxiety.data
            )
            # Saving Pain Log to Database
            db.session.add(symptom_entry)
            
            #Saving Database Changes
            db.session.commit()

        flash('Pain record saved successfully', 'success')
        return redirect(url_for("routes.placeholder"))
    return render_template('pain.html', title='Logging', form1=form1, form2=form2)

@bp.route ('/symptoms', methods=['GET', 'POST'])
@login_required
def symptoms():
    
    

    return render_template('symptoms.html', title='Symptoms', form=form)







#PLACEHOLDER ROUTE
@bp.route ('/placeholder')
def placeholder():
    return render_template('placeholder.html', title='Placeholder')