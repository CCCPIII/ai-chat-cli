#!/usr/bin/env python3
"""
API调用测试脚本
演示如何调用不同AI模型的API
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_openai_api():
    """测试OpenAI API调用"""
    print("=== 测试OpenAI API ===")
    
    try:
        import openai
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key.startswith("sk-test"):
            print("[ERROR] 未配置有效的OpenAI API密钥")
            return False
        
        client = openai.OpenAI(api_key=api_key)
        
        # 简单测试调用
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, say hi!"}],
            max_tokens=10
        )
        
        print(f"[OK] OpenAI API调用成功")
        print(f"响应: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"[ERROR] OpenAI API调用失败: {e}")
        return False

def test_anthropic_api():
    """测试Anthropic API调用"""
    print("\n=== 测试Anthropic API ===")
    
    try:
        from anthropic import Anthropic
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key.startswith("sk-ant-test"):
            print("[ERROR] 未配置有效的Anthropic API密钥")
            return False
        
        client = Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # 使用便宜的模型测试
            max_tokens=10,
            messages=[{"role": "user", "content": "Hello, say hi!"}]
        )
        
        print(f"[OK] Anthropic API调用成功")
        print(f"响应: {response.content[0].text}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Anthropic API调用失败: {e}")
        return False

def test_deepseek_api():
    """测试DeepSeek API调用"""
    print("\n=== 测试DeepSeek API ===")
    
    try:
        import openai
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key or api_key.startswith("test-"):
            print("[ERROR] 未配置有效的DeepSeek API密钥")
            return False
        
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "Hello, say hi!"}],
            max_tokens=10
        )
        
        print(f"[OK] DeepSeek API调用成功")
        print(f"响应: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"[ERROR] DeepSeek API调用失败: {e}")
        return False

def main():
    """主测试函数"""
    print("AI API调用测试工具")
    print("=" * 40)
    
    # 检查环境变量
    print("检查环境变量配置:")
    for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY"]:
        value = os.getenv(key)
        if value and not value.startswith(("sk-test", "test-")):
            print(f"  [OK] {key}: 已配置")
        else:
            print(f"  [WARN] {key}: 未配置或为测试值")
    
    print("\n" + "=" * 40)
    
    # 运行测试
    tests_passed = 0
    tests_total = 3
    
    tests_passed += 1 if test_openai_api() else 0
    tests_passed += 1 if test_anthropic_api() else 0
    tests_passed += 1 if test_deepseek_api() else 0
    
    # 总结
    print("\n" + "=" * 40)
    print(f"测试完成: {tests_passed}/{tests_total} 通过")
    
    if tests_passed == 0:
        print("\n[WARN] 所有API测试都失败或未配置")
        print("请按照以下步骤操作:")
        print("1. 获取API密钥:")
        print("   - OpenAI: https://platform.openai.com/api-keys")
        print("   - Anthropic: https://console.anthropic.com/")
        print("   - DeepSeek: https://platform.deepseek.com/api_keys")
        print("2. 编辑 .env 文件，填入真实API密钥")
        print("3. 重新运行测试")
    elif tests_passed < tests_total:
        print(f"\n[WARN] 部分API测试失败")
        print("可以继续开发，但部分功能可能受限")
    else:
        print("\n[SUCCESS] 所有API测试通过！")
        print("可以完整使用所有功能")

if __name__ == "__main__":
    main()