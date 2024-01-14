from uuid import UUID

from fastapi import APIRouter

from app.clients.exceptions.no_response_exception import NoResponseException
from app.clients.exceptions.question_not_found_exception import QuestionNotFoundException
from app.clients.exceptions.wrong_question_type_exception import WrongQuestionTypeException
from app.clients.schemas import schemas
from fastapi import HTTPException

from app.services import analysis_service

router = APIRouter()


@router.get("/analyze/question/{question_id}", response_model=schemas.QuestionAnalyzed)
async def analyze_question(question_id: UUID):
    try:
        return await analysis_service.analyze_question(question_id)
    except WrongQuestionTypeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NoResponseException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except QuestionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

