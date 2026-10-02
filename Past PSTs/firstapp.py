import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image


# Title
st.title("Hello, Streamlit!")
st.header("Header")
st.subheader("Subheader")
st.text("Plain text")


# Input
name = st.text_input("Enter your name: ")

# Button
if st.button("Greet"):
    st.write(f"Hello, {name}! Welcome to streamlit.")

st.checkbox("check me out !")
st.radio("choose one:", ["option A", "Option B"])
st.selectbox("pick a number:", [1,2,3])
st.slider("select a value", 0, 100)

chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

img = Image.open("my_image.jpeg")
st.image(img, caption="my image")
