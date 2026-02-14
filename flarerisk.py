from datetime import date, timedelta
from models import PainAM, PainPM, SymptomsAM, SymptomsPM

def calculate_flare_risk(stress, sleep, pain_values, symptom_values):
    #Stress
    if stress >=8:
        stress_score = 3
    elif stress >=4:
        stress_score = 2
    elif stress >=1:
        stress_score = 1
    else:
        stress_score = 0

    #Sleep Quality
    if sleep >=8:
        sleep_score = 3
    elif sleep >=4:
        sleep_score = 2
    elif sleep >=1:
        sleep_score = 1
    else:
        sleep_score = 0

    #Pain Score
    high_pain_count = sum(
        1 for p in pain_values
        if p >=8
    )
    if high_pain_count >=10:
        pain_score = 4
    elif high_pain_count >=7:
        pain_score = 3
    elif high_pain_count >=4:
        pain_score = 2
    elif high_pain_count >=1:
        pain_score = 1
    else:
        pain_score = 0

    #Symptom Score
    severe_symptom_count = sum(
        1 for s in symptom_values
        if s >=8
    )
    if severe_symptom_count >=10:
        symptom_score = 4
    elif severe_symptom_count >=7:
        symptom_score = 3
    elif severe_symptom_count >=4:
        symptom_score = 2
    elif severe_symptom_count >=1:
        symptom_score = 1
    else:
        symptom_score = 0

    #Total Risk Score
    risk_score = stress_score + sleep_score + pain_score + symptom_score

    #Risk Level
    if risk_score >= 9:
        risk_level = "High"
    elif risk_score >= 5:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    return risk_score, risk_level

def get_flarerisk_for_user(user_id):
    today = date.today()
    days = [ today, today - timedelta(days=1), today - timedelta(days=2) ]
    pain_values = [] 
    symptom_values = [] 
    stress_values = [] 
    sleep_values = []

    for day in days: 
        pain_am = PainAM.query.filter_by(user_id=user_id, date=day).first() 
        pain_pm = PainPM.query.filter_by(user_id=user_id, date=day).first() 
        symptoms_am = SymptomsAM.query.filter_by(user_id=user_id, date=day).first() 
        symptoms_pm = SymptomsPM.query.filter_by(user_id=user_id, date=day).first()

        if symptoms_am:
            if symptoms_am.sleepquality is not None: 
                sleep_values.append(symptoms_am.sleepquality)

        if pain_am: 
            if pain_am.stress is not None: 
                stress_values.append(pain_am.stress) 
        if pain_pm: 
            if pain_pm.stress is not None: 
                stress_values.append(pain_pm.stress) 

        if pain_am: pain_values.extend([ 
            pain_am.neck, pain_am.shoulders, pain_am.upperback, 
            pain_am.lowerback, pain_am.chest, pain_am.hips, pain_am.arms, 
            pain_am.elbows, pain_am.legs, pain_am.knees, pain_am.overall 
            ]) 
        if pain_pm: pain_values.extend([ 
            pain_pm.neck, pain_pm.shoulders, pain_pm.upperback, 
            pain_pm.lowerback, pain_pm.chest, pain_pm.hips, pain_pm.arms, 
            pain_pm.elbows, pain_pm.legs, pain_pm.knees, pain_pm.overall 
            ])

        if symptoms_am: symptom_values.extend([ 
            symptoms_am.fatigue, symptoms_am.fibrofog
            ]) 
        if symptoms_pm: symptom_values.extend([ 
            symptoms_pm.fatigue, symptoms_pm.fibrofog 
            ])
    avg_stress = sum(stress_values) / len(stress_values) if stress_values else 0 
    avg_sleep = sum(sleep_values) / len(sleep_values) if sleep_values else 10
    return calculate_flare_risk( stress=avg_stress, sleep=avg_sleep, pain_values=pain_values, symptom_values=symptom_values )

