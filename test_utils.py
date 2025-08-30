import pytest
import unittest.mock as mock
from utils import Generator


@mock.patch('utils.Generator._get_llm')
def test_get_llm(mock_get_llm):
    # set return value for _get_llm
    fake_llm = mock.MagicMock(name='MockLLM')
    mock_get_llm.return_value = fake_llm

    generator = Generator('fake_token', 'OpenAI', 0.5)
    # self._llm = self._get_llm()
    assert generator._llm is fake_llm
    mock_get_llm.assert_called_once()


@mock.patch('utils.ChatOpenAI')
def test_get_llm_success(mock_chat_openai):
    # set return value for ChatOpenAI
    fake_llm = mock.MagicMock(name='MockLLM')
    mock_chat_openai.return_value = fake_llm
    # 1st call: self._llm = self._get_llm()
    generator = Generator('fake_token', 'OpenAI', 0.5)
    llm = generator._get_llm()  # 2nd call

    assert llm is fake_llm
    assert mock_chat_openai.call_count == 2


@mock.patch('utils.ChatOpenAI')
def test_get_llm_kimi_success(mock_chat_openai):
    fake_llm = mock.MagicMock(name='MockLLM')
    mock_chat_openai.return_value = fake_llm
    generator = Generator('fake_token', 'KIMI', 0.5)
    assert generator._llm is fake_llm
    mock_chat_openai.assert_called_once()


def test_get_llm_failure():
    generator = Generator('fake_token', 'CloseAI', 0.5)
    assert generator._llm is None


@mock.patch('utils.ChatOpenAI', side_effect=Exception("boom"))
def test_get_llm_chatopenai_error(mock_chat_openai):
    generator = Generator('fake_token', 'OpenAI', 0.5)
    assert generator._llm is None
