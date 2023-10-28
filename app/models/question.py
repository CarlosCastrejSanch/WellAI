from app import db
from datetime import datetime

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    questions = db.relationship('Question', backref='questionnaire', lazy=True)

    def __repr__(self):
        return f'<Questionnaire id={self.id} title={self.title}>'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    category = db.Column(db.String(255))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))



class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime)

    @property
    def score(self):
        if self.value == 'Nunca':
            return 1
        elif self.value == 'Raramente':
            return 2
        elif self.value == 'Algunas veces':
            return 3
        elif self.value == 'A menudo':
            return 4
        else:
            return 5

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    submitted_at = db.Column(db.DateTime)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
