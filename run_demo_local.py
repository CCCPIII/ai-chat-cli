#!/usr/bin/env python3
"""
本地运行Demo - 无需真实API密钥
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict
from enum import Enum

# 模拟Rich库的功能
class MockConsole:
    def print(self, text, **kwargs):
        # 移除颜色标记
        import re
        text = re.sub(r'\[.*?\]', '', text)
        print(text)
    
    def input(self, prompt):
        return input(prompt)

class MockPrompt:
    @staticmethod
    def ask(text, default=None):
        if default:
            return input(f"{text} ({default}): ") or default
        return input(f"{text}: ")
    
    @staticmethod
    def confirm(text, default=True):
        response = input(f"{text} (y/n): ").lower()
        if response == '':
            return default
        return response in ['y', 'yes']

class ModelType(Enum):
    """支持的模型类型"""
    OPENAI_GPT4 = "gpt-4"
    OPENAI_GPT35 = "gpt-3.5-turbo"
    CLAUDE_OPUS = "claude-3-opus-20240229"
    CLAUDE_SONNET = "claude-3-sonnet-20240229"
    DEEPSEEK_CHAT = "deepseek-chat"
    DEEPSEEK_CODER = "deepseek-coder"

@dataclass
class Message:
    """聊天消息"""
    role: str  # user, assistant, system
    content: str
    timestamp: str
    
    def to_dict(self) -> Dict:
        return asdict(self)

class MockAIChatClient:
    """模拟AI聊天客户端"""
    
    def __init__(self):
        self.history: List[Message] = []
        self.console = MockConsole()
        
    def add_message(self, role: str, content: str):
        """添加消息到历史"""
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat()
        )
        self.history.append(message)
        return message
    
    def chat_with_model(self, model_type: ModelType, prompt: str) -> str:
        """模拟AI响应"""
        self.add_message("user", prompt)
        
        # 根据模型类型返回不同的模拟响应
        responses = {
            ModelType.OPENAI_GPT4: "这是GPT-4的模拟响应：你好！我是一个AI助手。",
            ModelType.OPENAI_GPT35: "这是GPT-3.5的模拟响应：很高兴为你服务！",
            ModelType.CLAUDE_OPUS: "这是Claude 3 Opus的模拟响应：你好，我是Claude！",
            ModelType.CLAUDE_SONNET: "这是Claude 3 Sonnet的模拟响应：欢迎使用AI聊天工具！",
            ModelType.DEEPSEEK_CHAT: "这是DeepSeek Chat的模拟响应：你好，我是DeepSeek！",
            ModelType.DEEPSEEK_CODER: "这是DeepSeek Coder的模拟响应：我可以帮你写代码！"
        }
        
        response = responses.get(model_type, "这是AI的响应")
        self.add_message("assistant", response)
        return response
    
    def display_response(self, response: str, model_name: str):
        """显示响应"""
        print(f"\n{model_name} 回复:")
        print("-" * 40)
        print(response)
        print("-" * 40)
    
    def save_history(self, filename: str = "chat_history.json"):
        """保存聊天历史到文件"""
        history_data = [msg.to_dict() for msg in self.history]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
        
        print(f"聊天历史已保存到 {filename}")
    
    def load_history(self, filename: str = "chat_history.json"):
        """从文件加载聊天历史"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            self.history = [
                Message(**msg_data) for msg_data in history_data
            ]
            print(f"已加载 {len(self.history)} 条历史消息")
        except FileNotFoundError:
            print("未找到历史文件，开始新对话")
        except Exception as e:
            print(f"加载历史失败: {e}")

def show_welcome():
    """显示欢迎信息"""
    print("=" * 50)
    print("AI Chat CLI - 多模型命令行聊天工具 (模拟版)")
    print("支持 OpenAI GPT-4, Claude, DeepSeek 等头部模型")
    print("输入 'quit' 退出，'save' 保存历史，'load' 加载历史")
    print("=" * 50)

def select_model() -> ModelType:
    """选择模型"""
    print("\n请选择AI模型:")
    print("1. OpenAI GPT-4")
    print("2. OpenAI GPT-3.5 Turbo")
    print("3. Claude 3 Opus")
    print("4. Claude 3 Sonnet")
    print("5. DeepSeek Chat")
    print("6. DeepSeek Coder")
    
    while True:
        choice = input("选择模型 (1-6, 默认1): ").strip()
        if choice == '':
            choice = '1'
        
        model_map = {
            "1": ModelType.OPENAI_GPT4,
            "2": ModelType.OPENAI_GPT35,
            "3": ModelType.CLAUDE_OPUS,
            "4": ModelType.CLAUDE_SONNET,
            "5": ModelType.DEEPSEEK_CHAT,
            "6": ModelType.DEEPSEEK_CODER
        }
        
        if choice in model_map:
            return model_map[choice]
        else:
            print("无效选择，请重试")

def main():
    """主函数"""
    show_welcome()
    
    # 创建客户端
    client = MockAIChatClient()
    
    # 选择模型
    model_type = select_model()
    model_name = model_type.value
    
    print(f"\n已选择模型: {model_name}")
    print("开始聊天吧！输入 'quit' 退出\n")
    
    # 主聊天循环
    while True:
        try:
            # 获取用户输入
            user_input = input("你: ").strip()
            
            # 处理特殊命令
            if user_input.lower() == 'quit':
                if input("是否保存聊天历史? (y/n): ").lower() in ['y', 'yes']:
                    filename = input("保存文件名 (默认chat_history.json): ").strip()
                    if not filename:
                        filename = "chat_history.json"
                    client.save_history(filename)
                print("再见！")
                break
            
            elif user_input.lower() == 'save':
                filename = input("保存文件名 (默认chat_history.json): ").strip()
                if not filename:
                    filename = "chat_history.json"
                client.save_history(filename)
                continue
            
            elif user_input.lower() == 'load':
                filename = input("加载文件名 (默认chat_history.json): ").strip()
                if not filename:
                    filename = "chat_history.json"
                client.load_history(filename)
                continue
            
            elif user_input.lower() == 'model':
                model_type = select_model()
                model_name = model_type.value
                print(f"已切换到模型: {model_name}")
                continue
            
            elif user_input.lower() == 'history':
                print(f"\n聊天历史 ({len(client.history)} 条消息):")
                for i, msg in enumerate(client.history, 1):
                    print(f"{i}. [{msg.role}] {msg.content[:50]}...")
                continue
            
            # 调用AI
            print("思考中...")
            response = client.chat_with_model(model_type, user_input)
            
            # 显示响应
            client.display_response(response, model_name)
            
        except KeyboardInterrupt:
            print("\n检测到中断，退出程序")
            break
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    main()