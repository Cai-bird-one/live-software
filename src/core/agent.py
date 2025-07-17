from ..utils.config import Config
from ..llm.llm_client import LLMClient
from ..llm.llm_basics import LLMMessage, LLMResponse
from ..utils.templates import add_method_template
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
        codes = self.state_manager.load_code()
        design = self.state_manager.load_design()
        message = LLMMessage(role="user", content=add_method_template(request), design=design, codes=codes)
        response = self.client.chat([LLMMessage(role="user", content=message.parse_to_str())],model_parameters=config.model_providers[config.default_provider])
        # print(response)
        response = json.loads(response.content)
        self.state_manager.save_design(response["design"])
        self.state_manager.save_code(response["code"])
        return response
    def run_code(self, entry_file, args):
        try:
            # result = run_local_code_in_docker("/home/birdcly/live software/codes", entry_file, args)
            run_cmd = ["python", f"/home/birdcly/live software/codes/{entry_file}", *args.split(" ")]
            result = subprocess.run(run_cmd, capture_output=True, timeout=60)
            return result
        except Exception as e:
            return e
if __name__ == "__main__":
    live_software = LiveSoftware(config)
    while(True):
        str = input()
        if str == "exit":
            break
        elif str == "add method":
            describetion = input("describetion:")
            print(live_software.add_method(describetion))
        elif str == "run code":
            entry_file = input("entry_file:")
            args = input("args:")
            print("results= ", live_software.run_code(entry_file, args))

