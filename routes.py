import os
from flask import render_template, Blueprint, url_for, current_app, redirect, flash, request
from flask_login import current_user, login_user, login_required, logout_user
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
        return redirect(url_for('routes.account')) 
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

@bp.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'custom-success')
    return redirect(url_for('home'))

@bp.route("/history")
@login_required
def history():
    pain_am_logs = PainAM.query.filter_by(user_id=current_user.id).order_by(PainAM.date.desc()).all()
    pain_pm_logs = PainPM.query.filter_by(user_id=current_user.id).order_by(PainPM.date.desc()).all()
    symptoms_am_logs = SymptomsAM.query.filter_by(user_id=current_user.id).order_by(SymptomsAM.date.desc()).all()
    symptoms_pm_logs = SymptomsPM.query.filter_by(user_id=current_user.id).order_by(SymptomsPM.date.desc()).all()
    activity_logs = Activity.query.filter_by(user_id=current_user.id).order_by(Activity.date.desc()).all()

    #Combining Pain Logs
    combined_pain_logs = []
    for log in pain_am_logs:
        combined_pain_logs.append({
            "date": log.date,
            "time": "AM",
            "neck": log.neck,
            "shoulders": log.shoulders,
            "upperback": log.upperback,
            "lowerback": log.lowerback,
            "chest": log.chest,
            "hips": log.hips,
            "arms": log.arms,
            "elbows": log.elbows,
            "legs": log.legs,
            "knees": log.knees,
            "overall": log.overall
        })

    for log in pain_pm_logs:
        combined_pain_logs.append({
            "date": log.date,
            "time": "PM",
            "neck": log.neck,
            "shoulders": log.shoulders,
            "upperback": log.upperback,
            "lowerback": log.lowerback,
            "chest": log.chest,
            "hips": log.hips,
            "arms": log.arms,
            "elbows": log.elbows,
            "legs": log.legs,
            "knees": log.knees,
            "overall": log.overall
        })

    #Sorting the pain logs by date and time
    combined_pain_logs = sorted(combined_pain_logs, key=lambda x: (x["date"], x["time"]), reverse=True)

    #Combining Symptom Logs
    combined_symptom_logs = []
    for log in symptoms_am_logs:
        combined_symptom_logs.append({
            "date": log.date,
            "time": "AM",
            "fatigue": log.fatigue,
            "stiffness": log.stiffness,
            "sleepquality": log.sleepquality,
            "fibrofog": log.fibrofog,
            "headache": log.headache,
            "ibs": log.ibs,
            "dizziness": log.dizziness,
            "bodytemp": log.bodytemp,
            "paraesthesia": log.paraesthesia,
            "allodynia": log.allodynia,
            "lightsens": log.lightsens,
            "depression": log.depression,
            "anxiety": log.anxiety
        })
    for log in symptoms_pm_logs:
        combined_symptom_logs.append({
            "date": log.date,
            "time": "PM",
            "fatigue": log.fatigue,
            "stiffness": log.stiffness,
            "sleepquality": log.sleepquality,
            "fibrofog": log.fibrofog,
            "headache": log.headache,
            "ibs": log.ibs,
            "dizziness": log.dizziness,
            "bodytemp": log.bodytemp,
            "paraesthesia": log.paraesthesia,
            "allodynia": log.allodynia,
            "lightsens": log.lightsens,
            "depression": log.depression,
            "anxiety": log.anxiety
        })

    #Sorting the symtpom logs by date and time
    combined_symptom_logs = sorted(combined_symptom_logs, key=lambda x: (x["date"], x["time"]), reverse=True)

    #Activity History Logic
    activity_display_logs = []
    for log in activity_logs:
        activity_display_logs.append({
            "date": log.date,
            "shower": log.shower,
            "cooking": log.cooking,
            "laundry": log.laundry,
            "vacuuming": log.vacuuming,
            "cleaning": log.cleaning,
            "groceries": log.groceries,
            "walking": log.walking,
            "driving": log.driving,
            "exercise": log.exercise,
            "studying": log.studying,
            "resting": log.resting,
            "socialising": log.socialising,
            "outing": log.outing
        })


    return render_template(
        "history.html",combined_pain_logs=combined_pain_logs,combined_symptom_logs=combined_symptom_logs,activity_display_logs=activity_display_logs)


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
                headache=form2.headache.data,
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
                shower=bool(form3.shower.data),
                cooking=bool(form3.cooking.data),
                laundry=bool(form3.laundry.data),
                vacuuming=bool(form3.vacuuming.data),
                cleaning=bool(form3.cleaning.data),
                groceries=bool(form3.groceries.data),
                studying=bool(form3.studying.data)
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
                headache=form2.headache.data,
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
                shower=form.shower.data,
                cooking=form.cooking.data,
                laundry=form.laundry.data,
                vacuuming=form.vacuuming.data,
                cleaning=form.cleaning.data,
                groceries=form.groceries.data,
                walking=form.walking.data,
                driving=form.driving.data,
                exercise=form.exercise.data,
                studying=form.studying.data,
                resting=form.resting.data,
                socialising=form.socialising.data,
                outing=form.outing.data
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