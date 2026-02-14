from flask_sqlalchemy import SQLAlchemy
from extenstions import db
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from wtforms.validators import ValidationError
from sqlalchemy.dialects.sqlite import JSON

#User Table
class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=False)

#Hashing the Password for Security
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #Password Matching Checker
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    def __repr__(self):
        return f"User('{self.name}','{self.email}','{self.id}')"
    
    # Checks if Email Already Exists
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email  == email.data))
        if user is not None:
            raise ValidationError('This email is already registered. Please login')
    
    #Relationships
    pain_am = so.relationship("PainAM", backref="user", lazy="dynamic") 
    pain_pm = so.relationship("PainPM", backref="user", lazy="dynamic") 
    symptoms_am = so.relationship("SymptomsAM", backref="user", lazy="dynamic") 
    symptoms_pm = so.relationship("SymptomsPM", backref="user", lazy="dynamic") 
    activities = so.relationship("Activity", backref="user", lazy="dynamic") 
    initial_activity = so.relationship("InitialActivity", backref="user", uselist=False)

#Pain Table
class PainAM(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    neck: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    shoulders: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    upperback: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    lowerback: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    chest: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    hips: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    arms: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    elbows: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    legs: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    knees: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    overall: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    stress: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)

    #Place relationships of tables here

class PainPM(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    neck: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    shoulders: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    upperback: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    lowerback: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    chest: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    hips: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    arms: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    elbows: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    legs: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    knees: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    overall: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    stress: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)

    #Place relationships of tables here


class SymptomsAM(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    fatigue: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    stiffness: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    sleepquality: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    fibrofog: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    headache: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    ibs: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    dizziness: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    bodytemp: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    paraesthesia: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    allodynia: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    lightsens: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    depression: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    anxiety: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)

    #Place relationships of tables here

class SymptomsPM(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    fatigue: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    stiffness: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    fibrofog: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    headache: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    ibs: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    dizziness: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    bodytemp: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    paraesthesia: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    allodynia: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    lightsens: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    depression: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    anxiety: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)

    #Place relationships of tables here

class Activity(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    shower: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False) 
    cooking: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    laundry: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False) 
    vacuuming: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    cleaning: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    groceries: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False) 
    walking: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    driving: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    exercise: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False) 
    studying: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    resting: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False)
    socialising: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    outing: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    #Add more here

    #Place relationships of tables here

class InitialActivity(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    shower: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False) 
    cooking: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    laundry: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False) 
    vacuuming: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    cleaning: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    groceries: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False) 
    walking: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    driving: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    exercise: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False) 
    studying: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    socialising: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    outing: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    #Add more here

    #Place relationships of tables here

class ActivityPriority(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    shower: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True) 
    cooking: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    laundry: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True) 
    vacuuming: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    cleaning: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    groceries: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    studying: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)

class DailyRecommendation(db.Model): 
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    threshold: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    allowed: so.Mapped[list] = so.mapped_column(JSON, nullable=False) 
    avoid: so.Mapped[list] = so.mapped_column(JSON, nullable=False)
    user: so.Mapped["User"] = so.relationship("User", backref="daily_recommendations")






