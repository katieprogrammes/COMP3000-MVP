import os
from flask import render_template, Blueprint, url_for, current_app, redirect, flash, request
from flask_login import current_user, login_user, login_required
from models import User, PainAM, SymptomsAM, PainPM, SymptomsPM, Activity, InitialActivity, ActivityPriority, DailyRecommendation
from forms import RegistrationForm, LoginForm, PainForm, SymptomsForm, InitialActivityForm, ActivityForm, ActivityPriorityForm
from extenstions import db, login_manager
import sqlalchemy as sa

bp = Blueprint("routes", __name__)

@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))

#HOME
@bp.route ('/')
def home():
    return render_template('home.html', title='Home')

#REGISTRATION PAGE
@bp.route ('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Add User to Table
    if form.validate_on_submit():
        # Check if Email is Already in Use
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email is already in use. Please choose a different one.', 'error')

        # Check if Passwords Match
        elif form.password.data != form.password2.data:
            flash('Passwords do not match. Please try again.', 'error')

        else:
            # Add User to Table
            user = User(name=form.name.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('routes.reginit'))
        
    return render_template('register.html', title='Register', form=form)

@bp.route('/reginit', methods=['GET', 'POST'])
@login_required
def reginit():
    form = InitialActivityForm()

    if form.validate_on_submit():
        # Validation
        initact = InitialActivity(
            user_id=current_user.id,
            shower=int(form.shower.data),
            cooking=int(form.cooking.data),
            laundry=int(form.laundry.data),
            vacuuming=int(form.vacuuming.data),
            cleaning=int(form.cleaning.data),
            groceries=int(form.groceries.data),
            walking=int(form.walking.data),
            driving=int(form.driving.data),
            exercise=int(form.exercise.data),
            studying=int(form.studying.data),
            resting=int(form.resting.data),
            socialising=int(form.socialising.data),
            outing=int(form.outing.data),
        )

        # Saving Log to Database
        db.session.add(initact)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('routes.home'))

    return render_template('reginfo.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST']) 
def login(): 
    if current_user.is_authenticated: 
        return redirect(url_for('routes.home')) 
    form = LoginForm() 
    if form.validate_on_submit(): 
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data)) 
        if user is None or not user.check_password(form.password.data): 
            flash('Invalid username or password', 'error') 
            return redirect(url_for('routes.login')) 
        login_user(user, remember=form.remember_me.data) 
        flash('You are logged in!', 'success') 
        return redirect(url_for('routes.home')) 
    return render_template('login.html', title='Login', form=form)



@bp.route ('/logAM', methods=['GET', 'POST'])
#@login_required
def logAM():
    form1 = PainForm()
    form2 = SymptomsForm()
    form3 = ActivityPriorityForm()
    if request.method == "POST":
        #Validation
        pain_valid = form1.validate()
        symptoms_valid = form2.validate()
        if pain_valid and symptoms_valid:
        #Adding a New Pain Record
            pain_entry = PainAM(
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
            symptom_entry = SymptomsAM(
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
            # Saving Symptom Log to Database
            db.session.add(symptom_entry)

            activity_priority = ActivityPriority(
                user_id = current_user.id,
                date=form1.date.data,
                shower=int(form3.shower.data),
                cooking=int(form3.cooking.data),
                laundry=int(form3.laundry.data),
                vacuuming=int(form3.vacuuming.data),
                cleaning=int(form3.cleaning.data),
                groceries=int(form3.groceries.data),
                studying=int(form3.studying.data)
            )
            #Saving Activity Priority to Database
            db.session.add(activity_priority)
            
            #Saving Database Changes
            db.session.commit()

        flash('Record saved successfully', 'success')
        return redirect(url_for("routes.home"))
    return render_template('logAM.html', title='Morning Log', form1=form1, form2=form2, form3=form3)

@bp.route ('/logPM', methods=['GET', 'POST'])
@login_required
def logPM():
    form1 = PainForm()
    form2 = SymptomsForm()
    if request.method == "POST":
        #Validation
        pain_valid = form1.validate()
        symptoms_valid = form2.validate()
        if pain_valid and symptoms_valid:
        #Adding a New Pain Record
            pain_entry = PainPM(
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
            symptom_entry = SymptomsPM(
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
        return redirect(url_for("routes.home"))
    return render_template('logPM.html', title='Evening Log', form1=form1, form2=form2)

@bp.route ('/symptoms', methods=['GET', 'POST'])
@login_required
def symptoms():
    form = SymptomsForm()
    

    return render_template('symptoms.html', title='Symptoms', form=form)




#DAILY ACTIVITY ROUTE
@bp.route('/activity', methods=['GET', 'POST']) 
@login_required 
def activities():
    form = ActivityForm()
    if request.method == "POST":
        #Validation
        activity_valid = form.validate()
        if activity_valid:
        #Adding a New Activity Record
            activity_entry = Activity(
                user_id = current_user.id,
                date=form.date.data,
                shower=int(form.shower.data),
                cooking=int(form.cooking.data),
                laundry=int(form.laundry.data),
                vacuuming=int(form.vacuuming.data),
                cleaning=int(form.cleaning.data),
                groceries=int(form.groceries.data),
                walking=int(form.walking.data),
                driving=int(form.driving.data),
                exercise=int(form.exercise.data),
                studying=int(form.studying.data),
                resting=int(form.resting.data),
                socialising=int(form.socialising.data),
                outing=int(form.outing.data),
            )
            # Saving Pain Log to Database
            db.session.add(activity_entry)
            
            #Saving Database Changes
            db.session.commit()

            flash('Activity record saved successfully', 'success')
        return redirect(url_for("routes.home"))
    return render_template('activity.html', title='Activities', form=form)


#PLACEHOLDER ROUTE
@bp.route ('/placeholder')
def placeholder():
    return render_template('placeholder.html', title='Placeholder')