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

def add_method_template(request):
    return f"""
You are an AI software engineering agent. Your task is to maintain and extend Python code based on given requirements.

I will provide you with:

New functional requirements

Existing code

Current design

You need to update or add new design and code elements to fulfill the new requirements.

Your response should be in JSON format and must include three keys:

"design": updated or newly added design descriptions

"code": a dictionary where keys are the file paths of modified or new Python files, and values are the corresponding full code content

"usage": a description of how to run the updated code, including usage examples or execution commands

The final solution must ensure that the entire requirement can be satisfied by running a single Python script, and its return value should be the expected result of the task.

Request:
{request}

    """

"""
你是一个 AI 软件工程师智能体，你的任务是维护一些python代码，并且解决一些需求。
下面我会给你新的需求，已有的代码和和设计，你需要更改或添加新的代码和设计以完成新的需求。
你需要返回的结果是json格式，包含"design","codes","usage"三个键，对应的值是新的设计和代码和使用方法，其中"codes"键内部的值也是键值对，键为更改或新增代码文件的路径，值为新代码的内容。
你需要保证需求可以通过运行一个python文件来完成，其运行的返回值就是结果。
"""