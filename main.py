from ai_thinker import large_language_model, extract_think_code_command
from command_executor import execute_command
import time

# 思考并生成命令
def thinking_step(user_input, conversation_history):
    print("Thinking... Please wait while I analyze your request.")
    response = large_language_model(
        f"Provide only a valid Windows command enclosed in '<think></think>', '<code></code>', and '<command></command>' tags. "
        f"Do NOT add explanations. Ensure the command works on Windows. "
        f"Task: {user_input}",
        conversation_history
    )
    
    # 提取思考、代码和命令部分
    think, code, command = extract_think_code_command(response)
    
    # 如果没有命令，重新进行思考
    if not command or command == "指令":
        print("Failed to extract a valid command from AI response. Retrying...")
        return None, None, None

    # 输出思考内容
    if think:
        print(f"<think>{think}</think>")
    
    # 输出代码内容
    if code:
        print(f"<code>{code}</code>")
    
    # 输出命令部分
    if command:
        print(f"<command>{command}</command>")
    
    return think, code, command

# 主循环
def main():
    conversation_history = []
    while True:
        user_input = input("Describe what you need to do (or type 'exit' to quit): ").strip()
        
        # 如果用户输入 'exit'，则退出程序
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break

        # 思考并生成命令
        think, code, command = thinking_step(user_input, conversation_history)
        
        # 如果思考失败，重新进行
        if command is None:
            continue

        # 执行命令
        confirm = input(f"Do you want to execute this command: {command} (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Execution canceled by user.")
            continue
        
        output, error = execute_command(command)

        # 若执行失败，将错误信息传回 AI，请求修正
        if error:
            user_input = f"The command failed with error: {error}. Please suggest a corrected command."
        else:
            print("Task completed successfully.")

if __name__ == "__main__":
    main()
