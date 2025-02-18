import uuid

import httpx

from src.app.core.config import settings


class LLMApiService:
    def __init__(self):
        url = "http://localhost:8001"
        self.client = httpx.Client(base_url=url)

    async def construct_query(self, user_question: str, user_instruction: str):
        url = "/sql_generator"
        body = {
            "user_question": user_question,
            "user_instruction": user_instruction,
        }
        response = self.client.post(url=url, json=body)
        return response.json()

    async def validate_answer(self, question_id: uuid.UUID, is_valid: bool):
        url = f"/sql_generator/{question_id}"
        body = {"is_correct": is_valid}
        response = self.client.patch(url=url, json=body)
        return response.json()

    async def get_insights_response(self, user_question: str, query_result: str):
        url = "/insight_generator"
        body = {
            "user_question": user_question,
            "query_result": query_result,
        }
        response = self.client.post(url=url, json=body)
        return response.json()
