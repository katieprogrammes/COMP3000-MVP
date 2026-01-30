from flask_sqlalchemy import SQLAlchemy
from extenstions import db
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from wtforms.validators import ValidationError

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
    
#Pain Table
class PainAM(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    neck: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    shoulders: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    upperback: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    lowerback: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    chest: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    hips: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    arms: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    elbows: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    legs: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    knees: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    overall: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)

    #Place relationships of tables here

class PainPM(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    neck: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    shoulders: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    upperback: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    lowerback: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    chest: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    hips: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    arms: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    elbows: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    legs: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    knees: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    overall: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)

    #Place relationships of tables here


class SymptomsAM(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    fatigue: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    stiffness: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    sleepquality: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    fibrofog: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    headache: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    ibs: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    dizziness: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    bodytemp: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    paraesthesia: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    allodynia: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    lightsens: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    depression: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    anxiety: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)

    #Place relationships of tables here

class SymptomsPM(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    fatigue: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    stiffness: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    sleepquality: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    fibrofog: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    headache: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    ibs: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    dizziness: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    bodytemp: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    paraesthesia: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    allodynia: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    lightsens: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    depression: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    anxiety: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)

    #Place relationships of tables here

class Activity(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date, default=datetime.date.today)
    shower: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False) 
    cooking: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    laundry: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False) 
    vacuuming: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    cleaning: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    groceries: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False) 
    walking: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    driving: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    exercise: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True) 
    studying: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    resting: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    socialising: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    outing: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    #Add more here

    #Place relationships of tables here

class InitialActivity(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    shower: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False) 
    cooking: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    laundry: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False) 
    vacuuming: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    cleaning: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    groceries: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False) 
    walking: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    driving: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    exercise: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True) 
    studying: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    resting: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    socialising: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    outing: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    #Add more here

    #Place relationships of tables here






