import json
from uuid import UUID

import httpx

from app.clients.exceptions.question_not_found_exception import QuestionNotFoundException
from app.clients.schemas.schemas import Question


async def fetch_question(question_id: UUID) -> Question:
    url = f"http://localhost:8000/questions/{question_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 404:
        raise QuestionNotFoundException(json.loads(response.text)['detail'])

    question_data = response.json()
    return Question(**question_data)
