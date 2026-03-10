#!/usr/bin/env python3
"""
AI Chat CLI - 多模型命令行聊天工具
支持 OpenAI GPT-4, Claude, DeepSeek 等模型
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

import openai
from anthropic import Anthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化控制台
console = Console()

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

class AIChatClient:
    """AI聊天客户端"""
    
    def __init__(self):
        self.history: List[Message] = []
        self.console = Console()
        
        # 初始化API客户端
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def add_message(self, role: str, content: str):
        """添加消息到历史"""
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat()
        )
        self.history.append(message)
        return message
    
    def call_openai(self, model: str, prompt: str) -> str:
        """调用OpenAI API"""
        try:
            messages = [{"role": "user", "content": prompt}]
            
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except openai.APIError as e:
            return f"OpenAI API错误: {e}"
        except Exception as e:
            return f"未知错误: {e}"
    
    def call_anthropic(self, model: str, prompt: str) -> str:
        """调用Anthropic API"""
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=1000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Anthropic API错误: {e}"
    
    def call_deepseek(self, prompt: str) -> str:
        """调用DeepSeek API（通过OpenAI兼容接口）"""
        try:
            # DeepSeek使用OpenAI兼容的API
            client = openai.OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"DeepSeek API错误: {e}"
    
    def chat_with_model(self, model_type: ModelType, prompt: str) -> str:
        """根据模型类型调用相应的API"""
        self.add_message("user", prompt)
        
        if model_type in [ModelType.OPENAI_GPT4, ModelType.OPENAI_GPT35]:
            response = self.call_openai(model_type.value, prompt)
        elif model_type in [ModelType.CLAUDE_OPUS, ModelType.CLAUDE_SONNET]:
            response = self.call_anthropic(model_type.value, prompt)
        elif model_type in [ModelType.DEEPSEEK_CHAT, ModelType.DEEPSEEK_CODER]:
            response = self.call_deepseek(prompt)
        else:
            response = "不支持的模型类型"
        
        self.add_message("assistant", response)
        return response
    
    def display_response(self, response: str, model_name: str):
        """美化显示响应"""
        console.print(f"\n[bold blue]{model_name}[/bold blue] 回复:")
        console.print(Panel(
            Markdown(response),
            border_style="green"
        ))
    
    def save_history(self, filename: str = "chat_history.json"):
        """保存聊天历史到文件"""
        history_data = [msg.to_dict() for msg in self.history]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
        
        console.print(f"[green]聊天历史已保存到 {filename}[/green]")
    
    def load_history(self, filename: str = "chat_history.json"):
        """从文件加载聊天历史"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            self.history = [
                Message(**msg_data) for msg_data in history_data
            ]
            console.print(f"[green]已加载 {len(self.history)} 条历史消息[/green]")
        except FileNotFoundError:
            console.print("[yellow]未找到历史文件，开始新对话[/yellow]")
        except Exception as e:
            console.print(f"[red]加载历史失败: {e}[/red]")

def show_welcome():
    """显示欢迎信息"""
    console.print(Panel.fit(
        "[bold cyan]AI Chat CLI - 多模型命令行聊天工具[/bold cyan]\n"
        "支持 OpenAI GPT-4, Claude, DeepSeek 等头部模型\n"
        "输入 'quit' 退出，'save' 保存历史，'load' 加载历史",
        border_style="cyan"
    ))

def select_model() -> ModelType:
    """选择模型"""
    console.print("\n[bold]请选择AI模型:[/bold]")
    console.print("1. OpenAI GPT-4")
    console.print("2. OpenAI GPT-3.5 Turbo")
    console.print("3. Claude 3 Opus")
    console.print("4. Claude 3 Sonnet")
    console.print("5. DeepSeek Chat")
    console.print("6. DeepSeek Coder")
    
    while True:
        choice = Prompt.ask("选择模型 (1-6)", default="1")
        
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
            console.print("[red]无效选择，请重试[/red]")

def check_api_keys():
    """检查API密钥"""
    missing_keys = []
    
    if not os.getenv("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
    if not os.getenv("ANTHROPIC_API_KEY"):
        missing_keys.append("ANTHROPIC_API_KEY")
    if not os.getenv("DEEPSEEK_API_KEY"):
        missing_keys.append("DEEPSEEK_API_KEY")
    
    if missing_keys:
        console.print(f"[yellow]警告: 缺少以下API密钥: {', '.join(missing_keys)}[/yellow]")
        console.print("请在 .env 文件中配置，或使用环境变量")
        console.print("部分功能可能无法使用")
        
        if not Confirm.ask("是否继续?", default=True):
            sys.exit(1)

def main():
    """主函数"""
    show_welcome()
    check_api_keys()
    
    # 创建客户端
    client = AIChatClient()
    
    # 选择模型
    model_type = select_model()
    model_name = model_type.value
    
    console.print(f"\n[green]已选择模型: {model_name}[/green]")
    console.print("开始聊天吧！输入 'quit' 退出\n")
    
    # 主聊天循环
    while True:
        try:
            # 获取用户输入
            user_input = Prompt.ask("[bold cyan]你[/bold cyan]")
            
            # 处理特殊命令
            if user_input.lower() == 'quit':
                if Confirm.ask("是否保存聊天历史?"):
                    client.save_history()
                console.print("[cyan]再见！[/cyan]")
                break
            
            elif user_input.lower() == 'save':
                filename = Prompt.ask("保存文件名", default="chat_history.json")
                client.save_history(filename)
                continue
            
            elif user_input.lower() == 'load':
                filename = Prompt.ask("加载文件名", default="chat_history.json")
                client.load_history(filename)
                continue
            
            elif user_input.lower() == 'model':
                model_type = select_model()
                model_name = model_type.value
                console.print(f"[green]已切换到模型: {model_name}[/green]")
                continue
            
            # 调用AI
            console.print("[yellow]思考中...[/yellow]")
            response = client.chat_with_model(model_type, user_input)
            
            # 显示响应
            client.display_response(response, model_name)
            
        except KeyboardInterrupt:
            console.print("\n[yellow]检测到中断，退出程序[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]错误: {e}[/red]")

if __name__ == "__main__":
    main()