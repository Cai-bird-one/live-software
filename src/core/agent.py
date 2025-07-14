from ..utils.config import Config
from ..llm.llm_client import LLMClient
from ..llm.llm_basics import LLMMessage, LLMResponse

config = Config()


class LiveSoftware:
    design: str
    code: str
    def __init__(self, config):
        self.client = LLMClient(config)
        self.code = ""
    def add_method(self, method: str):
        pass
