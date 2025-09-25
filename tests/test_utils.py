import pytest
import unittest.mock as mock
from utils.vsgen import Generator


@pytest.fixture
def generator():
    return Generator(api_key='fake_token', model_provider='OpenAI', creativity=0.5)


# ========== test _get_llm ==========
@mock.patch('utils.vsgen.Generator._get_llm')
def test_get_llm_call(mock_get_llm):
    fake_llm = mock.MagicMock(name='MockLLM')
    mock_get_llm.return_value = fake_llm

    generator = Generator('fake_token', 'OpenAI', 0.5)
    assert generator._llm is fake_llm
    mock_get_llm.assert_called_once()


@mock.patch('utils.vsgen.ChatOpenAI')
def test_get_llm_success(mock_chat_openai):
    fake_llm = mock.MagicMock(name='MockLLM')
    mock_chat_openai.return_value = fake_llm

    generator = Generator('fake_token', 'OpenAI', 0.5)
    llm = generator._get_llm()
    assert llm is fake_llm
    assert mock_chat_openai.call_count == 2


@mock.patch('utils.vsgen.ChatOpenAI')
def test_get_llm_kimi_success(mock_chat_openai):
    fake_llm = mock.MagicMock(name='MockLLM')
    mock_chat_openai.return_value = fake_llm

    generator = Generator('fake_token', 'KIMI', 0.5)
    assert generator._llm is fake_llm
    mock_chat_openai.assert_called_once()


@mock.patch('utils.vsgen.Generator._log_warning')
def test_get_llm_failure_logs(mock_log):
    generator = Generator('fake_token', 'CloseAI', 0.5)
    assert generator._llm is None
    mock_log.assert_called_once()


@mock.patch('utils.vsgen.ChatOpenAI', side_effect=Exception("boom"))
def test_get_llm_chatopenai_error(mock_chat_openai):
    generator = Generator('fake_token', 'OpenAI', 0.5)
    assert generator._llm is None


# ========== test _get_prompts_template ==========
@mock.patch('utils.vsgen.Generator._get_prompts_template')
def test_get_prompts_template_call(mock_get_prompts_template):
    fake_title_template = mock.MagicMock(name='MockTitleTemplate')
    fake_script_template = mock.MagicMock(name='MockScriptTemplate')
    mock_get_prompts_template.return_value = fake_title_template, fake_script_template

    generator = Generator('fake_token', 'OpenAI', 0.5)
    title_tplt, script_tplt = generator._get_prompts_template('English')
    assert title_tplt is fake_title_template and script_tplt is fake_script_template


@mock.patch('utils.vsgen.ChatPromptTemplate')
def test_get_prompts_template_success(mock_chat_prompt_template, generator):
    fake_template = mock.MagicMock(name='MockTemplate')
    mock_chat_prompt_template.return_value = fake_template

    title_tplt, script_tplt = generator._get_prompts_template('English')
    assert title_tplt is fake_template and script_tplt is fake_template
    assert mock_chat_prompt_template.call_count == 2


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


# ========== test _get_wikipedia ==========
@mock.patch('utils.vsgen.Generator._get_wikipedia')
def test_get_wikipedia_call(mock_get_wikipedia, generator):
    mock_get_wikipedia.return_value = 'Mock search result'
    wiki_result = generator._get_wikipedia('fake_subject', 'English')
    assert wiki_result == 'Mock search result'
    mock_get_wikipedia.assert_called_once()


@mock.patch('utils.vsgen.WikipediaAPIWrapper.run')
def test_get_wikipedia_success(mock_run, generator):
    mock_run.return_value = 'Mock search result'
    wiki_result = generator._get_wikipedia('fake_subject', 'English')
    assert wiki_result == 'Mock search result'
    mock_run.assert_called_once()


@mock.patch('utils.vsgen.WikipediaAPIWrapper.run', side_effect=Exception('Mock search failed'))
def test_get_wikipedia_error(mock_run, generator):
    wiki_result = generator._get_wikipedia('fake_subject', 'English')
    assert wiki_result.startswith('Fallback')
    mock_run.assert_called_once()


# ========== test _generate_title ==========
@mock.patch('utils.vsgen.Generator._generate_title')
def test_generate_title_call(mock_generate_title, generator):
    # test only the function call, won't go through the inside logic
    mock_generate_title.return_value = 'Mock Title'
    title = generator._generate_title('title_template', 'subject', 'lang')
    assert title == 'Mock Title'


def test_generate_title_success(generator):
    fake_llm = mock.MagicMock(name='MockLLM')
    fake_template = mock.MagicMock(name='MockTemplate')
    fake_chain = mock.MagicMock(name='MockChain')

    # Mock pipe operation: fake_template | fake_llm → fake_chain
    fake_template.__or__.return_value = fake_chain
    fake_chain.invoke.return_value.content = 'Generated Title'

    # passby the real _get_llm function call
    generator._llm = fake_llm
    title = generator._generate_title(fake_template, 'subject1', 'English')

    assert title == 'Generated Title'
    fake_template.__or__.assert_called_once_with(fake_llm)
    fake_chain.invoke.assert_called_once_with(
        {'subject': 'subject1', 'lang': 'English'})


@mock.patch('utils.vsgen.Generator._get_llm')
def test_generate_title_success_chinese(mock_get_llm):
    fake_llm = mock.MagicMock(name='MockLLM')
    fake_template = mock.MagicMock(name='MockTemplate')
    fake_chain = mock.MagicMock(name='MockChain')

    fake_template.__or__.return_value = fake_chain
    fake_chain.invoke.return_value.content = 'Generated Title CN'

    mock_get_llm.return_value = fake_llm
    generator = Generator('fake_token', 'OpenAI', 0.5)
    title = generator._generate_title(fake_template, 'subject2', 'Chinese')

    assert title == 'Generated Title CN'
    fake_template.__or__.assert_called_once_with(generator._llm)
    fake_chain.invoke.assert_called_once_with(
        {'subject': 'subject2', 'lang': 'Chinese'})


