import uuid

import loguru
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.exception import ChatError
from src.app.chatbot import models, repository, schemas as sch, enums
from src.app.services.llm_api import LLMApiService


class ChatService:

    def __init__(
        self,
        chat_repository: repository.ChatRepository,
        chat_message_repository: repository.ChatMessageRepository,
        session_ext: AsyncSession,
    ):
        self.chat_repository = chat_repository
        self.chat_message_repository = chat_message_repository
        self.session_ext = session_ext
        self.llm_api_service = LLMApiService()

    async def construct_query(self, prompt: str):
        return await self.llm_api_service.construct_query(user_question=prompt, user_instruction=None)

    async def query_external_db(self, query: str):
        try:
            query = sa.text(query)
            query_execution = await self.session_ext.execute(query)
            query_response = query_execution.all()
            query_response = str(query_response)
            status = enums.ChatMessageResponseStatusEnum.QUERY_EXECUTION_COMPLETED
        except Exception as e:
            query_response = None
            status = enums.ChatMessageResponseStatusEnum.QUERY_EXECUTION_FAILED
            loguru.logger.error(f"Query execution failed: {e}")
        return {"query_response": query_response, "status": status}

    async def construct_insight(self, prompt: str, query: str, query_response: str):
        return await self.llm_api_service.get_insights_response(user_question=prompt, query=query, query_result=query_response)

    async def ask(self, prompt: str) -> dict[str, str | None]:
        loguru.logger.info(f"Constructing query... prompt: {prompt}")
        response_1 = await self.construct_query(prompt)
        loguru.logger.info(f"Query response: {response_1}")
        status = response_1.get("status")
        if status != enums.ChatMessageResponseStatusEnum.QUERY_COMPLETED:
            raise ChatError(status=enums.ChatMessageResponseStatusEnum.QUERY_FAILED, detail="Query construction failed")
        llm_response_id = response_1.get("id")
        query = response_1.get("query")
        confidence_score = response_1.get("confidence_score")

        loguru.logger.info(f"Querying external database... query: {query}")
        response_2 = await self.query_external_db(query)
        loguru.logger.info(f"Query response: {response_2}")
        status = response_2.get("status")
        if status != enums.ChatMessageResponseStatusEnum.QUERY_EXECUTION_COMPLETED:
            raise ChatError(status=enums.ChatMessageResponseStatusEnum.QUERY_EXECUTION_FAILED, detail="Query execution failed")
        query_response = response_2.get("query_response")

        loguru.logger.info(f"Constructing insight... prompt: {prompt}, query: {query}, query_response: {query_response}")
        response_3 = await self.construct_insight(prompt, query, query_response)
        loguru.logger.info(f"Insight response: {response_3}")
        status = response_3.get("status")
        if status != enums.ChatMessageResponseStatusEnum.INSIGHT_COMPLETED:
            raise ChatError(status=enums.ChatMessageResponseStatusEnum.INSIGHT_FAILED, detail="Insight construction failed")
        insights_response = response_3.get("insights_response")
        query_explanation = response_3.get("query_explanation")

        response = {
            "llm_response_id": llm_response_id,
            "query": query,
            "confidence_score": confidence_score,
            "query_response": query_response,
            "query_explanation": query_explanation,
            "insights_response": insights_response,
        }

        return response

    async def create_message(self, obj_in: sch.ChatMessageCreateRequestSch, chat_id: uuid.UUID):
        try:
            response = await self.ask(obj_in.question)
            loguru.logger.info(response)
            status = enums.ChatMessageResponseStatusEnum.COMPLETED
        except ChatError as e:
            response = dict()
            status = e.status
            loguru.logger.error(f"Chat error: {e}")
        except Exception as e:
            response = dict()
            status = enums.ChatMessageResponseStatusEnum.ERROR
            loguru.logger.error(f"Exception: {e}")
        finally:
            llm_response_id = response.get("llm_response_id")
            query = response.get("query")
            confidence_score = response.get("confidence_score")
            query_response = response.get("query_response")
            insights_response = response.get("insights_response")
            query_explanation = response.get("query_explanation")

            obj_in_ = sch.ChatMessageCreateSch(
                question=obj_in.question,
                llm_response_id=llm_response_id,
                query=query,
                confidence_score=confidence_score,
                query_explanation=query_explanation,
                query_response=query_response,
                response=insights_response,
                status=status,
            )
            loguru.logger.info(f"Creating chat message: {obj_in_} for chat_id: {chat_id}")
            return await self.chat_message_repository.create(obj_in=obj_in_, chat_id=chat_id)

    async def update_message(self, obj_db: models.ChatMessageModel, obj_in: sch.ChatMessageUpdateSch):
        await self.llm_api_service.validate_answer(question_id=obj_db.llm_response_id, is_valid=obj_in.is_valid)
        return await self.chat_message_repository.update(obj_db=obj_db, obj_in=obj_in)

    async def create_chat(self, obj_in: sch.ChatMessageCreateRequestSch):
        chat_obj_in = {}
        chat_db = await self.chat_repository.create(obj_in=chat_obj_in)
        await self.create_message(obj_in=obj_in, chat_id=chat_db.id)
        await self.chat_repository.async_session.refresh(chat_db)
        return chat_db
