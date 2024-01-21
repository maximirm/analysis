import unittest
from uuid import uuid4
from fastapi.testclient import TestClient
from app.services.schemas.schemas import AnalyzedQuestion
from main import app


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_analyze_question_valid(self):
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
        self.assertEqual(analyzed_question.analysis_respondents, {"Total": 3, "Anonym": 2})
        self.assertEqual(analyzed_question.analysis_responses, {"Red": 3, "Blue": 2, "Green": 2, "Yellow": 1})

    def test_analyze_question_wrong_type(self):
        wrong_type = 1
        question_data = {
            "id": str(uuid4()),
            "survey_id": str(uuid4()),
            "order": 2,
            "question_text": "What is your favorite color?",
            "type": wrong_type
        }

        response = self.client.post("/analyze/question/", json=question_data)

        self.assertEqual(response.status_code, 422)

    def test_analyze_question_no_responses(self):
        no_responses = []
        question_data = {
            "id": str(uuid4()),
            "survey_id": str(uuid4()),
            "order": 2,
            "question_text": "What is your favorite color?",
            "type": 2,
            "options": ["Red", "Blue", "Green", "Yellow"],
            "responses": no_responses
        }

        response = self.client.post("/analyze/question/", json=question_data)

        self.assertEqual(response.status_code, 404)
