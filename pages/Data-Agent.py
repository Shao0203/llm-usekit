import streamlit as st
import pandas as pd
from utils.agent_tool import dataframe_agent
from utils.sidebar import render_sidebar


lang, txt, model_provider = render_sidebar()


def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data)
    # 设置索引，方便 st.chart 直接使用
    df_data.set_index('columns', inplace=True)
    if chart_type == 'bar':
        st.bar_chart(df_data)
    elif chart_type == 'line':
        st.line_chart(df_data)
    elif chart_type == 'scatter':
        st.scatter_chart(df_data)


st.title(txt['agent_title'])

uploaded_csv = st.file_uploader(txt['agent_upload_hint'], type='csv')

if uploaded_csv:
    st.session_state['df'] = pd.read_csv(uploaded_csv)
    with st.expander(txt['original_data']):
        st.dataframe(st.session_state['df'])

left, right = st.columns([6, 1])
query = left.text_area(label='question', label_visibility='collapsed',
                       placeholder=txt['agent_question_hint'])
space_line = right.write('')
submit = right.button(txt['submit_question'],
                      disabled=not (uploaded_csv and query))

if submit and uploaded_csv and query:
    with st.spinner(txt['loading']):
        response_dict = dataframe_agent(
            model_provider, st.session_state['df'], query)

    if 'answer' in response_dict:
        st.write(response_dict['answer'])
    if 'table' in response_dict:
        st.table(pd.DataFrame(
            response_dict['table']['data'], columns=response_dict['table']['columns']))
    if 'bar' in response_dict:
        create_chart(response_dict['bar'], 'bar')
    if 'line' in response_dict:
        create_chart(response_dict['line'], 'line')
    if 'scatter' in response_dict:
        create_chart(response_dict['scatter'], 'scatter')

    with st.expander(txt['ai_res_data']):
        st.write(response_dict)

# print(st.session_state)
