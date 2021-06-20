import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'What is the smallest country in the world?',
            'answer': 'Vatican City',
            'category': 3,
            'difficulty': 5
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # tests get_questions() in __init__.py
    def test_get_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], None)

    def test_404_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests get_categories() in __init__.py
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    # tests delete_question() in __init__.py
    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        question = Question.query.get(5)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question_id'], 5)

    def test_404_if_question_not_found(self):
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests create_question() in __init__.py
    def test_create_question(self):
        res = self.client().post('/questions', json= self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_question_id'])

    def test_405_if_creation_not_allowed(self):
        res = self.client().post('/questions/5', json = self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

    # tests get_by_category() in __init__.py
    def test_get_by_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'History')

    def test_404_if_category_does_not_exist(self):
        res = self.client().get('/categories/5000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests search_questions() in __init__.py
    def test_search_questions(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'artist'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'],)
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(data['current_category'], None)

    #tests  get_quiz_questions() in __init__.property
    def test_get_quiz_questions(self):
        res = self.client().post('/quizzes', json={'previous_questions':[5, 9, 12], 'quiz_category': {'id': 4, 'type': 'History'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question'].get('id'), 23)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
