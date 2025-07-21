from ..utils.config import Config
from ..llm.llm_client import LLMClient
from ..llm.llm_basics import LLMMessage, LLMResponse
from ..utils.templates import add_method_template, request_template, get_answer_template
from ..utils.running import run_local_code_in_docker
from ..utils.state_manager import StateManager
import json
import subprocess

config = Config()

class LiveSoftware:
    design: str
    code: str
    def __init__(self, config):
        self.client = LLMClient(config.default_provider, config.model_providers[config.default_provider])
        self.state_manager = StateManager()
    def add_method(self, request):
        message = LLMMessage(role="user", content=add_method_template(request, self.state_manager.state_str()))
        print(message)
        response = self.client.chat([message],model_parameters=config.model_providers[config.default_provider])
        print(response)
        response = json.loads(response.content)
        self.state_manager.update(response)
        return response
    def run_code(self, entry_file, args):
        return self.state_manager.run_code(entry_file, args)
    def request(self, request):
        message = LLMMessage(role="user", content=request_template(request, self.state_manager.state_str()))
        print(message)
        response = self.client.chat([message],model_parameters=config.model_providers[config.default_provider])
        print(response)
        response = json.loads(response.content)
        if "method" in response:
            self.add_method(response["method"])
            return self.request(request)
        elif "run" in response:
            entry_file = response["run"]["entry_file"]
            args = response["run"]["args"]
            results = self.run_code(entry_file, args)
            results = self.get_answer(request, response, results)
            return results
        elif "stop" in response:
            return response["stop"]
    def get_answer(self, request, response, result):
        print("!!!result!!!", result)
        message = LLMMessage(role="user", content=get_answer_template(request, self.state_manager.state_str(),
        json.dumps(response["run"]), json.dumps({
        "stdout": result.stdout,
        "stderr": result.stderr
})))
        print(message)
        response = self.client.chat([message],model_parameters=config.model_providers[config.default_provider])
        print(response)
        return response.content
    
    def get_structure(self):
        return self.state_manager.get_structure()
if __name__ == "__main__":
    live_software = LiveSoftware(config)
    while(True):
        str = input()
        if str == "exit":
            break
        else:
            response = live_software.request(str)
            print("response:", response)
            print(live_software.get_structure())

