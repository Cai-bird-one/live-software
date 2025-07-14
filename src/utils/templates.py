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