def test_generate_title_failure(generator):
    fake_template = mock.MagicMock(name='BadTemplate')
    fake_llm = mock.MagicMock(name='BadLLM')

    generator._llm = fake_llm
    fake_template.__or__.side_effect = Exception('BadChain')

    title = generator._generate_title(fake_template, 'subject1', 'English')
    assert 'Error' in title


# ========== test _generate_content ==========
@mock.patch('utils.vsgen.Generator._generate_content')
def test_generate_content_call(mock_generate_content, generator):
    # test only the function call, won't go through the inside logic
    mock_generate_content.return_value = 'Mock script'
    script = generator._generate_content(
        'script_template', 'English', 'title', 1, 'wiki', 'ref')
    assert script == 'Mock script'


@mock.patch('utils.vsgen.Generator._get_llm')
def test_generate_content_success(mock_get_llm):
    fake_llm = mock.MagicMock(name='MockLLM')
    fake_template = mock.MagicMock(name='MockTemplate')
    fake_chain = mock.MagicMock(name='MockChain')

    fake_template.__or__.return_value = fake_chain
    fake_chain.invoke.return_value.content = 'Generated script'
    mock_get_llm.return_value = fake_llm

    generator = Generator('fake_token', 'OpenAI', 0.5)
    script = generator._generate_content(
        fake_template, 'English', 'title1', 1, 'wiki', 'ref')

    assert script == 'Generated script'
    fake_template.__or__.assert_called_once_with(fake_llm)
    fake_chain.invoke.assert_called_once_with({
        'lang': 'English', 'title': 'title1', 'duration': 1,
        'wikipedia_search': 'wiki', 'reference_prompt': 'ref'})


def test_generate_content_success_chinese(generator):
    fake_llm = mock.MagicMock(name='MockLLM')
    fake_template = mock.MagicMock(name='MockTemplate')
    fake_chain = mock.MagicMock(name='MockChain')

    generator._llm = fake_llm
    fake_template.__or__.return_value = fake_chain
    fake_chain.invoke.return_value.content = 'Generated script CN'

    script = generator._generate_content(
        fake_template, 'Chinese', 'title2', 1, 'wiki', 'ref')
    assert script == 'Generated script CN'
    fake_template.__or__.assert_called_once_with(fake_llm)
    fake_chain.invoke.assert_called_once_with({
        'lang': 'Chinese', 'title': 'title2', 'duration': 1,
        'wikipedia_search': 'wiki', 'reference_prompt': 'ref'})


def test_generate_content_failure(generator):
    fake_llm = mock.MagicMock(name='BadLLM')
    fake_template = mock.MagicMock(name='BadTemplate')

    generator._llm = fake_llm
    fake_template.__or__.side_effect = Exception('BadChain')

    script = generator._generate_content(
        fake_template, 'English', 'title1', 1, 'wiki', 'ref')
    assert 'Error' in script


# ========== test generate_script ==========
@mock.patch('utils.vsgen.Generator.generate_script')
def test_generate_script_call(mock_generate_script, generator):
    # test only the function call, won't go through the inside logic
    mock_generate_script.return_value = ('wiki', 'title', 'script')
    result = generator.generate_script('subject', 1, 'English', 'ref')
    assert result == ('wiki', 'title', 'script')
    mock_generate_script.assert_called_once()


@mock.patch('utils.vsgen.Generator._generate_content')
@mock.patch('utils.vsgen.Generator._generate_title')
@mock.patch('utils.vsgen.Generator._get_wikipedia')
@mock.patch('utils.vsgen.Generator._get_prompts_template')
@mock.patch('utils.vsgen.Generator._get_llm')
def test_generate_script_success(
        mock_get_llm, mock_get_prompts_template, mock_get_wikipedia,
        mock_generate_title, mock_generate_content):
    # Mock return values of each function call
    mock_get_llm.return_value = mock.MagicMock(name='MockLLM')
    mock_get_prompts_template.return_value = mock.MagicMock(
        name='MockTitleTemplate'), mock.MagicMock(name='MockScriptTemplate')
    mock_get_wikipedia.return_value = 'Mock Wiki'
    mock_generate_title.return_value = 'Mock Title'
    mock_generate_content.return_value = 'Mock Script'

    generator = Generator('fake_token', 'OpenAI', 0.5)
    result = generator.generate_script('subject', 1, 'English', 'ref')
    assert result == ('Mock Wiki', 'Mock Title', 'Mock Script')


@mock.patch('utils.vsgen.Generator._get_llm')
def test_generate_script_llm_init_failed(mock_get_llm):
    mock_get_llm.return_value = None
    generator = Generator('fake_token', 'OpenAI', 0.5)
    result = generator.generate_script('subject', 1, 'English', 'ref')
    assert result == ('LLM init failed', 'LLM init failed', 'LLM init failed')
    mock_get_llm.assert_called_once()


@mock.patch('utils.vsgen.Generator._get_prompts_template', side_effect=Exception('boom'))
def test_generate_script_failure(mock_get_prompts_template, generator):
    result = generator.generate_script('subject', 1, 'English', 'ref')
    assert result == ('Wiki fetch failed',
                      'Title generation failed', 'Script generation failed')
    mock_get_prompts_template.assert_called_once()
