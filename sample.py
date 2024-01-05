import streamlit as st
import pandas as pd


st.title("Welcome!")
st.divider()
name=st.text_input("Please Enter your name")
year=st.date_input("Please select Date")
code=st.text_input("code")

if(name):
    st.caption(f" Hello {name}, **Welcome**!")

st.caption("Read CSV data")
data=pd.read_csv("user_listt.csv")
st.write(data)






