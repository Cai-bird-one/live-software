
class Node:
    """
    A node in the DAG
    """
    subclasses: list
    members: list
    className: str
    classPath: str

    def __init__(self, path):
        self.path = path
    
    def get_codes():
        """
        Returns the code of the class
        """
        pass
    
    def modify_code(self, codes:str):
        """
        Changes the code of the class
        """
        pass
    
    
    def add_method(self, requirement:str):
        """
        Adds a method to the class
        """
        pass

    def add_subclass(self, requirement:str):
        """
        Adds a subclass of this class
        """
        pass

    def add_member(self, requirement:str):
        """
        Adds a member of this class
        """
    
    def generate_code_information(self):
        codes = {}
        codes["own"][self.className] = self.get_codes()
        for subclass in self.subclasses:
           codes["subclasses"][subclass.className] = subclass.get_codes()
        for member in self.members:
           codes["members"][member.className] = subclass.get_codes()
        return codes