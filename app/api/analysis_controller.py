
from fastapi import APIRouter


from app.services.schemas import schemas


from app.services import analysis_service

router = APIRouter()


@router.post("/analyze/question", response_model=schemas.QuestionAnalyzed)
async def analyze_question(question: schemas.Question):

    return await analysis_service.analyze_question(question)


