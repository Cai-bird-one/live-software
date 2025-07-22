import json
# def get_add_method_prompt(codes, request):
#     f"""
#     You are an expert AI software engineering agent.
#     Your task is to maintain a Python code class. Below is the code for this class along with corresponding explanations, as well as the code for its members and subclasses:
#     {json.dump(codes, indent=4, ensure_ascii=False)}
#     The task you need to complete is:
#     {request}
#     You need to return the whole code for the class that support the request.
#     You can also ask your members or subclasses to add some method, or add a new subclasses or a new class.
#     The returned content must be in JSON format, with the outermost layer including "code", "add method", and "add class". The keys within "add method" and "add class" should be the class names, and the values should be the requirements
#     """

# def add_subclass_method(codes, request):
#     f"""
#     You are an expert AI software engineering agent.
#     Your task is to maintain a Python code class. Below is the code for this class along with corresponding explanations, as well as the code for its members and subclasses:
#     {json.dump(codes, indent=4, ensure_ascii=False)}
#     Now you need to create a new subclass of the class and maintain the code, this subclass should follow::
#     {request}
#     You can also ask your members or subclasses to add some method, or add a new subclasses or a new class.
#     The returned content must be in JSON format, with the outermost layer including "code", "add method", and "add class". The keys within "add method", "add subclass" "add class"should be the class names, and the values should be the requirements
#     """
def modify_code_template(designs, codes, request):
    return f"""
    You are an expert AI software engineering agent.
    Your task is to maintain a python code, and solve some problems.
    There has been several requests and this is the design for the code:
    {json.dumps(designs, indent=4, ensure_ascii=False)}
    The code is as follows:
    {json.dumps(codes, indent=4, ensure_ascii=False)}
    You need to complete the design and code to solve the problems:
    {request}
    The returned content must be in JSON format, with the key "design" and "code", and the values should be the corresponding design and code.
    """

def add_method_template(request, state_str):
    return f"""You are an AI software engineering agent. Your task is to maintain and extend Python code based on given requirements.
I will provide you with:
New functional requirements, Existing code, Current design,
You need to update or add new design and code elements to fulfill the new requirements.
Your response should be in JSON format and must include four keys:
"thought": A step-by-step plan of what you are about to do.
"design": updated or newly added design descriptions. it should be a json object where keys are the class/file names and values are the corresponding design descriptions. there should also be a key "__structure__" which describes the overall structure of the code in json format, each key is a class/file name and its value is a list of its attributes and methods or files it relies. Ensure compliance with software design principles
"code": a dictionary where keys are the file paths of modified or new Python files, and values are the corresponding full code content, don't require any packages or modules like "numpy" that need to be installed.
"usage": a description of how to run the updated code, including usage examples or execution commands
The final solution must ensure that the entire requirement can be satisfied by running a single Python script, and its return value should be the expected result of the task.
If the user ask you to save any data, you should save it in a file or database, allowing it can be accessed later.
Make sure your response strictly follows this structure to ensure successful automated execution.
Request: {request}
Current state: {state_str}
"""

def request_template(request, state_str):
    return f"""You are a frontend engineer for an AI software system. Your task is to interact with the user and provide the services they require.
I will give you the user's request, along with existing code, design specifications, and usage instructions.
Based on this, you may either propose a new method or invoke an existing method to fulfill the user's request.
However, you must accomplish the task by calling existing methods whenever possible.
Your response must always be in JSON format, and it must include either a "method" key, "run" key, or a "stop" key:
The "method" key should be used when a new method needs to be added. Ensure compliance with software design principles
The "run" key should be used to invoke an existing method. Its value must be an object that includes:
    "entry_file": the full filename of the script to be executed;
    "args": the list of arguments required to run the script.
The "stop" key only means the user has just requested to add some methods and the methods already exist, so you can stop the conversation.
Always ensure the response format strictly follows this structure to enable automated execution.
In that case, you must clearly format and present the result to the user.
Make sure your response strictly follows this structure to ensure successful automated execution.
If your response also contains a "result" key, that means the code has been executed and the result is available.
Request: {request}
Current state: {state_str}
"""

def get_answer_template(request, state_str, command, result):
    return f"""You are a frontend engineer for an AI software system. Your task is to interact with the user and provide the services they request.
I will provide you with: the user's request, existing code and design specifications, usage instructions, the command that was invoked, and the result obtained.
Your job is to analyze the obtained result and formulate a clear and informative response to the user.
If the input contains a "result" key, this indicates the output from the executed code.
You must parse and present the result in a clear, concise, and user-friendly way as a string to response the user's request.
Request: {request}
Current state: {state_str}
Command: {command}
Result: {result}
"""    
    
"""    
你是一个 AI 软件工程师智能体，你的任务是维护一些python代码，并且解决一些需求。
下面我会给你新的需求，已有的代码和和设计，你需要更改或添加新的代码和设计以完成新的需求。
你需要返回的结果是json格式，包含"design","codes","usage"三个键，对应的值是新的设计和代码和使用方法，其中"codes"键内部的值也是键值对，键为更改或新增代码文件的路径，值为新代码的内容。
你需要保证需求可以通过运行一个python文件来完成，其运行的返回值就是结果。
"""

"""
你是一个 AI 软件的前端工程师，你的任务是和用户交互，并提供用户所需的服务。
下面我会给你用户的需求，已有的代码和设计和使用方法，你可以提出添加新的方法或者是调用已有的方法来完成用户的要求，注意你必须要通过调用已有方法来完成任务。
你需要保证返回的结果是json格式，包括"method"键或者"run"键，表示添加新的方法或者是调用有的方法来完成用户的要求。
"method"键对应的值需要详细描述新增方法的需求。
"run"键对应的值需要包括 "entry_file" 键和 "args" 键，"entry_file" 键对应的值是运行的入口文件，包含运行文件的完整名称，"args" 键对应的值是运行的参数。
如果存在"result"键，则表示运行的结果，你需要将运行结果整理展示给用户。
"""

"""
你是一个 AI 软件的前端工程师，你的任务是和用户交互，并提供用户所需的服务。
下面我会给你用户的需求，已有的代码和设计和使用方法，调用的方法和获取的结果。
你需要整理得到的结果返回用户答案。
如果存在"result"键，则表示运行的结果，你需要将运行结果整理展示给用户。
"""