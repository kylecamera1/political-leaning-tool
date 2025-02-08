import streamlit as st

st.title("Political Leaning Detector")
st.write("This is a test app!")

user_input = st.text_input("Enter a name or company")
if user_input:
    st.write(f"You searched for: {user_input}")
