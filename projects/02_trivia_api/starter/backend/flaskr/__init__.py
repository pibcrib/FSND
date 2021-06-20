import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(lst, request):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in lst]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Sets up CORS. Allows '*' for origins.
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Uses after_request decorator to sets Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

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

    # Endpoint for GET requests for questions
    @app.route('/questions', methods=['GET'])
    def get_questions():  # DONE
        questions = Question.query.all()
        current_questions = paginate_questions(questions, request)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        return jsonify({
            'questions': current_questions,
            'total_questions': len(current_questions),
            'categories': {category.id: category.type for category in categories},
            'current_category': None
        })

    # Create an endpoint to handle GET requests for all available categories.
    @app.route('/categories', methods=['GET'])  # DONE
    def get_categories():
        categories = Category.query.all()
        return jsonify({
            'categories': {category.id: category.type for category in categories}
        })

    # Endpoint to DELETE question using a question ID.
    #     TEST: When you click the trash icon next to a question, the question will be removed.
    #     This removal will persist in the database and when you refresh the page.
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question is None:
            abort(404)

        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted_question_id': question_id
            })

        # throws error is there is an issue committing delete to the database
        except:
            abort(422)

    # Create an endpoint to POST a new question,
    #    which will require the question and answer text,
    #     category, and difficulty score.

    # TEST: When you submit a question on the "Add" tab,
    #     the form will clear and the question will appear at the end of the last page
    #     of the questions list in the "List" tab.
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        try:
            new_question = Question(
                question=body.get('question', None),
                answer=body.get('answer', None),
                category=body.get('category', None),
                difficulty=body.get('difficulty', None))

            new_question.insert()
            return jsonify({
                'success': True,
                'new_question_id': new_question.id
            })

        except:
            abort(422)

    # Creates a POST endpoint to get questions based on a search term.
    #     It should return any questions for whom the search term
    #     is a substring of the question.

    # TEST: Search by any phrase. The questions list will update to include
    #     only question that include that string within their question.
    #     Try using the word "title" to start.

    @app.route('/questions/search', methods=['POST'])
    def search_questions():  # error check?
        search_term = request.get_json()['searchTerm']
        questions = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()

        return jsonify({
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': None
        })

    # Creates a GET endpoint to get questions based on category.
    #     TEST: In the "List" tab / main screen, clicking on one of the
    #     categories in the left column will cause only questions of that
    #     category to be shown.
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_category(category_id):  # DONE, check for correctness
        questions = Question.query.filter(
            Question.category == category_id).all()
        if not questions:
            abort(404)

        category = Category.query.get(category_id)
        total_questions = Question.query.count()

        return jsonify({
            'questions': [question.format() for question in questions],
            'total_questions': total_questions,
            'current_category': category.type
        })

    # Creates a POST endpoint to get questions to play the quiz.
    #     This endpoint should take category and previous question parameters
    #     and return a random questions within the given category,
    #     if provided, and that is not one of the previous questions.

    # TEST: In the "Play" tab, after a user selects "All" or a category,
    #     one question at a time is displayed, the user is allowed to answer
    #     and shown whether they were correct or not.
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        previous_questions = request.get_json()['previous_questions']
        quiz_category_id = request.get_json()['quiz_category'].get('id')

        next_question = Question.query.filter(Question.category == quiz_category_id).filter(
            Question.id.notin_(previous_questions)).order_by(func.random()).first()

        return jsonify({
            'question': next_question.format() if next_question is not None else None
        })

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app
