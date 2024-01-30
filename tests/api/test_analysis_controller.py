import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.services.schemas import schemas
from main import app


class TestAnalysisController(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch("app.services.analysis_service.analyze_question")
    def test_create_question(self, mock_analyze_question):
        analyze_question_data = {
            "id": str(uuid4()),
            "survey_id": str(uuid4()),
            "order": 1,
            "question_text": "text",
            "type": 1,
            "options": [],
            "responses": [{
                "id": str(uuid4()),
                "question_id": str(uuid4()),
                "respondent_id": None,
                "response_text": ["Red"],
            }]
        }

        mock_analyzed_question = MagicMock(analysis_responses={}, analysis_respondents={}, **analyze_question_data)
        mock_analyze_question.return_value = mock_analyzed_question

        response = self.client.post("/analyze/question/", json=analyze_question_data)
        print(response.json())
        assert response.status_code == 200
        assert response.json() == {
            "analysis_responses": {},
            "analysis_respondents": {},
            **analyze_question_data
        }

        mock_analyze_question.assert_called_once_with(schemas.Question(**analyze_question_data))
