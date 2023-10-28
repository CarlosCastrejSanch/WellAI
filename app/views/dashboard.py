from app import app
from flask import render_template, jsonify, request
from flask_login import current_user, login_required
from ..models import Answer, Question, Submission, EmployeeList,User
from sqlalchemy import and_, or_

def get_answers_with_same_corp_id(corp_id):
    users_with_same_corp_id = EmployeeList.query.filter_by(corp_id=corp_id).all()
    user_ids = []
    for u in users_with_same_corp_id:
        user = User.query.filter_by(email=u.email).first()
        user_ids.append(user.id)
    answers = Answer.query.filter(Answer.user.in_(user_ids)).all()
    return answers



def get_users_with_same_corp(corp_id):
    users_with_same_corp_id = EmployeeList.query.filter_by(corp_id=corp_id).all()
    user_ids = []
    for u in users_with_same_corp_id:
        user = User.query.filter_by(email=u.email).first()
        user_ids.append(user.id)
    return user_ids

@app.route("/dashboard", methods = ['GET','POST'])
@login_required
def dashboard():
    if current_user.is_employee:
        answers = Answer.query.filter_by(user=current_user.id).all()
        questions = Question.query.all()
        list_questions = []
        for q in questions:
            list_questions.append(q.text)

        chart_data = []
        if answers is not None:
            chart_data = [
              {"date":answer.timestamp.strftime('%Y-%m-%D'),
             "value":answer.value,
             "score":answer.score,
             "category": Question.query.filter_by(id=answer.question_id).first().category
             }
                    for answer in answers]
            
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


        return render_template("employee_dashboard.html", user=current_user,chart_data=chart_data,list_questions=list_questions,avg_data=avg_data)

    answers = Answer.query.all()
    if current_user.is_corp:
        answers = get_answers_with_same_corp_id(current_user.id)
    if current_user.is_doctor:
        corp_id = EmployeeList.query.filter_by(email=current_user.email).first()
        answers = get_answers_with_same_corp_id(corp_id.corp_id)
    questions = Question.query.all()
    list_questions = []
    for q in questions:
        list_questions.append(q.text)

    roles=[]
    employees = EmployeeList.query.all()
    if employees is not None:
        roles = list(set([employee.role for employee in employees]))
    
    chart_data = []
    avg_data={}
    if answers is not None:
        chart_data = [
            {"date":answer.timestamp.strftime('%Y-%m-%D'),
             "value":answer.value,
             "score":answer.score,
             "category": Question.query.filter_by(id=answer.question_id).first().category
             }
             for answer in answers]
    

        exhaustion_answers = [answer for answer in answers if Question.query.get(answer.question_id).category == "Agotamiento"]

        mental_distance_answers = [answer for answer in answers if Question.query.get(answer.question_id).category == "Distancia mental"]
        
        emotional_impairment_answers = [answer for answer in answers if Question.query.get(answer.question_id).category == "Deterioro emocional"]

        cognitive_impairment_answers = [answer for answer in answers if Question.query.get(answer.question_id).category == "Deterioro cognitivo"]

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


    return render_template("dashboard.html", user=current_user,chart_data=chart_data,list_questions=list_questions,roles=roles,avg_data=avg_data)



