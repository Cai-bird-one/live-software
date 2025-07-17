import json
import os
import shutil

class StateManager:
    def __init__(self):
        self.dir="/home/birdcly/live software/codes"
        # 清空 self.dir
        shutil.rmtree(self.dir)
        os.mkdir(self.dir)
        self.design=""
        # 创建一个docker容器

    def load_code(self):
        # 查询一个目录下的所有python文件，用文件路径作为字典的key，用代码内容作为值
        codes={}
        for file in os.listdir(self.dir):
            if file.endswith(".py"):
                codes[file]=open(os.path.join(self.dir,file)).read()
        return codes
    
    def save_code(self, codes):
        for file, code in codes.items():
            with open(os.path.join(self.dir,file), "w") as f:
                f.write(code)
    
    def load_design(self):
        return self.design
    
    def save_design(self, design):
        self.design=design

    # def run_code(self, entry_file, args):
        