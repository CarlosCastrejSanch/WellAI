from app import app,db ,GPTJ
from flask import render_template,flash, request, jsonify
from flask_login import current_user, login_required
from ..models import User, EmployeeList,Answer,Question
from time import sleep
from ..config import basedir


@app.route("/employee", methods = ['GET','POST'])
@login_required
def employee():
    return render_template("employee.html", user=current_user)


@app.route("/employee_profile", methods = ['GET','POST'])
@login_required
def employee_profile():
    return render_template("employee_profile.html", user=current_user)




@app.route("/updateEmployee", methods = ['GET','POST'])
def updateEmployee():
    email = request.args.get('email')
    name = request.args.get('name')
    checkbox = request.args.get('checkbox')
    is_doctor = request.args.get('is_doctor')
    user = current_user
    user.email = email
    user.username = name
    if is_doctor == "Doctor":
        user.is_doctor = True
    else:
        user.is_doctor = False
    
    if checkbox == "true":
        userEmployee= EmployeeList.query.filter_by(email=email).first()
        doctorsList = EmployeeList.query.filter_by(is_doctor=True).all()
        for u in doctorsList:
            doctor = User.query.filter_by(email=u.email).first()
            userDoctor= EmployeeList.query.filter_by(email=doctor.email).first()

            if userEmployee.corp_id == userDoctor.corp_id:
                user.doctor_access = True

    else:
        userEmployee= EmployeeList.query.filter_by(email=email).first()
        doctorsList = EmployeeList.query.filter_by(is_doctor=True).all()
        for u in doctorsList:
            doctor = User.query.filter_by(email=u.email).first()
            userDoctor= EmployeeList.query.filter_by(email=doctor.email).first()
            if userEmployee.corp_id == userDoctor.corp_id:
                user.doctor_access = False
        
    db.session.commit()
    flash("¡Los datos han sido actualizados correctamente!", category="success")
    return render_template("user_updated_message.html", user=user)


@app.route("/my_results", methods = ['GET','POST'])
@login_required
def my_results():
    answers = Answer.query.filter_by(user=current_user.id).all()
    exhaustion_answers = Answer.query \
        .join(Question, Answer.question_id == Question.id) \
        .filter(Answer.user == current_user.id, Question.category == "Agotamiento") \
        .all()

    mental_distance_answers = Answer.query \
        .join(Question, Answer.question_id == Question.id) \
        .filter(Answer.user == current_user.id, Question.category == "Distancia mental") \
        .all()

    emotional_impairment_answers = Answer.query \
    .join(Question, Answer.question_id == Question.id) \
    .filter(Answer.user == current_user.id, Question.category == "Deterioro emocional") \
    .all()

    cognitive_impairment_answers = Answer.query \
    .join(Question, Answer.question_id == Question.id) \
    .filter(Answer.user == current_user.id, Question.category == "Deterioro cognitivo") \
    .all()

    def calculate_average_score(answers):
            if len(answers) != 0:
                return round(sum([answer.score for answer in answers])/len(answers), 2)
            else:
                return 0

    total_score = calculate_average_score(answers)
    exhaustion_answers_score = calculate_average_score(exhaustion_answers)
    mental_distance_answers_score = calculate_average_score(mental_distance_answers)
    emotional_impairment_answers_score = calculate_average_score(emotional_impairment_answers)
    cognitive_impairment_answers_score = calculate_average_score(cognitive_impairment_answers)

    info_dict = {
        "puntuacion_total": {
            "bajo": total_score if total_score >= 1.00 and total_score <=1.50 else "-",
            "normal": total_score if total_score >= 1.51 and total_score <= 2.35 else "-",
            "alto": total_score if total_score >= 2.36 and total_score <= 3.17 else "-",
            "muy_alto":total_score if total_score >= 3.18  else "-"
        },
        "agotamiento": {
            "bajo": exhaustion_answers_score if exhaustion_answers_score >= 1.00 and exhaustion_answers_score <= 1.66 else "-",
            "normal":exhaustion_answers_score if exhaustion_answers_score >= 1.67 and exhaustion_answers_score <= 2.99 else "-",
            "alto":exhaustion_answers_score if exhaustion_answers_score >= 3.00 and exhaustion_answers_score <= 3.99 else "-",
            "muy_alto":exhaustion_answers_score if exhaustion_answers_score >= 4.00 else "-"
        },
        "distancia_mental": {
            "bajo": mental_distance_answers_score if mental_distance_answers_score == 1.00 else "-",
            "normal": mental_distance_answers_score if mental_distance_answers_score >= 1.01 and mental_distance_answers_score <= 2.65 else "-",
            "alto":mental_distance_answers_score if mental_distance_answers_score >= 2.66 and mental_distance_answers_score <= 3.99 else "-",
            "muy_alto": mental_distance_answers_score if mental_distance_answers_score >= 4.00 else "-"
        },
        "deterioro_emocional": {
            "bajo": emotional_impairment_answers_score if emotional_impairment_answers_score == 1.00 else "-",
            "normal": emotional_impairment_answers_score if emotional_impairment_answers_score >= 1.01 and emotional_impairment_answers_score <= 2.00 else "-",
            "alto": emotional_impairment_answers_score if emotional_impairment_answers_score >= 2.01 and emotional_impairment_answers_score <= 3.00 else "-",
            "muy_alto": emotional_impairment_answers_score if emotional_impairment_answers_score >= 3.01 else "-"
        },
        "deterioro_cognitivo": {
            "bajo": cognitive_impairment_answers_score if cognitive_impairment_answers_score >= 1.00 and cognitive_impairment_answers_score <= 1.66 else "-",
            "normal": cognitive_impairment_answers_score if cognitive_impairment_answers_score >= 1.67 and cognitive_impairment_answers_score <= 2.33 else "-",
            "alto": cognitive_impairment_answers_score if cognitive_impairment_answers_score >= 2.34 and cognitive_impairment_answers_score <= 3.32 else "-",
            "muy_alto": cognitive_impairment_answers_score if cognitive_impairment_answers_score >= 3.33 else "-"
        }
    }




    return render_template("my_results.html", user=current_user, info_dict=info_dict,text="")



@app.route("/send_gpt", methods = ['GET','POST'])
def send_gpt():
    text = request.form.get('gpt4')
    messages = [{"role": "user", "content": text}]
    response = GPTJ.chat_completion(messages,streaming=False)
    result = response['choices'][0]['message']['content']
    return jsonify(result)
