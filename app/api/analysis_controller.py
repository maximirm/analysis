from fastapi import APIRouter

from app.services import analysis_service
from app.services.schemas import schemas

router = APIRouter()


@router.post("/analyze/question", response_model=schemas.QuestionAnalyzed)
async def analyze_question(question: schemas.Question):
    return await analysis_service.analyze_question(question)
