# AI Chat CLI - 多模型命令行聊天工具

一个支持多个头部AI模型的命令行聊天工具，用于学习和实践API调用。

## 功能特性

- ✅ 支持多个头部AI模型：
  - OpenAI: GPT-4, GPT-3.5 Turbo
  - Anthropic: Claude 3 Opus, Claude 3 Sonnet
  - DeepSeek: Chat, Coder
- ✅ 美观的命令行界面（使用Rich库）
- ✅ 聊天历史保存和加载
- ✅ 错误处理和API密钥验证
- ✅ Markdown格式响应显示

## 安装

### 1. 克隆或下载项目

### 2. 安装依赖
```bash
pip install openai anthropic python-dotenv rich
```

### 3. 配置API密钥
复制 `.env.example` 为 `.env` 并填入你的API密钥：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
DEEPSEEK_API_KEY=your-deepseek-api-key-here
```

### 4. 获取API密钥
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [Anthropic Console](https://console.anthropic.com/)
- [DeepSeek API Keys](https://platform.deepseek.com/api_keys)

## 使用方法

### 基本使用
```bash
python ai_chat_cli.py
```

### 命令行参数（计划中）
```bash
# 指定模型
python ai_chat_cli.py --model gpt-4

# 单次问答
python ai_chat_cli.py --prompt "你好，世界！"

# 加载历史
python ai_chat_cli.py --load history.json
```

### 交互命令
- `quit` - 退出程序
- `save` - 保存聊天历史
- `load` - 加载聊天历史
- `model` - 切换模型

## 项目结构
```
ai_chat_cli/
├── ai_chat_cli.py      # 主程序
├── .env.example        # API密钥配置示例
├── .env                # 实际配置（不要提交到Git）
├── README.md           # 说明文档
└── requirements.txt    # 依赖列表
```

## 技术栈
- **Python 3.8+**
- **openai** - OpenAI API客户端
- **anthropic** - Anthropic API客户端
- **rich** - 命令行美化
- **python-dotenv** - 环境变量管理

## 学习要点

这个项目涵盖了以下API调用实践：

1. **多模型API集成**
   - 不同API提供商（OpenAI, Anthropic, DeepSeek）
   - 统一的接口设计

2. **错误处理**
   - API调用异常处理
   - 网络错误重试（计划中）
   - 速率限制处理（计划中）

3. **数据持久化**
   - JSON格式聊天历史保存
   - 环境变量配置管理

4. **用户体验**
   - 美观的命令行界面
   - Markdown渲染
   - 交互式提示

## 扩展计划

- [ ] 添加流式响应（打字机效果）
- [ ] 支持图像生成（DALL-E, Midjourney API）
- [ ] 添加语音输入/输出
- [ ] 实现插件系统
- [ ] 添加Web界面版本

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License