import subprocess

# 执行命令并获取结果
def execute_command(command):
    print(f"Executing command: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("Command executed successfully:")
            print(result.stdout)
            return result.stdout, None
        else:
            print(f"Error executing command: {result.stderr}")
            return None, result.stderr
    except Exception as e:
        print(f"Execution failed: {e}")
        return None, str(e)
