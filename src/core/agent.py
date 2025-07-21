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
        response = self.client.chat([message],model_parameters=config.model_providers[config.default_provider])
        response = json.loads(response.content)
        self.state_manager.update(response)
        return response
    def run_code(self, entry_file, args):
        return self.state_manager.run_code(entry_file, args)
    def request(self, request):
        full_response = {
            "thought": "Starting request processing...",
            "result": None,
            "stop_message": None
        }
        for _ in range(10):
            message = LLMMessage(role="user", content=request_template(request, self.state_manager.state_str()))
            response = self.client.chat([message],model_parameters=config.model_providers[config.default_provider])
            response = json.loads(response.content)

            # 检查LLM的计划并执行
            if "method" in response:
                method_request = response["method"]
                add_method_response = self.add_method(method_request)
                current_thought = add_method_response.get("thought", "No thought from add_method.")
                full_response["thought"] += f"\n\n {json.dumps(current_thought)}"
                continue
            elif "run" in response:
                entry_file = response["run"]["entry_file"]
                args = response["run"]["args"]
                results = self.run_code(entry_file, args)
                results = self.get_answer(request, response, results)
                print(results)
                try:
                    result = json.loads(results)
                    full_response["result"] = result.get("result", result.get("stop", results))
                    # final_thought = result.get('thought', 'No final thought.')
                    # full_response["thought"] += f"\n\nThought for final answer: {json.dumps(final_thought)}"
                except (json.JSONDecodeError, TypeError):
                    full_response["result"] = results
                return full_response
            elif "stop" in response:
                full_response["stop_message"] = response["stop"]
                return full_response
            else:
                full_response["thought"] += f"\nError: {response}"
                full_response["stop_message"] = "Unexcepted stop."
                return full_response
        full_response["stop_message"] = "Exceeded maximum steps."
        return full_response
    def get_answer(self, request, response, result):
        # print("!!!result!!!", result)
        message = LLMMessage(role="user", content=get_answer_template(request, self.state_manager.state_str(),
        json.dumps(response["run"]), json.dumps({
            "stdout": result.stdout,
            "stderr": result.stderr
        })))
        response = self.client.chat([message],model_parameters=config.model_providers[config.default_provider])
        # print(response)
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
            print(response)
            print(live_software.get_structure())

