from fastapi import APIRouter

from app.services import analysis_service
from app.services.schemas import schemas

router = APIRouter()


@router.post("/analyze/question/", response_model=schemas.AnalyzedQuestion)
async def analyze_question(question: schemas.Question):
    return await analysis_service.analyze_question(question)


@router.post("/analyze/survey/", response_model=schemas.AnalyzedSurvey)
async def analyze_question(survey: schemas.Survey):
    return await analysis_service.analyze_survey(survey)
