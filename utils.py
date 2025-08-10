from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper


def generate_script(subject, video_length, creativity, api_key):
    model = ChatOpenAI(
        api_key=api_key,
        base_url='https://api.moonshot.cn/v1',
        model='kimi-k2-0711-preview',
        temperature=creativity
    )

    title_template = ChatPromptTemplate([
        ('human', '请为"{subject}"这个主题的视频想一个吸引人的标题。')
    ])

    script_template = ChatPromptTemplate([
        ("human",
         """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
        视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
        要求开头抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
        整体内容的表达方式要尽量轻松有趣，吸引年轻人。
        脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关内容即可，对不相关的进行忽略：
        ```{wikipedia_search}```""")
    ])

    search_result = WikipediaAPIWrapper(lang='zh').run(subject)

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({'subject': subject}).content
    script = script_chain.invoke({
        'title': title,
        'duration': video_length,
        'wikipedia_search': search_result,
    }).content

    return search_result, title, script


# print(generate_script('KIMI AI 大模型', 1, 0.7, os.getenv('KIMI_API_KEY')))
