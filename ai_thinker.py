import json
import time
from openai import OpenAI

# 调用 AI 生成指令
def large_language_model(content, conversation_history, retries=3):
    conversation_history.append({'role': 'user', 'content': content})
    client = OpenAI(
        api_key="YOUR_API_KEY",
        base_url="https://open.bigmodel.cn/api/paas/v4/",
    )
    for attempt in range(retries):
        try:
            completion = client.chat.completions.create(
                model="GLM-4-Flash",
                messages=conversation_history
            )
            data = json.loads(completion.model_dump_json())
            result = data['choices'][0]['message']['content']
            conversation_history.append({'role': 'assistant', 'content': result})
            return result
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise

# 提取思考、代码和命令部分
def extract_think_code_command(response):
    think = ''
    code = ''
    command = ''
    
    # 查找并提取思考过程（<think>...<think>）
    if '<think>' in response and '</think>' in response:
        think_start = response.find('<think>') + len('<think>')
        think_end = response.find('</think>')
        think = response[think_start:think_end].strip()
    
    # 查找并提取代码（<code>...<code>）
    if '<code>' in response and '</code>' in response:
        code_start = response.find('<code>') + len('<code>')
        code_end = response.find('</code>')
        code = response[code_start:code_end].strip()
    
    # 查找并提取命令（<command>...<command>）
    if '<command>' in response and '</command>' in response:
        command_start = response.find('<command>') + len('<command>')
        command_end = response.find('</command>')
        command = response[command_start:command_end].strip()

    return think, code, command
