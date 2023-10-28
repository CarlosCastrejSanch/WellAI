from app import app,db
from flask import render_template,jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models.question import Question,Answer, Submission
from datetime import datetime, timedelta
import random

@app.route("/", methods = ['GET','POST'])
@login_required
def home():

    if current_user.is_doctor or current_user.is_corp:
        return redirect(url_for('dashboard'))
    questions = Question.query.filter_by(questionnaire_id=1).order_by(Question.category).all()
    choices = [ 
        'Nunca',
        'Raramente',
        'Algunas veces',
        'A menudo',
        'Siempre'
    ]
    submission = Submission.query.filter_by(user=current_user.id).order_by(Submission.id.desc()).first()
    current_date = datetime.now() 
    submited = False
    if submission:
        next_week = submission.submitted_at + timedelta(weeks=1)
        if current_date <= next_week:
            submited= True

    return render_template("home.html", user=current_user, questions=questions,submited=submited, choices= choices)


@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    data = request.get_json()
    current_date = datetime.now()
    


    for answer in data:
        new_answer = Answer(question_id=answer['question_id'],user=current_user.id,value=answer['answer'],timestamp=current_date)
        db.session.add(new_answer)
        db.session.commit()
    submit = Submission(user=current_user.id, questionnaire_id=1, submitted_at = current_date)
    db.session.add(submit)
    db.session.commit()
    flash("El cuestionario se ha respondido correctamente", category="success")
    return jsonify({'message': 'El cuestionario se ha respondido correctamente'})

