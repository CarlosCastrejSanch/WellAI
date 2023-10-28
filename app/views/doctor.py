from app import app,db
from flask import render_template, request,jsonify
from flask_login import current_user, login_required
from ..models import User,EmployeeList,Answer, Question
from datetime import datetime, timedelta


@app.route("/doctor_employees", methods = ['GET','POST'])
@login_required
def doctor_employees():
    employeesList = EmployeeList.query.filter_by(is_doctor=False).all()
    doctor_employees = []
    doctor = EmployeeList.query.filter_by(email=current_user.email).first()
    for user in employeesList:
        employee = User.query.filter_by(email=user.email).first()
        if employee:
            if employee.doctor_access and user.corp_id == doctor.corp_id:
                doctor_employees.append(employee)
    return render_template("doctor_employees.html", user=current_user,doctor_employees=doctor_employees,chart_data=[],avg_data=[])



#  filter_by_employee
@app.route("/filter_by_employee", methods = ['GET','POST'])
def filter_by_employee():
    employee_id = request.form.get('employee_id')
    if current_user.is_employee:
        employee_id = current_user.id
    time = request.form.get('time')
    print('---------- time', time)
    answers = Answer.query.filter_by(user=employee_id).all()
    if time == "last-15mins":
        last_15_minutes = datetime.now() - timedelta(minutes=15)
        answers = Answer.query.filter(Answer.user == employee_id, Answer.timestamp >= last_15_minutes).all()
    elif time == "last-30mins":
        last_30_minutes = datetime.now() - timedelta(minutes=30)
        answers = Answer.query.filter(Answer.user == employee_id, Answer.timestamp >= last_30_minutes).all()
    elif time == "last-hour":
        last_hour = datetime.now() - timedelta(hours=1)
        answers = Answer.query.filter(Answer.user == employee_id, Answer.timestamp >= last_hour).all()
    elif time == "last-24hours":
        last_24_hour = datetime.now() - timedelta(hours=24)
        answers = Answer.query.filter(Answer.user == employee_id, Answer.timestamp >= last_24_hour).all()
    elif time == "last-2days":
        last_2_days = datetime.now() - timedelta(days=2)
        answers = Answer.query.filter(Answer.user == employee_id, Answer.timestamp >= last_2_days).all()
    elif time == "last-5days":
        last_5_days = datetime.now() - timedelta(days=5)
        answers = Answer.query.filter(Answer.user == employee_id, Answer.timestamp >= last_5_days).all()
    elif time == "last-week":
        last_week = datetime.now() - timedelta(weeks=1)
        answers = Answer.query.filter(Answer.user == employee_id, Answer.timestamp >= last_week).all()
    elif time == "last-month":
        last_month = datetime.now() - timedelta(days=30)
        answers = Answer.query.filter(Answer.user == employee_id, Answer.timestamp >= last_month).all()
        
    chart_data = []

    if answers is not None:
        chart_data = [
            {"date":answer.timestamp.strftime('%Y-%m-%D'),
             "value":answer.value,
             "score":answer.score,
             "category": Question.query.filter_by(id=answer.question_id).first().category
             }
             for answer in answers]

    return jsonify(chart_data)


@app.route("/avg_chart_doctor_employee", methods = ['GET','POST'])
def avg_chart_doctor_employee():
    employee_id = request.form.get('employee_id')
    if current_user.is_employee:
        employee_id = current_user.id
    answers = Answer.query.filter_by(user=employee_id).all()
    avg_data = {}
    if answers is not None:

        exhaustion_answers = Answer.query \
        .join(Question, Answer.question_id == Question.id) \
        .filter(Answer.user == employee_id, Question.category == "Agotamiento") \
        .all()

        mental_distance_answers = Answer.query \
            .join(Question, Answer.question_id == Question.id) \
            .filter(Answer.user == employee_id, Question.category == "Distancia mental") \
            .all()

        emotional_impairment_answers = Answer.query \
        .join(Question, Answer.question_id == Question.id) \
        .filter(Answer.user == employee_id, Question.category == "Deterioro emocional") \
        .all()

        cognitive_impairment_answers = Answer.query \
        .join(Question, Answer.question_id == Question.id) \
        .filter(Answer.user == employee_id, Question.category == "Deterioro cognitivo") \
        .all()


        total_score = round(sum([answer.score for answer in answers])/len(answers),2)
        exhaustion_answers_score = round(sum([answer.score for answer in exhaustion_answers])/len(exhaustion_answers),2)
        mental_distance_answers_score = round(sum([answer.score for answer in mental_distance_answers])/len(mental_distance_answers),2)
        emotional_impairment_answers_score = round(sum([answer.score for answer in emotional_impairment_answers])/len(emotional_impairment_answers),2)
        cognitive_impairment_answers_score = round(sum([answer.score for answer in cognitive_impairment_answers])/len(cognitive_impairment_answers),2)
        avg_data = {
            "puntuacion_total": {
                "bajo": total_score if total_score >= 1.00 and total_score <=1.50 else 0,
                "normal": total_score if total_score >= 1.51 and total_score <= 2.35 else 0,
                "alto": total_score if total_score >= 2.36 and total_score <= 3.17 else 0,
                "muy_alto":total_score if total_score >= 3.18  else 0
            },
            "agotamiento": {
                "bajo": exhaustion_answers_score if exhaustion_answers_score >= 1.00 and exhaustion_answers_score <= 1.66 else 0,
                "normal":exhaustion_answers_score if exhaustion_answers_score >= 1.67 and exhaustion_answers_score <= 2.99 else 0,
                "alto":exhaustion_answers_score if exhaustion_answers_score >= 3.00 and exhaustion_answers_score <= 3.99 else 0,
                "muy_alto":exhaustion_answers_score if exhaustion_answers_score >= 4.00 else 0
            },
            "distancia_mental": {
                "bajo": mental_distance_answers_score if mental_distance_answers_score == 1.00 else 0,
                "normal": mental_distance_answers_score if mental_distance_answers_score >= 1.01 and mental_distance_answers_score <= 2.65 else 0,
                "alto":mental_distance_answers_score if mental_distance_answers_score >= 2.66 and mental_distance_answers_score <= 3.99 else 0,
                "muy_alto": mental_distance_answers_score if mental_distance_answers_score >= 4.00 else 0
            },
            "deterioro_emocional": {
                "bajo": emotional_impairment_answers_score if emotional_impairment_answers_score == 1.00 else 0,
                "normal": emotional_impairment_answers_score if emotional_impairment_answers_score >= 1.01 and emotional_impairment_answers_score <= 2.00 else 0,
                "alto": emotional_impairment_answers_score if emotional_impairment_answers_score >= 2.01 and emotional_impairment_answers_score <= 3.00 else 0,
                "muy_alto": emotional_impairment_answers_score if emotional_impairment_answers_score >= 3.01 else 0
            },
            "deterioro_cognitivo": {
                "bajo": cognitive_impairment_answers_score if cognitive_impairment_answers_score >= 1.00 and cognitive_impairment_answers_score <= 1.66 else 0,
                "normal": cognitive_impairment_answers_score if cognitive_impairment_answers_score >= 1.67 and cognitive_impairment_answers_score <= 2.33 else 0,
                "alto": cognitive_impairment_answers_score if cognitive_impairment_answers_score >= 2.34 and cognitive_impairment_answers_score <= 3.32 else 0,
                "muy_alto": cognitive_impairment_answers_score if cognitive_impairment_answers_score >= 3.33 else 0
            }
        }
    print(avg_data)
    return jsonify(avg_data)