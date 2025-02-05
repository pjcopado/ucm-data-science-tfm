from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from src.app.chatbot import repository, schemas as sch


class ChatService:

    def __init__(self, repository: repository.ChatRepository):
        self.repository = repository

    async def create(self, obj_in: sch.ChatCreateSch) -> sch.ChatSch:
        return await self.repository.create(obj_in=obj_in)

    def create_prompt(self, prompt: str):
        return prompt

    async def ask(self, prompt: str):
        MODEL_NAME = "llama3.2:1b"
        LLAMA_API_KEY = "ollama"
        LLAMA_API_URL = "http://localhost:11434/v1/"

        class CityLocation(BaseModel):
            city: str
            country: str

        model = OpenAIModel(model_name=MODEL_NAME, base_url=LLAMA_API_URL, api_key=LLAMA_API_KEY)

        agent = Agent(model)  # , result_type=CityLocation)

        # result = agent.run_sync(prompt)
        result = await agent.run(prompt)
        return result.data


# RESPONSE
# {
#   "_all_messages": [
#     {
#       "parts": [
#         {
#           "content": "Hello",
#           "timestamp": "2025-02-04T21:45:53.646148+00:00",
#           "part_kind": "user-prompt"
#         }
#       ],
#       "kind": "request"
#     },
#     {
#       "parts": [
#         {
#           "content": "Hello! How can I assist you today?",
#           "part_kind": "text"
#         }
#       ],
#       "model_name": "llama3.2:1b",
#       "timestamp": "2025-02-04T21:45:59+00:00",
#       "kind": "response"
#     }
#   ],
#   "_new_message_index": 0,
#   "data": "Hello! How can I assist you today?",
#   "_result_tool_name": null,
#   "_usage": {
#     "requests": 1,
#     "request_tokens": 26,
#     "response_tokens": 10,
#     "total_tokens": 36,
#     "details": null
#   }
# }
