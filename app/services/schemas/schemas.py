from typing import Optional, List

from pydantic import BaseModel, UUID4


class Response(BaseModel):
    id: UUID4
    question_id: UUID4
    respondent_id: Optional[UUID4] = None
    response_text: List[str]


class Question(BaseModel):
    id: UUID4
    survey_id: UUID4
    order: int
    question_text: str
    type: int
    options: Optional[List[str]] = None
    responses: list[Response] = []


class AnalyzedQuestion(Question):
    analysis_responses: Optional[dict] = None
    analysis_respondents: Optional[dict] = None


class Survey(BaseModel):
    creator_id: UUID4
    title: str
    description: str
    id: UUID4
    questions: list[Question] = []


class AnalyzedSurvey(BaseModel):
    creator_id: UUID4
    title: str
    description: str
    id: UUID4
    analyzed_questions: list[AnalyzedQuestion] = []

    @classmethod
    def from_survey(cls, survey: Survey):
        return cls(
            creator_id=survey.creator_id,
            title=survey.title,
            description=survey.description,
            id=survey.id
        )

