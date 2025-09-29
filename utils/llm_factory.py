"""这个模块提供一个公共的大模型工厂，供其他所有后台逻辑创建不同的llm实例"""

import os
import streamlit as st
from langchain_openai import ChatOpenAI

MODEL_OPTIONS = {
    'OpenAI': {'model': 'gpt-5-mini', 'key_name': 'OPENAI_API_KEY', 'base_url': ''},
    'Kimi': {'model': 'kimi-k2-0905-preview', 'key_name': 'KIMI_API_KEY', 'base_url': 'https://api.moonshot.cn/v1'},
    'DeepSeek': {'model': 'deepseek-chat', 'key_name': 'DEEPSEEK_API_KEY', 'base_url': 'https://api.deepseek.com/v1'},
    'Qwen': {'model': 'qwen-plus', 'key_name': 'QWEN_API_KEY', 'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1'},
}


def get_api_key(key_name):
    """Get model api_key from secrets.toml(deployed) or env variable(local)."""
    try:
        return st.secrets[key_name]
    except Exception:
        return os.getenv(key_name)


def get_llm(model_provider, creativity=0.3):
    """工厂方法：根据不同 model_provider 创建 LLM 实例"""
    if model_provider not in MODEL_OPTIONS:
        raise ValueError(
            f'Unknown model provider <{model_provider}>. Available providers: {list(MODEL_OPTIONS.keys())}'
        )

    selected_model = MODEL_OPTIONS[model_provider]

    return ChatOpenAI(
        model=selected_model['model'],
        base_url=selected_model['base_url'],
        api_key=get_api_key(selected_model['key_name']),
        temperature=creativity,
    )
