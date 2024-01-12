from pydantic import BaseModel, UUID4
from typing import Optional, List


class Response(BaseModel):
    id: UUID4
    question_id: UUID4
    respondent_id: Optional[UUID4] = None
    response_text: List[str]

    class Config:
        from_attributes = True


class Question(BaseModel):
    id: UUID4
    survey_id: UUID4
    order: int
    question_text: str
    type: int
    options: Optional[List[str]] = None
    responses: list[Response] = []
    analysis_responses: Optional[dict] = None
    analysis_respondents: int = None

    class Config:
        from_attributes = True


class Survey(BaseModel):
    id: UUID4
    creator_id: UUID4
    title: str
    description: str
    questions: list[Question] = []

    class Config:
        from_attributes = True