@app.route("/filter_by_last_submit", methods = ['GET','POST'])
def filter_by_last_submit():
    submit_num = request.form.get('lastSubmitSelect')
    answers = Answer.query.all()
    corp_id = EmployeeList.query.filter_by(email=current_user.email).first()
    if current_user.is_corp:
        answers = get_answers_with_same_corp_id(current_user.id)
    if current_user.is_doctor:
        answers = get_answers_with_same_corp_id(corp_id.corp_id)

    if submit_num == "last-one":
        submission = Submission.query.order_by(Submission.id.desc()).limit(1).all()
        if len(submission)==1:
            if current_user.is_corp:
                answers = Answer.query.filter(and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(current_user.id)))).all()
            if current_user.is_doctor:
                answers = Answer.query.filter(and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id)))).all()
    
    elif submit_num == "last-tow":
        submission = Submission.query.order_by(Submission.id.desc()).limit(2).all()
        if len(submission)==2:
            if current_user.is_corp:
                answers = Answer.query.filter( or_(
                and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                     ) 
                ).all()
            if current_user.is_doctor:
                answers = Answer.query.filter( or_(
                and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                     ) 
                ).all()

    elif submit_num == "last-three":
        submission = Submission.query.order_by(Submission.id.desc()).limit(3).all()
        if len(submission)==3:
            if current_user.is_corp:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                        ) 
                    ).all()
            if current_user.is_doctor:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                        ) 
                    ).all()
    elif submit_num == "last-four":
        submission = Submission.query.order_by(Submission.id.desc()).limit(4).all()
        if len(submission)==4:
            if current_user.is_corp:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                        ) 
                        ).all()
            if current_user.is_doctor:
                answers = Answer.query.filter( or_(
                and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    ) 
                ).all()
    elif submit_num == "last-five":
        submission = Submission.query.order_by(Submission.id.desc()).limit(5).all()
        if len(submission)==5:
            if current_user.is_corp:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[4].submitted_at, Answer.user==submission[4].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                        ) 
                    ).all()
            if current_user.is_doctor:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[4].submitted_at, Answer.user==submission[4].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                        ) 
                    ).all()
                
    elif submit_num == "last-six":
        submission = Submission.query.order_by(Submission.id.desc()).limit(6).all()
        if len(submission)==6:
            if current_user.is_corp:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[4].submitted_at, Answer.user==submission[4].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[5].submitted_at, Answer.user==submission[5].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                        ) 
                    ).all()
            if current_user.is_doctor:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[4].submitted_at, Answer.user==submission[4].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[5].submitted_at, Answer.user==submission[5].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                        ) 
                    ).all()
    elif submit_num == "last-seven":
        submission = Submission.query.order_by(Submission.id.desc()).limit(7).all()
        if len(submission)==7:
            
            if current_user.is_corp:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[4].submitted_at, Answer.user==submission[4].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[5].submitted_at, Answer.user==submission[5].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[6].submitted_at, Answer.user==submission[6].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                        ) 
                    ).all()
            if current_user.is_doctor:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[4].submitted_at, Answer.user==submission[4].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[5].submitted_at, Answer.user==submission[5].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[6].submitted_at, Answer.user==submission[6].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                        ) 
                    ).all()
                
    elif submit_num == "last-eight":
        submission = Submission.query.order_by(Submission.id.desc()).limit(8).all()
        if len(submission)==8:
            if current_user.is_corp:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[4].submitted_at, Answer.user==submission[4].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[5].submitted_at, Answer.user==submission[5].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[6].submitted_at, Answer.user==submission[6].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[7].submitted_at, Answer.user==submission[7].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                        ) 
                    ).all()
            if current_user.is_doctor:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[4].submitted_at, Answer.user==submission[4].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[5].submitted_at, Answer.user==submission[5].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[6].submitted_at, Answer.user==submission[6].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[7].submitted_at, Answer.user==submission[7].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                        ) 
                    ).all()
    elif submit_num == "last-nine":
        submission = Submission.query.order_by(Submission.id.desc()).limit(9).all()
        if len(submission)==9:
            if current_user.is_corp:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[4].submitted_at, Answer.user==submission[4].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[5].submitted_at, Answer.user==submission[5].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[6].submitted_at, Answer.user==submission[6].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[7].submitted_at, Answer.user==submission[7].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                    and_(Answer.timestamp==submission[8].submitted_at, Answer.user==submission[8].user,Answer.user.in_(get_users_with_same_corp(current_user.id))),
                        ) 
                    ).all()
            if current_user.is_doctor:
                answers = Answer.query.filter( or_(
                    and_(Answer.timestamp==submission[0].submitted_at, Answer.user==submission[0].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[1].submitted_at, Answer.user==submission[1].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[2].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[2].submitted_at, Answer.user==submission[3].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[4].submitted_at, Answer.user==submission[4].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[5].submitted_at, Answer.user==submission[5].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[6].submitted_at, Answer.user==submission[6].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[7].submitted_at, Answer.user==submission[7].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                    and_(Answer.timestamp==submission[8].submitted_at, Answer.user==submission[8].user,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))),
                        ) 
                    ).all()
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





@app.route("/filter_by_role", methods = ['GET','POST'])
def filter_by_role():
    role = request.form.get('role')
    corp_id = EmployeeList.query.filter_by(email=current_user.email).first()
    answers = Answer.query.join(User).filter(User.role == role,Answer.user.in_(get_users_with_same_corp(current_user.id))).all()
    if current_user.is_doctor:
        answers = Answer.query.join(User).filter(User.role == role,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))).all()
    if role == "all-roles":
        answers = Answer.query.filter(Answer.user.in_(get_users_with_same_corp(current_user.id))).all()
        if current_user.is_doctor:
            answers = Answer.query.filter(Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))).all()
    
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



@app.route("/filter_by_gender", methods = ['GET','POST'])
def filter_by_gender():
    gender = request.form.get('gender')
    corp_id = EmployeeList.query.filter_by(email=current_user.email).first()
    answers = Answer.query.join(User).filter(User.gender == gender,Answer.user.in_(get_users_with_same_corp(current_user.id))).all()
    if current_user.is_doctor:
        answers = Answer.query.join(User).filter(User.gender == gender,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))).all()
    if gender == "all-genders":
        answers = Answer.query.filter(Answer.user.in_(get_users_with_same_corp(current_user.id))).all()
        if current_user.is_doctor:
            answers = Answer.query.filter(Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))).all()
            
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


@app.route("/filter_by_question", methods = ['GET','POST'])
def filter_by_question():
    question = request.form.get('question')
    answers = ""
    corp_id = EmployeeList.query.filter_by(email=current_user.email).first()
    if question == "All":
        answers=Answer.query.filter(Answer.user.in_(get_users_with_same_corp(current_user.id))).all()
    else:
        question_id = Question.query.filter_by(text=question).first()
        answers = Answer.query.filter(Answer.question_id==question_id.id,Answer.user.in_(get_users_with_same_corp(current_user.id))).all()
        if current_user.is_doctor:
            answers = Answer.query.filter(Answer.question_id==question_id.id,Answer.user.in_(get_users_with_same_corp(corp_id.corp_id))).all()
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