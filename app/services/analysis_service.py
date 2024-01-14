from uuid import UUID

from app.clients import client
from app.clients.exceptions.no_response_exception import NoResponseException
from app.clients.exceptions.wrong_question_type_exception import WrongQuestionTypeException
from app.clients.schemas.schemas import Question, QuestionAnalyzed


async def analyze_question(question_id: UUID) -> QuestionAnalyzed:
    question = await client.fetch_question(question_id)

    if not __question_type_is_valid(question.type):
        raise WrongQuestionTypeException(
            f"Question with id {question_id} has the wrong type for this analysis. type {question.type}"
        )
    if not question.responses:
        raise NoResponseException(
            f"No responses found for question with id {question_id}"
        )

    analyzed_question = QuestionAnalyzed(
        **dict(question),
        analysis_responses=__analyze_responses(question),
        analysis_respondents=__analyze_respondents(question)
    )

    return analyzed_question


def __question_type_is_valid(question_type: int) -> bool:
    return True if question_type in {2, 3} else False


def __analyze_respondents(question: Question):
    total_responses = len(question.responses)
    anonym_responses = sum(1 for response in question.responses if response.respondent_id is None)
    return {
        'total': total_responses,
        'anonym': anonym_responses
    }


def __analyze_responses(question):
    return {
        option: sum(response.response_text.count(option) for response in question.responses)
        for option in question.options
    }
