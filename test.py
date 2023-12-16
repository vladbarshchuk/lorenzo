import streamlit as st
import pandas as pd

df= pd.read_csv(r"/Users/vladimirbarshchuk/Downloads/expense1.csv")

st.set_page_config(layout="centered", page_icon = "rocket")
st.title('Lets Find you a Developer')
st.title('Fill out the :red[form] below :sunglasses:')
with st.form("my_form"):
    st.text_input("What is your Name ?",placeholder="name")
    st.text_input("What's your email ?", placeholder="email")
    option = st.selectbox('Provide Your Industry',
    ('Real Estate', 'Financial Services', 'E-Commerce'))
    st.write('You selected:', option)
    submitted = st.form_submit_button(label="Submit Vendor Details")
    if submitted:
        st.write("submitted")

import streamlit as st

import streamlit as st

container = st.container()
col1, col2 = st.columns([1, 3])
with container:
    with col1:
        st.header(f":red[{df['Posted Date'][0]}]", anchor= False)
        st.image("https://static.streamlit.io/examples/cat.jpg")
        st.header("PAY: ", anchor= False)
        st.subheader(":grey[$20 per hour]")
        st.header("PROJECTS: ", anchor= False)
        st.subheader(":grey[390 delivered]")
        st.header("REVIEW :", anchor= False)
        st.subheader(":grey[96% SUCCESS RATE]")

    with col2:
        st.header("Description")
        st.write(f":red[{df['Payee'][0]}]")
st.table(df)







