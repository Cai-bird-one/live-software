import json
import os
import shutil
import subprocess

def check_file(file_name):
    return file_name.endswith(".py")
class StateManager:
    def __init__(self):
        self.dir="/home/birdcly/live-software/codes"
        self.structure_path="home/birdcly/live-software/structure.json"
        # 清空 self.dir
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)
        os.mkdir(self.dir)
        self.structure= {"type":"dir", "children": {}}
        self.save_structure()

    def save_structure(self):
        with open(self.structure_path, "w") as f:
            json.dump(self.structure, f, indent=4)
    
    def load_structure(self):
        if not os.path.exists(self.structure_path):
            return
        with open(self.structure_path, "r") as f:
            self.structure = json.load(f)

    def find_path(self, file_path):
        now = self.structure
        for name in str.split(file_path, "/"):
            if name == "":
                continue
            if "children" not in now:
                if now["type"] != "dir":
                    return None
                now["children"] = {}
            if name not in now["children"]:
                now["children"][name] = {}
            now = now["children"][name]
            if check_file(name):
                now["type"] = "file"
                return now
            else:
                now["type"] = "dir"
        return None
    def update_code(self, file_path, code, classes, functions, dependencies, description):
        data = self.find_path(file_path)
        if data is None:
            return False
        data["classes"] = classes
        data["functions"] = functions
        data["dependencies"] = dependencies
        data["description"] = description
        path = os.path.join(self.dir, file_path)
        print("path: ", path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(code)
        self.save_structure()
        return True

    def read_code(self, file_path):
        path = os.path.join(self.dir, file_path)
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return f.read()
    
    def install_package(self, package_name):
        cmd = ["pip", "install", package_name]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return f"Error installing package {package_name}: {result.stderr}"
            return f"Package {package_name} installed successfully."
        except subprocess.CalledProcessError as e:
            return f"Error installing package {package_name}: {e.output}"

    def run_code(self, entry_file, args):
        if args is str:
            args = args.split(" ")
        str_args = []
        for value in args:
            str_args.append(str(value))
        cmd = ["python", os.path.join(self.dir, entry_file)] + str_args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result
        except subprocess.CalledProcessError as e:
            return e.output
    
    def get_structure(self):
        return self.structure
    
    def get_structure_str(self):
        return json.dumps(self.get_structure())
    