
from .app import app, db
class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Questionnaire (%d) %s>" % (self.id, self.name)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'questions': [q.to_json() for q in Question.query.filter_by(questionnaire_id=self.id).all()]
        }
        return json


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    questionType = db.Column(db.String(40))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    questionnaire = db.relationship(
        "Questionnaire",
        backref=db.backref("questions", lazy="dynamic")
    )
    __mapper_args__ = {
        "polymorphic_identity": "question",
        "polymorphic_on": questionType,
    }


    def to_json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'type': self.questionType,
        }
        return json

class QuestionChoix(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "choix",
    }

class QuestionOuverte(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "ouverte",
    }


def les_quiz():
    res = []
    for Q in Questionnaire.query.all():
        res.append(Q.to_json())
    return res

def supprimer_quiz(id):
    Q = Questionnaire.query.get(id)
    if Q is not None:
        for q in Question.query.filter_by(questionnaire_id=Q.id).all():
            db.session.delete(q)
        db.session.delete(Q)
        db.session.commit()
        return True
    return False

def ajout_quiz(quiz):
    Q = Questionnaire(name=quiz['name'])
    db.session.add(Q)
    db.session.commit()
    for question in quiz.get('questions',[]):
        match(question['type']):
            case "ouverte":
                q = QuestionOuverte(
                    title=question['name'],
                    questionType=question['type'],
                    questionnaire_id=Q.id
                )
            case "choix":
                q = QuestionChoix(
                    title=question['name'],
                    questionType=question['type'],
                    questionnaire_id=Q.id
                )
        db.session.add(q)
        db.session.commit()
    return Q.to_json()
