import streamlit as st
import pandas as pd


st.write('## *Hello world* !!!')

st.image('./pages/Rabbit.jpeg', width=200)

['apple', 'pear', 'orange']

{'name': 'Tom', 'age': 20, 'gender': 'male', 'hobby': 'sports'}

2**10

df = pd.DataFrame({
    'name': ['Bob', 'Candy', 'Dave', 'Eddy'],
    'id': ['01', '02', '03', '04'],
    'class': ['one', 'two', 'three', 'four'],
    'grade': [60, 70, 80, 90],
})

df
st.divider()
st.dataframe(df)
st.table(df)


st.write('## Hello!')

name = st.text_input('please input your name.')
if name:
    st.write(f'Welcome {name} ~')

password = st.text_input('please enter your password', type='password')

intro = st.text_area('Please introduce yourself:')

age = st.number_input('Please enter your age:', value=20,
                      min_value=0, max_value=150, step=1)
st.write(f'You are {age} years old.')

is_agreed = st.checkbox('Agree')
if is_agreed:
    st.write('Thanks!')

st.divider()

is_submitted = st.button('Submit', type='primary')
if is_submitted:
    st.write('Submitted Successfully!')


gender = st.radio('Gender', options=['Male', 'Female', 'Not sure'], index=None)
if gender:
    st.write(f'Your gender is {gender}')

qualification = st.selectbox('Qualification', options=[
    'Doctor', 'Master', 'Bachelor', 'High school'], index=None)
if qualification:
    st.write(f'You have a {qualification} degree.')

contacts = st.multiselect(
    'Contact', options=['Email', 'Phone', 'Mobile', 'Text'])
if contacts:
    st.write(f'We will contact you by {', '.join(contacts)}')

hobbies = st.multiselect(
    'Hobby: ', options=['swim', 'basketball', 'piano', 'painting', 'hiking'])
if hobbies:
    st.write(f'Your hobbies include {', '.join(hobbies)}')

height = st.slider(label='Height (cm):', min_value=100,
                   max_value=250, value=170, step=1, )
if height:
    st.write(f'Your body height is {height} cm.')

st.divider()

uploaded_file = st.file_uploader(
    'Upload file', type=['pdf', 'txt', 'png', 'jpeg', 'py'])
if uploaded_file:
    st.write(f'The file you upload is {uploaded_file.name}')
    st.write(uploaded_file.read())


st.write('## Hello!')

with st.sidebar:
    name = st.text_input('please input your name.')
    if name:
        st.write(f'Welcome {name} ~')

column1, column2, column3 = st.columns([1, 2, 1])
with column1:
    password = st.text_input('please enter your password', type='password')

with column2:
    intro = st.text_area('Please introduce yourself:')

with column3:
    age = st.number_input('Please enter your age:', value=20,
                          min_value=0, max_value=150, step=1)
    st.write(f'You are {age} years old.')

st.divider()

is_agreed = st.checkbox('Agree')

is_submitted = st.button('Submit', type='primary')
if is_submitted:
    st.write('Submitted Successfully!')


tab1, tab2, tab3, tab4 = st.tabs(
    ['gender', 'qualification', 'contacts', 'hobbies'])

with tab1:
    gender = st.radio('Gender', options=[
                      'Male', 'Female', 'Not sure'], index=None)
    if gender:
        st.write(f'Your gender is {gender}')

with tab2:
    qualification = st.selectbox('Qualification', options=[
        'Doctor', 'Master', 'Bachelor', 'High school'], index=None)
    if qualification:
        st.write(f'You have a {qualification} degree.')

with tab3:
    contacts = st.multiselect(
        'Contact', options=['Email', 'Phone', 'Mobile', 'Text'])
    if contacts:
        st.write(f'We will contact you by {', '.join(contacts)}')

with tab4:
    hobbies = st.multiselect(
        'Hobby: ', options=['swim', 'basketball', 'piano', 'painting', 'hiking'])
    if hobbies:
        st.write(f'Your hobbies include {', '.join(hobbies)}')

with st.expander('Height'):
    height = st.slider(label='Height (cm):', min_value=100,
                       max_value=250, value=170, step=1, )
    if height:
        st.write(f'Your body height is {height} cm.')

uploaded_file = st.file_uploader(
    'Upload file', type=['pdf', 'txt', 'png', 'jpeg', 'py'])
if uploaded_file:
    st.write(f'The file you upload is {uploaded_file.name}')
    st.write(uploaded_file.read())


print('Start: ', st.session_state)

if 'num' not in st.session_state:
    st.session_state.num = 0
clicked = st.button('Plus 1')
if clicked:
    st.session_state.num += 1
st.write(st.session_state.num)

print('End: ', st.session_state)
