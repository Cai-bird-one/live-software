from .llm.llm_client import LLMClient
from .utils.config import Config
from .llm.llm_basics import LLMMessage, LLMResponse

config = Config("config.json")
print(config)
llm_client: LLMClient = LLMClient(
            config.default_provider, config.model_providers[config.default_provider]
        )
message = LLMMessage(role="user", content="test")
response = llm_client.chat(messages = [message], model_parameters=config.model_providers[config.default_provider])
print(response)