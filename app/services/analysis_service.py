from typing import Dict

from app.services.schemas.schemas import Question, AnalyzedQuestion


async def analyze_question(question: Question) -> AnalyzedQuestion:
    analyzed_responses = {} if __is_freetext_question(question.type) or not question.responses \
        else __analyze_responses(question)
    analyzed_respondents = {} if not question.responses \
        else __analyze_respondents(question)

    return AnalyzedQuestion(
        **dict(question),
        analysis_responses=analyzed_responses,
        analysis_respondents=analyzed_respondents
    )


def __is_freetext_question(question_type: int) -> bool:
    return question_type == 1


def __analyze_respondents(question: Question) -> Dict[str, int]:
    anonym_responses = sum(1 for response in question.responses if response.respondent_id is None)
    logged_in_responses = len(question.responses) - anonym_responses
    return {
        'Anonymous Users': anonym_responses,
        'Signed in Users': logged_in_responses
    }


def __analyze_responses(question: Question) -> Dict[str, int]:
    response_texts = [response.response_text for response in question.responses]
    return {
        option: sum(response_text.count(option) for response_text in response_texts)
        for option in question.options
    }
