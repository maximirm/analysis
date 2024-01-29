import unittest
from uuid import uuid4

from fastapi.testclient import TestClient

from app.services.schemas.schemas import AnalyzedQuestion
from main import app


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_analyze_question(self):
        question_id = str(uuid4())
        question_data = {
            "id": question_id,
            "survey_id": str(uuid4()),
            "order": 2,
            "question_text": "What is your favorite color?",
            "type": 2,
            "options": ["Red", "Blue", "Green", "Yellow"],
            "responses": [
                {
                    "id": str(uuid4()),
                    "question_id": question_id,
                    "respondent_id": None,
                    "response_text": ["Red", "Blue"]
                },
                {
                    "id": str(uuid4()),
                    "question_id": question_id,
                    "respondent_id": None,
                    "response_text": ["Red", "Green"]
                },
                {
                    "id": str(uuid4()),
                    "question_id": question_id,
                    "respondent_id": str(uuid4()),
                    "response_text": ["Red", "Green", "Blue", "Yellow"]
                }
            ]
        }

        response = self.client.post("/analyze/question/", json=question_data)

        self.assertEqual(response.status_code, 200)
        analyzed_question = AnalyzedQuestion(**response.json())
        self.assertEqual({'Anonymous Users': 2, 'Signed in Users': 1}, analyzed_question.analysis_respondents)
        self.assertEqual({"Red": 3, "Blue": 2, "Green": 2, "Yellow": 1}, analyzed_question.analysis_responses)

    def test_analyze_free_text_question(self):
        question_type_free_text = 1
        question_id = str(uuid4())
        question_data = {
            "id": question_id,
            "survey_id": str(uuid4()),
            "order": 2,
            "question_text": "What is your favorite color?",
            "type": question_type_free_text,
            "options": ["Red", "Blue", "Green", "Yellow"],
            "responses": [
                {
                    "id": str(uuid4()),
                    "question_id": question_id,
                    "respondent_id": None,
                    "response_text": ["Red", "Blue"]
                },
                {
                    "id": str(uuid4()),
                    "question_id": question_id,
                    "respondent_id": None,
                    "response_text": ["Red", "Green"]
                },
                {
                    "id": str(uuid4()),
                    "question_id": question_id,
                    "respondent_id": str(uuid4()),
                    "response_text": ["Red", "Green", "Blue", "Yellow"]
                }
            ]
        }

        response = self.client.post("/analyze/question/", json=question_data)

        self.assertEqual(response.status_code, 200)
        analyzed_question = AnalyzedQuestion(**response.json())
        self.assertEqual({'Anonymous Users': 2, 'Signed in Users': 1}, analyzed_question.analysis_respondents)
        self.assertEqual({}, analyzed_question.analysis_responses)

    def test_analyze_question_no_responses(self):
        question_id = str(uuid4())
        question_data = {
            "id": question_id,
            "survey_id": str(uuid4()),
            "order": 2,
            "question_text": "What is your favorite color?",
            "type": 2,
            "options": ["Red", "Blue", "Green", "Yellow"],
            "responses": []
        }

        response = self.client.post("/analyze/question/", json=question_data)

        self.assertEqual(response.status_code, 200)
        analyzed_question = AnalyzedQuestion(**response.json())
        self.assertEqual({}, analyzed_question.analysis_respondents)
        self.assertEqual({}, analyzed_question.analysis_responses)
