import streamlit as st
import pandas as pd
from agent_tool import dataframe_agent


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


st.title('📈CSV数据分析智能助手')

uploaded_csv = st.file_uploader('请上传你要分析的CSV文件', type='csv')

if uploaded_csv:
    st.session_state['df'] = pd.read_csv(uploaded_csv)
    with st.expander('原始数据'):
        st.dataframe(st.session_state['df'])

left, right = st.columns([6, 1])
query = left.text_area(label='问题', label_visibility='collapsed',
                       placeholder='输入问题，如分析或提取数据，或可视化要求（支持条形图、折线图、散点图）')
space_line = right.write('')
submit = right.button('生成答案', disabled=not (uploaded_csv and query))

if submit and uploaded_csv and query:
    with st.spinner('🤔AI努力思考中，请稍等...☕️'):
        response_dict = dataframe_agent(st.session_state['df'], query)

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

    with st.expander('后台生成的响应数据'):
        st.write(response_dict)
