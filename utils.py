""" This module provides functions to generate video title/script based on user's preference. """

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

__all__ = ['Generator']  # Expose only one interface - Generator


class Generator:
    """A generator uses LLM to create video script"""

    def __init__(self, api_key, model_provider, creativity):
        """All attributes are private and only used for initialization"""
        self._api_key = api_key
        self._model_provider = model_provider
        self._creativity = creativity
        self._llm = self._get_llm()

    def generate_script(self, subject, video_length, lang):
        """
        Generate a video script based on the given parameters.
        This is the ONLY public method for external calls.

        Args: 
            subject (str): The video subject or topic.
            video_length (float): The video length in minutes.
            lang (str): Language to use. Options: 'Chinese', 'English'.

        Returns:
            tuple: A tuple containing:
            - wiki_search (str): Relevant information retrieved from Wikipedia.
            - title (str): Generated video title.
            - script (str): Generated video script.
        """
        title_template, script_template = self._get_prompts_template()
        wiki = self._get_wikipedia(subject, lang)
        title = self._generate_title(title_template, subject, lang)
        script = self._generate_content(
            script_template, lang, title, video_length, wiki)
        return wiki, title, script

    # ------------------- private methods below -------------------
    def _get_llm(self):
        """Private: Get selected LLM instance."""
        model_options = {
            'OpenAI': {'model': 'gpt-4o', 'base_url': ''},
            'KIMI': {'model': 'kimi-k2-0711-preview', 'base_url': 'https://api.moonshot.cn/v1'},
            'DeepSeek': {'model': 'deepseek-chat', 'base_url': 'https://api.deepseek.com/v1'},
        }
        return ChatOpenAI(
            api_key=self._api_key,
            base_url=model_options[self._model_provider]['base_url'],
            model=model_options[self._model_provider]['model'],
            temperature=self._creativity
        )

    def _get_prompts_template(self):
        """Private: Get prompts template for video title and script."""
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

    def _get_wikipedia(self, subject, lang):
        """Private: Get subject relevant info from Wikipedia."""
        lang_code = 'en' if lang == 'English' else 'zh'
        wiki = WikipediaAPIWrapper(lang=lang_code)
        return wiki.run(subject)

    def _generate_title(self, title_template, subject, lang):
        """Private: Generate script title."""
        title_chain = title_template | self._llm
        return title_chain.invoke({'subject': subject, 'lang': lang}).content

    def _generate_content(self, script_template, lang, title, video_length, wiki):
        """Private: Generate script content."""
        script_chain = script_template | self._llm
        return script_chain.invoke({
            'lang': lang,
            'title': title,
            'duration': video_length,
            'wikipedia_search': wiki,
        }).content
