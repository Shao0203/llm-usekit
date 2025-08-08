import streamlit as st

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
