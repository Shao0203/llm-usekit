# 📦 llm-usekit

## 🚀 项目简介 (English Version below)
`llm-usekit` 是一个基于 **LangChain + Streamlit + 多家大模型 API (OpenAI, DeepSeek, Kimi, Qwen 等)** 的多功能大模型工具集。  
它提供了多种开箱即用的 LLM 应用，包括：

- 🎬 **视频脚本生成器**（Video Script Generator）  
- 💬 **智能聊天助手**（Chat-Bot with memory）  
- 📑 **文档问答 (RAG)** —— 上传文档后基于向量数据库进行精准问答  
- 📊 **数据分析 Agent** —— 上传 CSV 文件后可进行数据分析和可视化  


## 📂 项目结构
```bash
llm-usekit/  
├── utils/                 # 工具 & 后台逻辑  
│ ├── vsgen.py             # 视频脚本生成器逻辑  
│ ├── chat.py              # 聊天助手逻辑  
│ ├── rag_tool.py          # RAG 文档问答逻辑  
│ ├── agent_tool.py        # 数据分析 Agent 逻辑  
│ ├── sidebar.py           # 通用侧边栏（语言切换 & 模型选择）  
│ └── llm_factory.py       # 统一的大模型实例工厂  
│  
├── pages/                 # Streamlit 多页面前端  
│ ├── Chat-Bot.py          # 聊天助手页面  
│ ├── Q&A-Rag.py           # 文档问答页面  
│ └── Data-Agent.py        # 数据分析 Agent 页面  
│  
├── VS-Gen.py              # 主入口页面（视频脚本生成器）  
├── texts.json             # 多语言文案配置  
├── requirements.txt       # 依赖文件  
└── README.md              # 项目说明文档  
```


## ⚙️ 环境配置

1. 克隆仓库：
   ```bash
   git clone https://github.com/Shao0203/llm-usekit.git
   ```
2. 创建虚拟环境并安装依赖：  
   ```bash
   cd llm-usekit               # 进入项目目录
   python -m venv .venv        # 创建虚拟环境
   source .venv/bin/activate   # Mac/Linux
   .\env\Scripts\activate      # Windows

   pip install -r requirements.txt
   ```
3. 配置 API Keys:  
   本地开发时可以在项目根目录下创建 `.env`文件: 
   ```bash
   # .env文件中存入以下api keys信息 - 
   OPENAI_API_KEY = "your_openai_key"
   DEEPSEEK_API_KEY = "your_deepseek_key"
   KIMI_API_KEY = "your_kimi_key"
   QWEN_API_KEY = "your_qwen_key"
   ```
   或在系统环境变量`.zshrc`中配置:
   ```bash
   # vi ~/.zshrc - 命令行进入系统环境变量，然后存入以下api keys信息：
   export OPENAI_API_KEY = "your_openai_key"
   export DEEPSEEK_API_KEY = "your_deepseek_key"
   export KIMI_API_KEY = "your_kimi_key"
   export QWEN_API_KEY = "your_qwen_key"
   ```


## ▶️ 运行项目
启动主页面 - 视频脚本生成器 (所有子页面随之一并启动)：  
```bash
streamlit run VS-Gen.py  
```
- 启动后浏览器会自动打开：`http://localhost:8501`  
- 左侧导航栏可切换到 Chat-Bot / Q&A-Rag / Data-Agent 页面。


## 📌 功能说明
1. 🎬 VS-Gen  
   输入视频主题，生成视频脚本文案；  
   所有页面可调用不同大模型（OpenAI / DeepSeek / Kimi / Qwen）；  
2. 🤖 Chat-Bot  
   带记忆的多轮对话（类似Chatgpt或DeepSeek使用体验）；  
   基于 RunnableWithMessageHistory + InMemoryChatMessageHistory；  
3. 📄 Q&A-RAG  
   上传文档 → 向量化存储 → 智能问答；  
   让 AI 基于你提供的知识来回答问题（Retrieval Augmented Generation）；  
4. 📊 Data-Agent  
   上传 CSV 文件 → 提出分析/绘图需求 → 自动生成结果；  
   基于 LangChain Agent + Pandas；  


## ✨ 功能亮点
- **🔄 多语言支持**（中文 / English / 可扩展任意语种）  
- **🧩 模块化设计**（不同工具独立实现，统一集成，前后端分离）  
- **🔌 多模型支持**（OpenAI / DeepSeek / Kimi / Qwen，在侧边栏切换。可扩展任意模型）  
- **💾 会话记忆**（Chat-Bot 页面支持对话历史记忆）  
- **📚 文档问答** RAG（支持 TXT / PDF / DOCX 上传，向量化存储检索）  
- **📊 数据分析** Agent（上传CSV文档，数据分析总结与自动生成可视化图表）  


## 📜 License
本项目采用 MIT License。  
自由使用、修改和二次开发，但请保留原始声明。  


## 💡 致谢
本项目基于以下优秀项目与框架构建：  
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://platform.openai.com/)
- [DeepSeek](https://www.deepseek.com/)
- [Kimi](https://platform.moonshot.cn/docs/)
- [Qwen](https://www.tongyi.com/)

