from ..utils.config import Config
from ..llm.llm_client import LLMClient
from ..llm.llm_basics import LLMMessage, LLMResponse
from ..utils.templates import modify_code_template
from ..utils.running import run_local_code_in_docker
import json
config = Config()


class LiveSoftware:
    design: str
    code: str
    def __init__(self, config):
        self.client = LLMClient(config.default_provider, config.model_providers[config.default_provider])
        self.design = ""
        self.code = ""
        # clear /home/birdcly/live software/codes/main.py
        with open("/home/birdcly/live software/codes/main.py", "w") as f:
            f.write("")
    def get_code(self):
        with open("/home/birdcly/live software/codes/main.py", "r") as f:
            self.code = f.read()
        return self.code
    def set_code(self, code: str):
        self.code = code
        with open("/home/birdcly/live software/codes/main.py", "w") as f:
            f.write(code)
    def get_design(self):
        return self.design
    def set_design(self, design: str):
        self.design = design
    def modify_code(self, message: str):
        response = self.client.chat([LLMMessage(role="user", content=modify_code_template(self.design, self.code, message))],model_parameters=config.model_providers[config.default_provider])
        # print(response)
        response = json.loads(response.content)
        self.set_design(response["design"])
        self.set_code(response["code"])
        return response["code"]


if __name__ == "__main__":
    live_software = LiveSoftware(config)
    live_software.modify_code("you need to create a calculator that can add one and two")
    print("results= ", run_local_code_in_docker("/home/birdcly/live software/codes", "main.py"))


    print("done")

