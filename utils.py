""" This module provides functions to generate video title/script based on user's preference. """

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper


def generate_script(subject, video_length, creativity, api_key, model_provider, lang):
    """
    Generate a video script based on the given parameters.

    Args: 
        subject (str): The video subject or topic.
        video_length (float): The video length in minutes.
        creativity (float): Creativity level of the video (0.0 to 1.0).
        api_key (str): API token for authentication.
        model_provider (str): LLM provider to choice. Options: 'OpenAI', 'DeepSeek', 'KIMI'.
        lang (str): Language to use. Options: 'Chinese', 'English'.

    Returns:
        tuple: A tuple containing:
        - wiki_search (str): Relevant information retrieved from Wikipedia.
        - title (str): Generated video title.
        - script (str): Generated video script.
    """
    llm = get_llm(api_key, model_provider, creativity)
    title_template, script_template = get_prompts_template()
    wiki = get_wikipedia(subject, lang)
    title = generate_title(llm, title_template, subject, lang)
    script = generate_content(llm, script_template,
                              lang, title, video_length, wiki)
    return wiki, title, script


def get_llm(api_key, model_provider, creativity):
    """Get selected llm"""
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
    return llm


def get_prompts_template():
    """Get prompts template for title and script"""
    title_template = ChatPromptTemplate([
        ('human', '请为"{subject}"这个主题的视频想一个吸引人的标题，回答使用{lang}')
    ])
    script_template = ChatPromptTemplate([
        ("human",
         """你是一位短视频博主。根据以下标题和相关信息，写一个视频脚本，回答使用语种{lang}。
        视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
        要求开头抓住眼球，中间提供干货内容，结尾有惊喜。整体内容的表达方式要尽量轻松有趣，吸引年轻人。
        脚本格式按照【开头】【中间】【结尾】分隔; 若英文回答请用【Opening】【Body】【Ending】分隔。
        脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关内容即可，不相关的忽略：
        ```{wikipedia_search}```""")
    ])
    return title_template, script_template


def get_wikipedia(subject, lang):
    """Get subject relevant info from Wiki"""
    lang = 'en' if lang == 'English' else 'zh'
    wiki = WikipediaAPIWrapper(lang=lang)
    return wiki.run(subject)


def generate_title(llm, title_template, subject, lang):
    """Generate script title"""
    title_chain = title_template | llm
    title = title_chain.invoke({'subject': subject, 'lang': lang}).content
    return title


def generate_content(llm, script_template, lang, title, video_length, wiki):
    """Generate script content"""
    script_chain = script_template | llm
    script = script_chain.invoke({
        'lang': lang,
        'title': title,
        'duration': video_length,
        'wikipedia_search': wiki,
    }).content
    return script
