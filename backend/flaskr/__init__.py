import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [qu.format() for qu in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        my_dic = {}
        for cat in categories:
            my_dic[cat.id] = cat.type

        return jsonify({
            'success': True,
            'categories': my_dic
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():

        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {}
        for cat in categories:
            formatted_categories[cat.id] = cat.type
        current_questions = paginate_questions(request, questions)
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': formatted_categories,
            'current_category': 2,
        })

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            print(question)
            question.delete()
            return jsonify({
                'success': True,
                'message': 'Question Deleted',
                'deleted': question.id
            })
        except:
            if question is None:
                abort(404)
            else:
                abort(422)

    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        if len(question) is 0 or len(answer) is 0 or difficulty is None or category is None:
            print("question 422")
            abort(422)
        try:
            question = Question(question=question, answer=answer,
                                difficulty=difficulty, category=category)
            question.insert()
            return jsonify({
                'success': True,
                'message': 'Question Added',
                'created': question.id
            })
        except:
            abort(500)
        return app

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search_term = request.get_json()['searchTerm']
        flag = search_term.isnumeric()
        if flag is True:
            error = 422
            abort(error)
        try:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            current_questions = paginate_questions(request, questions)
            if len(questions) == 0:
                error = 404
                abort(error)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'current_category': ''
            })
        except:
            if error == 404:
                abort(404)
            elif error == 422:
                abort(422)
            else:
                abort(500)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)
            questions = Question.query.filter_by(category=category.id).all()
            current_questions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'current_category': category.id
            })
        except:
            if category is None:
                abort(404)
            else:
                abort(500)

    @app.route('/quizzes', methods=['POST'])
    def play_game():
        data = request.get_json()
        previous_questions = data.get('previous_questions', None)
        category = data.get('quiz_category', None)
        try:
            if category['type'] == 'click':
                question = Question.query.filter(~Question.id.in_(previous_questions)).first()
            else:
                question = Question.query.filter(~Question.id.in_(previous_questions),
                                                 Question.category == category['id']).first()
        except:
            abort(500)
        return jsonify({
            'success': True,
            'question': question.format()
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False,
                        'error': 400,
                        'message': "Bad Request"
                        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False,
                        'error': 404,
                        'message': "Not Found"
                        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({'success': False,
                        'error': 405,
                        'message': "Not Allowed"
                        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': False,
                        'error': 422,
                        'message': "Unprocessable Entity"
                        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'success': False,
                        'error': 500,
                        'message': "Internal Server Error"
                        }), 500

    return app
