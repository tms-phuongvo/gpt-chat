import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from src.service.llm.base import BaseService


class OpenAIService(BaseService):
    def __init__(self, **configuration: dict):
        super().__init__()
        self.llm = ChatOpenAI(
            **configuration,
        )

    def chatCompletion(
        self,
        message: list[BaseMessage],
        llm_tools: list = None,
        tool_choices=None,
        strict: bool = None,
    ) -> BaseMessage:
        try:
            logging.info("START CALL API")
            client = self.llm
            if llm_tools:
                client = self.llm.bind_tools(tools=llm_tools)
            response = client.invoke(input=message)
            logging.info("DATA: %s", response)
            return response
        except Exception as e:
            raise e
        finally:
            logging.info("END CALL API")
