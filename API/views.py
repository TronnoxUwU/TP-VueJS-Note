from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import tasks
from .api_questionnaire import *

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

###################################################################################################
#                                   Partie task                                                   #
###################################################################################################

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_tasks', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task
# L'uri est généré par la fonction url_for() qui prend en paramètre le nom de la fonction qui gère la route et les paramètres de la route. Le paramètre _external=True permet de générer une URL absolue.

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks=[make_public_task(t) for t in tasks])

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    
    task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201

@app.route('/todo/api/v1.0/tasks', methods=['PUT'])
def update_task():
    task_id = request.args.get('task_id', type=int)
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': make_public_task(task[0])})

@app.route('/todo/api/v1.0/tasks', methods=['DELETE'])
def delete_task():
    task_id = request.args.get('task_id', type=int)
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

###################################################################################################
#                                   Partie quiz                                                   #
###################################################################################################

def make_public_quiz(quiz):
    new_quiz = {}
    for field in quiz:
        if field == 'id':
            new_quiz['uri'] = url_for('get_quiz', quiz_id=quiz['id'], _external=True)
        else:
            new_quiz[field] = quiz[field]
    return new_quiz

@app.route('/todo/api/v1.0/quiz', methods=['GET'])
def get_quiz():
    quiz = les_quiz()
    return jsonify(quiz=[make_public_quiz(q) for q in quiz])

@app.route('/todo/api/v1.0/quiz', methods=['DELETE'])
def delete_quiz():
    quiz_id = request.args.get('quiz_id', type=int)
    if not supprimer_quiz(quiz_id):
        abort(404)
    return jsonify({'result': True})

@app.route('/todo/api/v1.0/quiz', methods=['POST'])
def create_quiz():
    print(request.json)
    if not request.json or 'name' not in request.json:
        abort(400)
    return jsonify({'quiz': make_public_quiz(ajout_quiz(request.json))}), 201

@app.route('/todo/api/v1.0/quiz', methods=['PUT'])
def update_quiz():
    print(request.json)
    quiz_id = request.args.get('quiz_id', type=int) 
    if not quiz_id:
        abort(400)
    quiz = Questionnaire.query.get(quiz_id) 
    if not quiz:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json:
        if not isinstance(request.json['name'], str):
            abort(400)
        quiz.name = request.json['name']
    if 'questions' in request.json:
        if not isinstance(request.json['questions'], list):
            abort(400)

        quiz.questions = [] 

        for question_data in request.json['questions']:
            print(question_data)
            if 'name' not in question_data or 'type' not in question_data:
                abort(400, description="Each question must have a title and type")

            new_question = None
            match(question_data['type']):
                case "ouverte":
                    new_question = QuestionOuverte(
                        title=question_data['name'],
                        questionType=question_data['type'],
                        questionnaire_id=quiz.id
                    )
                case "choix":
                    new_question = QuestionChoix(
                        title=question_data['name'],
                        questionType=question_data['type'],
                        questionnaire_id=quiz.id
                    )
            quiz.questions.append(new_question)
    db.session.commit()

    return jsonify({'quiz': make_public_quiz(quiz.to_json())})