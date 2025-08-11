from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper


def generate_script(subject, video_length, creativity, api_key, model_provider, lang):
    """
    subject: string, the video subject or topic
    video_length: float, the video length in minutes
    creativity: float, how creative of the video
    api_key: string, the api token to consume
    model_provider: string, OpenAI or DeepSeek or KIMI
    lang: string, language to use Chinese or English
    Return: list, tuple (wiki search result, video title, video script)
    """
    # define the model to use
    model_options = {
        'OpenAI': {'model': 'gpt-4o', 'base_url': ''},
        'KIMI': {'model': 'kimi-k2-0711-preview', 'base_url': 'https://api.moonshot.cn/v1'},
        'DeepSeek': {'model': 'deepseek-chat', 'base_url': 'https://api.deepseek.com/v1'},
    }
    llm = ChatOpenAI(
        api_key=api_key,
        base_url=model_options[model_provider]['base_url'],
        model=model_options[model_provider]['model'],
        temperature=creativity
    )
    # prompt template
    title_template = ChatPromptTemplate([
        ('human', '请为"{subject}"这个主题的视频想一个吸引人的标题，回答使用{lang}')
    ])
    script_template = ChatPromptTemplate([
        ("human",
         """你是一位短视频博主。根据以下标题和相关信息，写一个视频脚本，回答使用语种{lang}。
        视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
        要求开头抓住眼球，中间提供干货内容，结尾有惊喜。整体内容的表达方式要尽量轻松有趣，吸引年轻人。
        脚本格式也请按照【开头, 中间, 结尾】分隔，英文回答时请用【Opening, Body, Ending】分隔。
        脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关内容即可，不相关的忽略：
        ```{wikipedia_search}```""")
    ])
    # get wikipedia search result for this topic
    search_result = WikipediaAPIWrapper().run(subject)
    # define the invoke chain
    title_chain = title_template | llm
    script_chain = script_template | llm
    # generate video title and script by using large language model
    title = title_chain.invoke({'subject': subject, 'lang': lang}).content
    script = script_chain.invoke({
        'lang': lang,
        'title': title,
        'duration': video_length,
        'wikipedia_search': search_result,
    }).content

    return search_result, title, script
