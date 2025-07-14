import json
def get_add_method_prompt(codes, request):
    f"""
    You are an expert AI software engineering agent.
    Your task is to maintain a Python code class. Below is the code for this class along with corresponding explanations, as well as the code for its members and subclasses:
    {json.dump(codes, indent=4, ensure_ascii=False)}
    The task you need to complete is:
    {request}:
    You need to return the whole code for the class that support the request.
    You can also ask your members or subclasses to add some method, or add a new subclasses or a new class.
    The returned content must be in JSON format, with the outermost layer including "code", "add method", and "add class". The keys within "add method" and "add class" should be the class names, and the values should be the requirements
    """