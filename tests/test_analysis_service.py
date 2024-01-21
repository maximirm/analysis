import unittest
from uuid import uuid4

from fastapi import HTTPException

from app.services.analysis_service import analyze_question
from app.services.schemas.schemas import Question, Response, AnalyzedQuestion


class TestAnalysisService(unittest.IsolatedAsyncioTestCase):
    async def test_analyze_question_with_valid_data(self):
        question_id = uuid4()
        mock_question = Question(
            id=question_id,
            survey_id=uuid4(),
            order=2,
            question_text="What is your favorite color?",
            type=2,
            options=["Red", "Blue", "Green", "Yellow"],
            responses=[
                Response(
                    id=uuid4(),
                    question_id=question_id,
                    respondent_id=None,
                    response_text=["Red", "Blue"]),
                Response(
                    id=uuid4(),
                    question_id=question_id,
                    respondent_id=None,
                    response_text=["Red", "Green"]),
                Response(
                    id=uuid4(),
                    question_id=question_id,
                    respondent_id=uuid4(),
                    response_text=["Red", "Green", "Blue", "Yellow"]),
            ]
        )
        result = await analyze_question(mock_question)

        self.assertIsInstance(result, AnalyzedQuestion)
        self.assertEqual({'Total': 3, 'Anonym': 2}, result.analysis_respondents)
        self.assertEqual({'Red': 3, 'Blue': 2, 'Green': 2, 'Yellow': 1}, result.analysis_responses)

    async def test_analyze_question_wrong_type(self):
        mock_question = Question(
            id=uuid4(),
            survey_id=uuid4(),
            order=2,
            question_text="What is your favorite color?",
            type=1
        )

        with self.assertRaises(HTTPException):
            await analyze_question(mock_question)

    async def test_analyze_question_no_responses(self):
        mock_question = Question(
            id=uuid4(),
            survey_id=uuid4(),
            order=2,
            question_text="What is your favorite color?",
            type=2,
            options=["Red", "Blue", "Green", "Yellow"],
            responses=[]
        )

        with self.assertRaises(HTTPException):
            await analyze_question(mock_question)
