from ..utils.config import Config
from ..llm.llm_client import LLMClient
from ..llm.llm_basics import LLMMessage, LLMResponse
from ..utils.prompts import add_method_prompt, request_prompt, make_test_prompt
from ..utils.state_manager import StateManager
import json
import random

config = Config()

class LiveSoftware:
    design: str
    code: str
    def __init__(self, config):
        self.request_client = LLMClient(config.default_provider, config.model_providers[config.default_provider])
        initial_messages = []
        initial_messages.append(LLMMessage(role="system", content=request_prompt))
        self.request_client.set_chat_history(initial_messages)
        self.state_manager = StateManager()
    def add_method(self, description):
        client = LLMClient(config.default_provider, config.model_providers[config.default_provider])
        initial_messages = []
        initial_messages.append(LLMMessage(role="system", content=add_method_prompt + f"Description: {description}"))
        client.set_chat_history(initial_messages)
        initial_test_messages = []
        initial_test_messages.append(LLMMessage(role="system", content=make_test_prompt  + f"Description: {description}"))

        message = LLMMessage(role="user", content=f"Code structure: {self.state_manager.get_structure_str()}")
        for _ in range(50):
            response = client.chat([message], model_parameters=config.model_providers[config.default_provider])
            alpha = 3
            beta = 3
            try:
                content = json.loads(response.content)
            except json.JSONDecodeError:
                return False
            if "operation" not in content:
                return False
            if content["operation"] == "query":
                if content["file_path"] is None:
                    return False
                code = self.state_manager.read_code(content["file_path"])
                message = LLMMessage(role="user", content=f"Code: {code}")
            elif content["operation"] == "install":
                if content["package_name"] is None:
                    message = LLMMessage(role="user", content=f"Error: Invalid package name.")
                else:
                    result = self.state_manager.install_package(content["package_name"])
                    message = LLMMessage(role="user", content=f"Install result: {result}")
            elif content["operation"] == "modify":
                if content["file_path"] is None or content["code"] is None or content["description"] is None:
                    return False
                codes = []
                test = []
                codes.append(content["code"])
                for i in range(alpha - 1):
                    tmp_code_client = LLMClient(config.default_provider, config.model_providers[config.default_provider])
                    tmp_code_client.set_chat_history(initial_messages)
                    num = random.randint(0, 65536)
                    message = LLMMessage(role="user", content=f"Code structure: {self.state_manager.get_structure_str()} \n"                 
                                        + f"Random_token:{num}\n")
                    response = tmp_code_client.chat([message], model_parameters=config.model_providers[config.default_provider])
                    try:
                        content_i = json.loads(response.content)
                    except json.JSONDecodeError:
                        continue
                    if "code" in content_i:
                        codes.append(content_i["code"])
                    else:
                        print("Warning: Response from LLM does not contain 'code' key. Skipping this response.")
                        continue
                for i in range(beta - 1):
                    tmp_test_client = LLMClient(config.default_provider, config.model_providers[config.default_provider])
                    tmp_test_client.set_chat_history(initial_test_messages)
                    num = random.randint(0, 65536)
                    message = LLMMessage(role="user", content=f"Code structure: {self.state_manager.get_structure_str()} \n"
                                        + f"Modify_file_path:{content['file_path']} \n"
                                        + f"Random_token:{num}\n")
                    response = tmp_test_client.chat([message], model_parameters=config.model_providers[config.default_provider])
                    try:
                        content_i = json.loads(response.content)
                    except json.JSONDecodeError:
                        continue
                    if "code" in content_i:
                        test.append(content_i["code"])
                    else:
                        print("Warning: Response from LLM does not contain 'code' key. Skipping this response.")
                        continue

                final_select_code = self.state_manager.select_code(codes, test, content["file_path"])
                success = self.state_manager.update_code(
                    content["file_path"],
                    final_select_code,
                    content.get("classes", []),
                    content.get("functions", []),
                    content.get("dependencies", []),
                    content["description"]
                )
                if not success:
                    return False
                message = LLMMessage(role="user", content=f"Code updated successfully: {content['file_path']}, now the new structure is: {self.state_manager.get_structure_str()}")
            elif content["operation"] == "stop":
                break
        return True

    def run_code(self, entry_file, args):
        return self.state_manager.run_code(entry_file, args)
    def request(self, requirement):
        full_response = {
            "thought": "Starting request processing...",
            "result": None,
            "stop_message": None
        }
        message = LLMMessage(role="user", content=f"User Requirement: {requirement}")
        for _ in range(50):
            response = self.request_client.chat([message], model_parameters=config.model_providers[config.default_provider])
            print(response.content)
            try:
                content = json.loads(response.content)
            except json.JSONDecodeError:
                print(111)
                return {"thought": "Error: Invalid response format.", "stop_message": "Invalid response format."}
            if "operation" not in content:
                print(222)
                return {"thought": "Error: Invalid response format.", "stop_message": "Invalid response format."}
            # 检查LLM的计划并执行
            # print(content["operation"])
            if content["operation"] == "add":
                description = content.get("description", "")
                if not self.add_method(description):
                    message = LLMMessage(role="user", content=f"Error: Failed to add method for requirement. Now the new structure is: {self.state_manager.get_structure_str()}")
                else:
                    message = LLMMessage(role="user", content=f"Method added successfully. Now the new structure is: {self.state_manager.get_structure_str()}")
            elif content["operation"] == "run":
                entry_file = content["entry_file"]
                args = content["args"]
                result = self.run_code(entry_file, args)
                message = LLMMessage(role="user", content=f"Return code: {result.returncode}, stdout: {result.stdout}, stderr: {result.stderr}")
            elif content["operation"] == "answer":
                full_response["result"] = content["result"]
                full_response["stop_message"] = "User answered."
                return full_response
            else:
                full_response["thought"] += f"\nError: {response}"
                full_response["stop_message"] = "Unexcepted stop."
                return full_response
        full_response["stop_message"] = "Exceeded maximum steps."
        return full_response

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
            print("structure:", live_software.get_structure())

