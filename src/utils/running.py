import subprocess
import os
import uuid

def run_local_code_in_docker(code_dir: str, entry_file: str = "main.py", args = None, timeout: int = 60):
    """
    将本地目录挂载到 Docker 容器中，执行指定入口文件。
    
    :param code_dir: 本地代码目录路径（绝对路径最佳）
    :param entry_file: 在容器中要执行的文件名
    :param timeout: 超时时间（秒）
    :return: dict 包含 returncode, stdout, stderr
    """
    if not os.path.isdir(code_dir):
        raise ValueError(f"代码目录不存在: {code_dir}")
    
    entry_path = os.path.join(code_dir, entry_file)
    if not os.path.isfile(entry_path):
        raise ValueError(f"入口文件不存在: {entry_path}")

    container_name = f"sandbox_{uuid.uuid4().hex[:8]}"

    args_list = args.split() if args else []
    # print(args_list)

    docker_cmd = [
    "docker", "run", "--rm",
    "--name", container_name,
    "--network", "none",
    "--cpus=0.5",
    "--memory=128m",
    "-v", f"{os.path.abspath(code_dir)}:/app:ro",
    "python:3.11",
    "timeout", str(timeout),
    "python", f"/app/{entry_file}",
    ] + args_list

    # print(" ".join(docker_cmd))
    try:
        result = subprocess.run(
            docker_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout + 2  # 预留额外时间
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout} seconds."
        }