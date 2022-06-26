import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

DATABASE_URL = "kelechi:kelechi96@localhost:5432"
DATABASE_NAME = "trivia_test"

NEW_QUESTION_MOCK = {
    "question": "What is the status code for - I'm a teapot",
    "answer": "418",
    "difficulty": "4",
    "category": 1,
}


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DATABASE_NAME
        self.database_path = "postgres://{}/{}".format(DATABASE_URL, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TEST CASES
    """

    def test_get_categories(self):
        """GET request should return list of categories"""
        res = self.client().get("/categories")
        payload = res.get_json()
        self.assertTrue(payload)
        self.assertEqual(res.status_code, 200)

    def test_get_questions(self):
        """GET request should return questions parameters"""
        res = self.client().get("/questions")
        payload = res.get_json()
        questions = payload["questions"]
        total_questions = payload["total_questions"]
        categories = payload["categories"]
        self.assertEqual(res.status_code, 200)
        self.assertTrue(categories)
        self.assertTrue(questions)
        self.assertTrue(total_questions)

    def test_delete_question(self):
        """DELETE request should delete question by id"""
        QUESTION_ID = 5
        res = self.client().delete("/questions/{}".format(QUESTION_ID))
        payload = res.get_json()
        success = payload["success"]
        self.assertEqual(res.status_code, 200)
        self.assertTrue(success)

    def test_delete_question_err_404(self):
        """DELETE request should return 404 if question does not exist"""
        QUESTION_ID = 10000000000
        res = self.client().delete("/questions/{}".format(QUESTION_ID))
        self.assertEqual(res.status_code, 404)

    def test_create_question(self):
        """POST request should create question"""
        res = self.client().post("/questions", json=NEW_QUESTION_MOCK)
        payload = res.get_json()
        success = payload["success"]
        self.assertEqual(res.status_code, 200)
        self.assertTrue(success)

    def test_create_question_err_bad_input(self):
        """POST request should check category exist"""
        bad_input = NEW_QUESTION_MOCK
        bad_input["category"] = 10000
        res = self.client().post("/questions", json=bad_input)
        self.assertEqual(res.status_code, 400)

    def test_search_question(self):
        """POST request should search questions"""
        PAYLOAD = {"searchTerm": "good"}
        res = self.client().post("/questions/search", json=PAYLOAD)
        payload = res.get_json()
        success = payload["success"]
        self.assertEqual(res.status_code, 200)
        self.assertTrue(success)

    def test_get_question_by_category(self):
        """GET should return question by category"""
        CATEGORY_ID = 1
        res = self.client().get("/categories/{}/questions".format(CATEGORY_ID))
        payload = res.get_json()
        success = payload["success"]
        questions = payload["questions"]
        self.assertTrue(success)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(questions)

    def test_get_quizzes(self):
        """POST should return random quizzes"""
        PAYLOAD = {"previous_questions": [1], "quiz_category": {"type": "All"}}
        res = self.client().post("/quizzes", json=PAYLOAD)
        payload = res.get_json()
        success = payload["success"]
        question1 = payload["question"]
        self.assertEqual(res.status_code, 200)
        self.assertTrue(success)
        self.assertTrue(question1)
        ## second question
        res = self.client().post("/quizzes", json=PAYLOAD)
        payload2 = res.get_json()
        question2 = payload2["question"]
        self.assertNotEqual(question1, question2)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
