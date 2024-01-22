from typing import Dict

from fastapi import HTTPException

from app.services.schemas.schemas import Question, AnalyzedQuestion, AnalyzedSurvey, Survey


async def analyze_survey(survey: Survey) -> AnalyzedSurvey:
    analyzed_survey = AnalyzedSurvey.from_survey(survey)
    for question in survey.questions:
        analyzed_question = await analyze_question(question)
        analyzed_survey.analyzed_questions.append(analyzed_question)
    return analyzed_survey


async def analyze_question(question: Question) -> AnalyzedQuestion:
    if not question.responses:
        return AnalyzedQuestion(
            **dict(question),
            analysis_responses={},
            analysis_respondents={}
        )
    analyzed_question = AnalyzedQuestion(
        **dict(question),
        analysis_responses=__analyze_responses(question),
        analysis_respondents=__analyze_respondents(question)
    )

    return analyzed_question


def __is_freetext_question(question_type: int) -> bool:
    return question_type == 1


def __analyze_respondents(question: Question) -> Dict[str, int]:
    total_responses = len(question.responses)
    anonym_responses = sum(1 for response in question.responses if response.respondent_id is None)
    return {
        'Total': total_responses,
        'Anonym': anonym_responses
    }


def __analyze_responses(question: Question) -> Dict[str, int]:
    if __is_freetext_question(question.type):
        return {}
    response_texts = [response.response_text for response in question.responses]
    return {
        option: sum(response_text.count(option) for response_text in response_texts)
        for option in question.options
    }
