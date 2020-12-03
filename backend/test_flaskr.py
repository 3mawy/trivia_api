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
        self.database_path = "postgres://postgres:0153@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 2,
            'category': 1
        }
        self.invalid_new_question = {
            'question': 'test question',
            'answer': '',
            'difficulty': '',
            'category': 1
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['categories'])

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue('success')
        self.assertIsNotNone(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertIsNotNone(data['categories'])
        ##self.assertTrue(data['current_category'])

    def test_404_beyond_valid_page(self):
        res = self.client().get('/questions?page=400')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not Found')

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/9')
    #     data = json.loads(res.data)
    #     question = Question.query.get(9)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['message'], 'Question Deleted')
    #     self.assertTrue(data['deleted'])
    #     self.assertIsNone(question)

    def test_404_delete_question_does_not_exist(self):
        res = self.client().delete('/questions/400')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not Found')

    ##422

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Question Added')
        self.assertIsNotNone(data['created'])

    def test_422_question_missing_fields(self):
        res = self.client().post('/questions', json=self.invalid_new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_405_add_question_not_allowed(self):
        res = self.client().post('/questions/50', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not Allowed')

    def test_question_search(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['questions'])
        self.assertTrue(data['total_questions'])
        ##self.assertTrue(data['current_category'])

    def test_422_question_search_invalid_term(self):
        res = self.client().post('/questions/search', json={'searchTerm': '5'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_404_question_search_no_results(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'randomtext'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not Found')

    ##500

    def test_questions_by_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 4)

    def test_404_questions_by_invalid_category(self):
        res = self.client().get('/categories/500/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not Found')

        ##500

        """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
