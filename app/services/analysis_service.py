from uuid import UUID

from app.clients import client
from app.clients.exceptions.no_response_exception import NoResponseException
from app.clients.exceptions.wrong_question_type_exception import WrongQuestionTypeException
from app.clients.schemas.schemas import Question


async def analyze_question(question_id: UUID) -> Question:
    question = await client.fetch_question(question_id)
    __check_question_type(question, question_id)
    __check_question_responses(question, question_id)
    __analyze_respondents(question)
    __analyze_responses(question)
    return question


def __check_question_type(question, question_id):
    if not __question_type_is_valid(question.type):
        raise WrongQuestionTypeException(
            f"Question with id {question_id} has the wrong type for this analysis. type {question.type}"
        )


def __check_question_responses(question, question_id):
    if not question.responses:
        raise NoResponseException(
            f"No responses found for question with id {question_id}"
        )


def __question_type_is_valid(question_type: int) -> bool:
    return True if question_type in {2, 3} else False


def __analyze_respondents(question: Question):
    total_responses = len(question.responses)
    anonym_responses = sum(1 for response in question.responses if response.respondent_id is None)
    question.analysis_respondents = {
        'total': total_responses,
        'anonym': anonym_responses
    }


def __analyze_responses(question):
    question.analysis_responses = {
        option: sum(response.response_text.count(option) for response in question.responses)
        for option in question.options
    }
