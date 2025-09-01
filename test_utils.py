import pytest
import unittest.mock as mock
from utils import Generator


@pytest.fixture
def generator():
    return Generator(api_key='fake_token', model_provider='OpenAI', creativity=0.5)


# ========== test _get_llm ==========
@mock.patch('utils.Generator._get_llm')
def test_get_llm(mock_get_llm):
    fake_llm = mock.MagicMock(name='MockLLM')
    mock_get_llm.return_value = fake_llm

    generator = Generator('fake_token', 'OpenAI', 0.5)
    assert generator._llm is fake_llm
    mock_get_llm.assert_called_once()


@mock.patch('utils.ChatOpenAI')
def test_get_llm_success(mock_chat_openai):
    fake_llm = mock.MagicMock(name='MockLLM')
    mock_chat_openai.return_value = fake_llm

    generator = Generator('fake_token', 'OpenAI', 0.5)
    llm = generator._get_llm()
    assert llm is fake_llm
    assert mock_chat_openai.call_count == 2


@mock.patch('utils.ChatOpenAI')
def test_get_llm_kimi_success(mock_chat_openai):
    fake_llm = mock.MagicMock(name='MockLLM')
    mock_chat_openai.return_value = fake_llm

    generator = Generator('fake_token', 'KIMI', 0.5)
    assert generator._llm is fake_llm
    mock_chat_openai.assert_called_once()


@mock.patch('utils.Generator._log_warning')
def test_get_llm_failure_logs(mock_log):
    generator = Generator('fake_token', 'CloseAI', 0.5)
    assert generator._llm is None
    mock_log.assert_called_once()


@mock.patch('utils.ChatOpenAI', side_effect=Exception("boom"))
def test_get_llm_chatopenai_error(mock_chat_openai):
    generator = Generator('fake_token', 'OpenAI', 0.5)
    assert generator._llm is None


# ========== test _get_prompts_template ==========
@mock.patch('utils.Generator._get_prompts_template')
def test_get_prompts_template(mock_get_prompts_template):
    fake_title_template = mock.MagicMock(name='MockTitleTemplate')
    fake_script_template = mock.MagicMock(name='MockScriptTemplate')
    mock_get_prompts_template.return_value = fake_title_template, fake_script_template

    generator = Generator('fake_token', 'OpenAI', 0.5)
    title_tplt, script_tplt = generator._get_prompts_template('English')
    assert title_tplt is fake_title_template and script_tplt is fake_script_template


@mock.patch('utils.ChatPromptTemplate')
def test_get_prompts_template_success(mock_chat_prompt_template, generator):
    fake_template = mock.MagicMock(name='MockTemplate')
    mock_chat_prompt_template.return_value = fake_template

    title_tplt, script_tplt = generator._get_prompts_template('English')
    assert title_tplt is fake_template and script_tplt is fake_template
    mock_chat_prompt_template.call_count == 2


@mock.patch('builtins.open', side_effect=FileNotFoundError('Mock File Not Found'))
def test_get_prompts_template_file_not_found(mock_open, generator):
    title_tplt, script_tplt = generator._get_prompts_template('English')
    assert 'Fallback prompt' in str(title_tplt)
    assert 'Fallback prompt' in str(script_tplt)
    mock_open.assert_called_once()


@mock.patch('builtins.open', new_callable=mock.mock_open, read_data='invalid json')
def test_get_prompts_template_json_decode_error(mock_open, generator):
    title_tplt, script_tplt = generator._get_prompts_template('English')
    assert 'Fallback prompt' in str(title_tplt)
    assert 'Fallback prompt' in str(script_tplt)
    mock_open.assert_called_once()


def test_get_prompts_template_french(generator):
    title_tpl, script_tpl = generator._get_prompts_template('French')
    assert 'Fallback title' in str(title_tpl)
    assert 'Fallback script' in str(script_tpl)
