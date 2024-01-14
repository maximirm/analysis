import json
from uuid import UUID

import httpx

from fastapi import HTTPException


from app.clients.schemas.schemas import Question


async def fetch_question(question_id: UUID) -> Question:
    url = f"http://localhost:8000/questions/{question_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        question_data = response.json()
        return Question(**question_data)
    raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])
