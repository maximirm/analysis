import unittest
from unittest.mock import AsyncMock
from uuid import UUID
from app.clients import client
from app.clients.exceptions.no_response_exception import NoResponseException
from app.clients.exceptions.wrong_question_type_exception import WrongQuestionTypeException
from app.clients.schemas.schemas import Question, Response, QuestionAnalyzed
from app.services.analysis_service import analyze_question


class TestAnalysisService(unittest.IsolatedAsyncioTestCase):
    async def test_analyze_question_valid(self):
        mock_question = Question(
            id=UUID('ceb68515-4cee-43b4-8943-b7931af93633'),
            survey_id=UUID('d03b04f7-4c03-4e8e-b9a1-60d9bebe7b14'),
            order=2,
            question_text="What is your favorite color?",
            type=2,
            options=["Red", "Blue", "Green", "Yellow"],
            responses=[
                Response(
                    id=UUID('0250ee07-5546-402a-9599-2f51d49e39cd'),
                    question_id=UUID('ceb68515-4cee-43b4-8943-b7931af93633'),
                    respondent_id=None,
                    response_text=["Red", "Blue"]),
                Response(
                    id=UUID('0250ee07-5546-402a-9599-2f51d49e39cd'),
                    question_id=UUID('ceb68515-4cee-43b4-8943-b7931af93633'),
                    respondent_id=None,
                    response_text=["Red", "Green"]),
                Response(
                    id=UUID('0250ee07-5546-402a-9599-2f51d49e39cd'),
                    question_id=UUID('ceb68515-4cee-43b4-8943-b7931af93633'),
                    respondent_id=UUID('f5b51a70-d2d5-4f76-af29-089667b8b725'),
                    response_text=["Red", "Green", "Blue", "Yellow"]),
            ]
        )
        mock_fetch_question = AsyncMock(return_value=mock_question)
        client.fetch_question = mock_fetch_question

        result = await analyze_question(UUID('ceb68515-4cee-43b4-8943-b7931af93633'))

        self.assertIsInstance(result, QuestionAnalyzed)
        self.assertEqual({'total': 3, 'anonym': 2}, result.analysis_respondents)
        self.assertEqual({'Red': 3, 'Blue': 2, 'Green': 2, 'Yellow': 1}, result.analysis_responses)
        mock_fetch_question.assert_called_once_with(UUID('ceb68515-4cee-43b4-8943-b7931af93633'))

    async def test_analyze_question_wrong_type(self):
        mock_question = Question(
            id=UUID('ceb68515-4cee-43b4-8943-b7931af93633'),
            survey_id=UUID('d03b04f7-4c03-4e8e-b9a1-60d9bebe7b14'),
            order=2,
            question_text="What is your favorite color?",
            type=1
        )
        mock_fetch_question = AsyncMock(return_value=mock_question)
        client.fetch_question = mock_fetch_question

        with self.assertRaises(WrongQuestionTypeException):
            await analyze_question(UUID('ceb68515-4cee-43b4-8943-b7931af93633'))

        mock_fetch_question.assert_called_once_with(UUID('ceb68515-4cee-43b4-8943-b7931af93633'))

    async def test_analyze_question_no_responses(self):
        mock_question = Question(
            id=UUID('ceb68515-4cee-43b4-8943-b7931af93633'),
            survey_id=UUID('d03b04f7-4c03-4e8e-b9a1-60d9bebe7b14'),
            order=2,
            question_text="What is your favorite color?",
            type=2,
            options=["Red", "Blue", "Green", "Yellow"],
            responses=[]
        )
        mock_fetch_question = AsyncMock(return_value=mock_question)
        client.fetch_question = mock_fetch_question

        with self.assertRaises(NoResponseException):
            await analyze_question(UUID('ceb68515-4cee-43b4-8943-b7931af93633'))

        mock_fetch_question.assert_called_once_with(UUID('ceb68515-4cee-43b4-8943-b7931af93633'))
