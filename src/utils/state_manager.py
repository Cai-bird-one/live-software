import json
import os
import shutil
import subprocess
class StateManager:
    def __init__(self):
        self.dir="D:/Live_software/live_software/codes"
        # 清空 self.dir
        shutil.rmtree(self.dir)
        os.mkdir(self.dir)
        self.design=""
        self.usage=""

    def load_code(self):
        codes={}
        for file in os.listdir(self.dir):
            if file.endswith(".py"):
                try:
                    with open(os.path.join(self.dir, file), 'r', encoding='utf-8') as f:
                        codes[file]=f.read()
                except UnicodeDecodeError:
                    codes[file] = f"# Error reading file {file}: {e}"      
        return codes
    
    def save_code(self, codes):
        for file, code in codes.items():
            with open(os.path.join(self.dir,file), "w", encoding='utf-8') as f:
                f.write(code)
    
    def load_design(self):
        return self.design
    
    def save_design(self, design):
        self.design = design

    def load_usage(self):
        return self.usage

    def save_usage(self, usage):
        self.usage = usage

    def run_code(self, entry_file, args):
        if args is str:
            args = args.split(" ")
        cmd = ["python", os.path.join(self.dir, entry_file)] + args
        # print(cmd)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            # print(result)
            return result
        except subprocess.CalledProcessError as e:
            return e.output
    
    def state_str(self):
        state = {
            "design": self.design,
            "code": self.load_code(),
            "usage": self.usage
        }
        return json.dumps(state)
    
    def update(self, response):
        self.save_design(response["design"])
        self.save_code(response["code"])
        self.save_usage(response["usage"])

    def get_structure(self):
        design = self.load_design()
        if("__structure__" not in design):
            return {}
        else:
            structure = design["__structure__"]
            return structure