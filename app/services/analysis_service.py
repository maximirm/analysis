from typing import Dict

from fastapi import HTTPException

from app.services.schemas.schemas import Question, AnalyzedQuestion


async def analyze_question(question: Question) -> AnalyzedQuestion:
    if not __question_type_is_valid(question.type):
        raise HTTPException(
            status_code=422,
            detail=f"Question with id {question.id} has the wrong type for this analysis. type {question.type}"
        )
    if not question.responses:
        raise HTTPException(
            status_code=404,
            detail=f"No responses found for question with id {question.id}"
        )
    analyzed_question = AnalyzedQuestion(
        **dict(question),
        analysis_responses=__analyze_responses(question),
        analysis_respondents=__analyze_respondents(question)
    )

    return analyzed_question


def __question_type_is_valid(question_type: int) -> bool:
    return question_type in {2, 3}


def __analyze_respondents(question: Question) -> Dict[str, int]:
    total_responses = len(question.responses)
    anonym_responses = sum(1 for response in question.responses if response.respondent_id is None)
    return {
        'Total': total_responses,
        'Anonym': anonym_responses
    }


def __analyze_responses(question: Question) -> Dict[str, int]:
    response_texts = [response.response_text for response in question.responses]
    return {
        option: sum(response_text.count(option) for response_text in response_texts)
        for option in question.options
    }
