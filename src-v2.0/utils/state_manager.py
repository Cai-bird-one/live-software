import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import re
import os, sys

def check_file(file_name):
    return file_name.endswith(".py")
class StateManager:
    def __init__(self):
        self.dir="./codes"
        self.structure_path="./structure.json"
        # 清空 self.dir
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)
        os.mkdir(self.dir)
        self.structure= {"type":"dir", "children": {}}
        os.makedirs(os.path.dirname(self.structure_path), exist_ok=True)
        self.save_structure()
        # self.structure= json.load(open(self.structure_path, "r", encoding="utf-8"))

    def save_structure(self):
        with open(self.structure_path, "w", encoding="utf-8") as f:
            json.dump(self.structure, f, indent=4)
    
    def load_structure(self):
        if not os.path.exists(self.structure_path):
            return
        with open(self.structure_path, "r", encoding="utf-8") as f:
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
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        self.save_structure()
        return True

    def read_code(self, file_path):
        path = os.path.join(self.dir, file_path)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
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
    
    @staticmethod
    def _extract_numbers(text: str) -> list[float]:
        return [float(m) for m in re.findall(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?', text or '')]
    
    @staticmethod
    def _get_file_structure_fingerprint(root_dir: Path, script_name: str) -> str:
        excluded_names = {'.git', 'src', '.gitignore', 'structure.json', 'codes', script_name}       
        paths = []
        for path in root_dir.rglob('*'):
            relative_parts = path.relative_to(root_dir).parts
            if any(part in excluded_names for part in relative_parts):
                continue
            paths.append(str(path.relative_to(root_dir)).replace("\\", "/"))
        paths.sort()
        return "\n".join(paths)
    
    def select_code(
        self,
        codes: list[str],
        tests: list[str],
        file_path: str
    ) -> str:
        if not tests:
            return codes[0]
        tmp_root = Path(tempfile.mkdtemp(prefix="mbr_"))
        fingerprints = []
        tingerprints = []
        fs_fingerprints = []
        error = [0] * len(codes)
        for code_idx, code in enumerate(codes):
            tmp_file = tmp_root / f"cand_{code_idx}.py"
            tmp_file.write_text(code, encoding="utf-8")
            fp = []
            tp = []
            fs_fp = []
            for test_cli in tests:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_path = Path(tmp_dir)
                    script_file_name = "test_script.py"
                    tmp_file = tmp_path / script_file_name
                    tmp_file.write_text(code, encoding="utf-8")
                    cmd = [sys.executable, str(tmp_file)] + test_cli.strip().split()
                    try:
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True,
                            timeout=10,
                            cwd=tmp_path
                        )
                        out = result.stdout.strip()
                        err = result.stderr.strip()
                        if result.returncode != 0:
                            out = f"__ERROR__:{err}".replace(script_file_name, "script.py")
                            error[code_idx] += 1
                    except Exception:
                        out = "__TIMEOUT__"
                        error[code_idx] += 1
                tp.append(StateManager._extract_numbers(out))
                fp.append(out)
                fs_fingerprint = StateManager._get_file_structure_fingerprint(
                        tmp_path, 
                        script_file_name
                    )
                fs_fp.append(fs_fingerprint)
            fingerprints.append(fp)
            tingerprints.append(tp)
            fs_fingerprints.append(fs_fp)

        n = len(codes)
        risk = [0] * n
        risk2 = [0] * n
        risk3 = [0] * n
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                diff = sum(1 for a, b in zip(fingerprints[i], fingerprints[j]) if a != b)
                diff2 = sum(1 for a, b in zip(tingerprints[i], tingerprints[j]) if a != b)
                diff3 = sum(1 for a, b in zip(fs_fingerprints[i], fs_fingerprints[j]) if a != b)
                risk[i] += diff
                risk2[i] += diff2
                risk3[i] += diff3
        for i in range(n):
            print(f"  Risk: {risk[i]}")
            print(f"  Risk2: {risk2[i]}")
            print(f"  Risk3: {risk3[i]}")
        best_idx = min(range(n), key=lambda i: (risk[i], risk2[i], risk3[i], error[i], i))
        shutil.rmtree(tmp_root)
        return codes[best_idx]
        # unittest-Version
        # tmp_root = Path(self.dir).parent / "tmp_select"
        # tmp_root.mkdir(exist_ok=True)
        # tmp_workspace = Path(tempfile.mkdtemp(dir=tmp_root))

        # for p in Path(self.dir).rglob("*"):
        #     rel = p.relative_to(self.dir)
        #     target = tmp_workspace / rel
        #     if rel == Path(file_path):
        #         continue
        #     if p.is_dir():
        #         target.mkdir(parents=True, exist_ok=True)
        #     else:
        #         try:
        #             target.symlink_to(p.resolve())
        #         except OSError:
        #             shutil.copy2(p, target)

        # best_code, best_score = None, -1
        # for c_idx, code in enumerate(codes):
        #     code_file = tmp_workspace / file_path
        #     code_file.parent.mkdir(parents=True, exist_ok=True)
        #     code_file.write_text(code, encoding="utf-8")
        #     total = 0
        #     passed = 0
        #     for t_idx, test_code in enumerate(tests):
        #         tests_dir = tmp_workspace / "tests"
        #         if tests_dir.exists():
        #             shutil.rmtree(tests_dir)
        #         tests_dir.mkdir(parents=True, exist_ok=True)

        #         try:
        #             test_map = json.loads(test_code)
        #         except json.JSONDecodeError:
        #             test_map = {f"test_{Path(file_path).stem}.py": test_code}

        #         for fname, content in test_map.items():
        #             (tests_dir / fname).write_text(content, encoding="utf-8")

        #         xml_out = tmp_workspace / f"result_{c_idx}_{t_idx}.xml"
        #         cmd = [
        #             sys.executable, "-m", "unittest", "discover",
        #             "-s", str(tests_dir),
        #             "-p", "test_*.py",
        #             "-v",
        #             "--buffer"
        #         ]
                
        #         proc = subprocess.run(
        #             cmd,
        #             cwd=str(tmp_workspace),
        #             stdout=subprocess.PIPE,
        #             stderr=subprocess.STDOUT,
        #             text=True
        #         )

        #         success = proc.returncode == 0
        #         passed += success
        #         total += 1
        #     print(f"Test Generator: {c_idx}")
        #     print(passed)
        #     print(total)
        #     score = passed / total
        #     if score > best_score:
        #         best_score = score
        #         best_code = code

        # # shutil.rmtree(tmp_workspace)
        # if best_code is None:
        #     return codes[0]
        # return best_code

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
    