""" This module provides functions to generate video title/script based on user's preference. """

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from typing import Tuple, Literal
from functools import lru_cache
import json

__all__ = ['Generator']  # Expose only one interface - Generator


class Generator:
    """A generator uses LLM to create video script"""

    def __init__(self, api_key, model_provider, creativity):
        """All attributes are private and only used for llm initialization"""
        self._api_key = api_key
        self._model_provider = model_provider
        self._creativity = creativity
        self._llm = self._get_llm()

    def generate_script(self, subject: str, video_length: float,
                        lang: Literal['Chinese', 'English'], reference_prompt: str) -> Tuple[str, str, str]:
        """
        Generate a video script based on the given parameters.
        This is the ONLY public method for external calls.

        Args: 
            subject (str): The video subject or topic.
            video_length (float): The video length in minutes.
            lang (str): Language to use. Options: 'Chinese', 'English'.
            reference_prompt (str): contents of file if user uploads one.

        Returns:
            tuple: A tuple containing:
            - wiki_search (str): Relevant information retrieved from Wikipedia.
            - title (str): Generated video title.
            - script (str): Generated video script.
        """
        title_template, script_template = self._get_prompts_template(lang)
        wiki = self._get_wikipedia(subject, lang)
        title = self._generate_title(title_template, subject, lang)
        script = self._generate_content(
            script_template, lang, title, video_length, wiki, reference_prompt)
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
            base_url=model_options[self._model_provider]['base_url'],
            model=model_options[self._model_provider]['model'],
            api_key=self._api_key,
            temperature=self._creativity
        )

    def _get_prompts_template(self, lang):
        """Private: Get prompts template for video title and script."""
        with open('texts.json', 'r', encoding='utf-8') as f:
            TEXTS = json.load(f)
        title_template = ChatPromptTemplate([
            ("human", f"""{TEXTS[lang]['prompt_title_str']}""")
        ])
        script_template = ChatPromptTemplate([
            ("human", f"""{TEXTS[lang]['prompt_script_str']}""")
        ])
        return title_template, script_template

    @lru_cache(maxsize=5)  # cache recent wiki search records
    def _get_wikipedia(self, subject, lang):
        """Private: Get subject relevant info from Wikipedia."""
        lang_code = 'en' if lang == 'English' else 'zh'
        wiki = WikipediaAPIWrapper(lang=lang_code)
        return wiki.run(subject)

    def _generate_title(self, title_template, subject, lang):
        """Private: Generate script title."""
        title_chain = title_template | self._llm
        return title_chain.invoke({'subject': subject, 'lang': lang}).content

    def _generate_content(self, script_template, lang, title, video_length, wiki, reference_prompt):
        """Private: Generate script content."""
        script_chain = script_template | self._llm
        return script_chain.invoke({
            'lang': lang,
            'title': title,
            'duration': video_length,
            'wikipedia_search': wiki,
            'reference_prompt': reference_prompt
        }).content
