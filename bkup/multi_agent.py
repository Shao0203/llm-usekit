import os
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from langchain import hub
from langchain.memory import ConversationBufferMemory

from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_experimental import PythonREPLTool   # 2. python交互式解释器，deprecated
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_experimental.agents.agent_toolkits import create_csv_agent   # 3. csv agent
from langchain.tools import Tool    # 4. 整合多个tool


# 1 自建tool - 计算文字数量
class TextLengthTool(BaseTool):
    name: str = 'text length calculator'
    description: str = 'use this tool when calclulating the length of texts.'

    def _run(self, text):
        return len(text)


tools = [TextLengthTool()]

prompt = hub.pull('hwchase17/structured-chat-agent')

llm = ChatOpenAI(
    model='deepseek-chat',
    base_url='https://api.deepseek.com/v1',
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    temperature=0,
)

agent = create_structured_chat_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,    # 告诉agent有哪些工具可以使用
)

memory = ConversationBufferMemory(  # 如果想连续对话也可以加入记忆memroy
    memory_key='chat_history',
    return_messages=True
)

calc_agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,     # 在这里才是实际调用工具
    memory=memory,
    handle_parsing_errors=True,  # 把发生的错误作为观察，返还给大模型自行处理错误
    verbose=True,   # 详尽模式 - 打印出过程，比如选择哪歌工具
)

# response = calc_agent_executor.invoke({'input': '"君不见黄河之水天上来奔流到海不复回", 这句话的字数是多少？'})
# print('#####', response['output'])
# response = calc_agent_executor.invoke({'input': '地球上最高点在哪？'})   # 不调用工具，因为不是查字数
# print('@@@@@', response['output'])


# 2. 用现成的AI工具执行python代码 -- 废弃了
python_agent_executor = create_python_agent(
    llm=llm,
    tool=PythonREPLTool(),
    verbose=True,
    agent_executor_kwargs={'handle_parsing_errors': True},
)
# response = python_agent_executor.invoke({'input': '斐波那契数列第12个数字是什么？'})


# 3. 现成的分析csv文档
csv_agent_executor = create_csv_agent(
    llm=llm,
    path='house_price.csv',
    verbose=True,
    agent_executor_kwargs={'handle_parsing_errors': True},
    allow_dangerous_code=True,
)
# response = csv_agent_executor.invoke({'input': '数据集里所有房子的价格平均值是多少？'})
# print('$$$$$', response)

# 4. 组合调用多个工具 自建文字查数 + python解释器 + csv分析器
tools = [
    Tool(
        name='python代码工具',
        description='''当你需要借助python解释器时，使用这个工具。
        用自然语言把要求给这个工具，它会生成Python代码并返回代码执行的结果。''',
        func=python_agent_executor.invoke,
    ),
    Tool(
        name='csv分析工具',
        description='''当你需要回答有关house_price.csv文件的问题时，使用次工具。
        它接受完整的问题作为输入，在使用Pandas库计算后，返回答案。''',
        func=csv_agent_executor.invoke,
    ),
    TextLengthTool(),
]

agent = create_structured_chat_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    handle_parsing_errors=True,
    verbose=True,
)

# agent_executor.invoke({'input': '这里可以问问题关于1.查文字数；2.让python运行代码；3.处理csv})
