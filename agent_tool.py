import os
import json
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# create_pandas_dataframe_agent 是 ReAct agent，它要求 LLM 输出的格式严格是：
# Thought: ... Action: ... Action Input: ... Final Answer: ...

PROMPT_TEMPLATE = """
你是一位数据分析助手，你的回应内容取决于用户的请求内容。

1. 对于文字回答的问题，按照这样的格式回答：
   Final Answer: {"answer": "<你的答案写在这里>"}
例如：
   Final Answer: {"answer": "订单量最高的产品ID是'MNWC3-067'"}

2. 如果用户需要一个表格，按照这样的格式回答：
   {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

3. 如果用户的请求适合返回条形图，按照这样的格式回答：
   {"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

4. 如果用户的请求适合返回折线图，按照这样的格式回答：
   {"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

5. 如果用户的请求适合返回散点图，按照这样的格式回答：
   {"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
注意：我们只支持三种类型的图表："bar", "line" 和 "scatter"。


请将所有输出作为JSON字符串返回。请注意要将"columns"列表和数据列表中的所有字符串都用双引号包围。
例如：{"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]]}

你要处理的用户请求如下： 
"""


def dataframe_agent(df, query):
    llm = ChatOpenAI(
        model='deepseek-chat',
        base_url='https://api.deepseek.com/v1',
        api_key=os.getenv('DEEPSEEK_API_KEY'),
        temperature=0,
    )

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        allow_dangerous_code=True,
        agent_executor_kwargs={'handle_parsing_errors': True},
    )

    prompt = PROMPT_TEMPLATE + query
    response = agent.invoke({'input': prompt})
    response_dict = json.loads(response['output'])
    return response_dict


df = pd.read_csv('house_price.csv')

# print('$$$$$: ', dataframe_agent(df, '数据集中所有房子卧室数的平均值是多少？'))
# $$$$$:  {'answer': '数据集中所有房子卧室数的平均值是2.97'}
# print('$$$$$: ', dataframe_agent(df, '用条形图展示所有房子的装修状态'))
# $$$$$:  {'bar': {'columns': ['furnished', 'semi-furnished', 'unfurnished'], 'data': [140, 227, 178]}}
# print('$$$$$: ', dataframe_agent(df, '提取价格高于1000万的房子信息。'))

# Agent 完整思考-行动-观察的步骤过程如下(针对上一个1000万的问题):
# > Entering new AgentExecutor chain...
# Thought: The user wants to extract house information where the price is above 10 million. I need to filter the dataframe where the 'price' column is greater than 10,000,000. Then I should return the filtered data in a table format.

# Action: python_repl_ast
# Action Input: df_filtered = df[df['price'] > 10000000]; print(df_filtered.head(10))
#       price   area  bedrooms  bathrooms  ...  airconditioning parking prefarea furnishingstatus
# 0  13300000   7420         4          2  ...              yes       2      yes        furnished
# 1  12250000   8960         4          4  ...              yes       3       no        furnished
# 2  12250000   9960         3          2  ...               no       2      yes   semi-furnished
# 3  12215000   7500         4          2  ...              yes       3      yes        furnished
# 4  11410000   7420         4          1  ...              yes       2       no        furnished
# 5  10850000   7500         3          3  ...              yes       2      yes   semi-furnished
# 6  10150000   8580         4          3  ...              yes       2      yes   semi-furnished
# 7  10150000  16200         5          3  ...               no       0       no      unfurnished

# [8 rows x 13 columns]
# Thought: I have filtered the dataframe to show houses with price above 10 million. There are 8 rows that meet this criteria. I should return the complete filtered data in a table format as requested.

# Action: python_repl_ast
# Action Input: df_filtered = df[df['price'] > 10000000]; print(df_filtered.to_dict(orient='split'))
# {'index': [0, 1, 2, 3, 4, 5, 6, 7], 'columns': ['price', 'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus'], 'data': [[13300000, 7420, 4, 2, 3, 'yes', 'no', 'no', 'no', 'yes', 2, 'yes', 'furnished'], [12250000, 8960, 4, 4, 4, 'yes', 'no', 'no', 'no', 'yes', 3, 'no', 'furnished'], [12250000, 9960, 3, 2, 2, 'yes', 'no', 'yes', 'no', 'no', 2, 'yes', 'semi-furnished'], [12215000, 7500, 4, 2, 2, 'yes', 'no', 'yes', 'no', 'yes', 3, 'yes', 'furnished'], [11410000, 7420, 4, 1, 2, 'yes', 'yes', 'yes', 'no', 'yes', 2, 'no', 'furnished'], [10850000, 7500, 3, 3, 1, 'yes', 'no', 'yes', 'no', 'yes', 2, 'yes', 'semi-furnished'], [10150000, 8580, 4, 3, 4, 'yes', 'no', 'no', 'no', 'yes', 2, 'yes', 'semi-furnished'], [10150000, 16200, 5, 3, 2, 'yes', 'no', 'no', 'no', 'no', 0, 'no', 'unfurnished']]}
# Thought: I now have the filtered data in a dictionary format. I can extract the columns and data to create the table response as specified in the instructions.

# Final Answer: {"table": {"columns": ["price", "area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "parking", "prefarea", "furnishingstatus"], "data": [[13300000, 7420, 4, 2, 3, "yes", "no", "no", "no", "yes", 2, "yes", "furnished"], [12250000, 8960, 4, 4, 4, "yes", "no", "no", "no", "yes", 3, "no", "furnished"], [12250000, 9960, 3, 2, 2, "yes", "no", "yes", "no", "no", 2, "yes", "semi-furnished"], [12215000, 7500, 4, 2, 2, "yes", "no", "yes", "no", "yes", 3, "yes", "furnished"], [11410000, 7420, 4, 1, 2, "yes", "yes", "yes", "no", "yes", 2, "no", "furnished"], [10850000, 7500, 3, 3, 1, "yes", "no", "yes", "no", "yes", 2, "yes", "semi-furnished"], [10150000, 8580, 4, 3, 4, "yes", "no", "no", "no", "yes", 2, "yes", "semi-furnished"], [10150000, 16200, 5, 3, 2, "yes", "no", "no", "no", "no", 0, "no", "unfurnished"]]}}

# > Finished chain.
# $$$$$:  {'table': {'columns': ['price', 'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus'], 'data': [[13300000, 7420, 4, 2, 3, 'yes', 'no', 'no', 'no', 'yes', 2, 'yes', 'furnished'], [12250000, 8960, 4, 4, 4, 'yes', 'no', 'no', 'no', 'yes', 3, 'no', 'furnished'], [12250000, 9960, 3, 2, 2, 'yes', 'no', 'yes', 'no', 'no', 2, 'yes', 'semi-furnished'], [12215000, 7500, 4, 2, 2, 'yes', 'no', 'yes', 'no', 'yes', 3, 'yes', 'furnished'], [11410000, 7420, 4, 1, 2, 'yes', 'yes', 'yes', 'no', 'yes', 2, 'no', 'furnished'], [10850000, 7500, 3, 3, 1, 'yes', 'no', 'yes', 'no', 'yes', 2, 'yes', 'semi-furnished'], [10150000, 8580, 4, 3, 4, 'yes', 'no', 'no', 'no', 'yes', 2, 'yes', 'semi-furnished'], [10150000, 16200, 5, 3, 2, 'yes', 'no', 'no', 'no', 'no', 0, 'no', 'unfurnished']]}}
