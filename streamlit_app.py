import streamlit as st
from together import Together

client = Together(api_key="22c7d3723a5c143b4f1ac02fd15b5d0d5034629c91abe3281d2f1e029c2aa371")

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
)

st.title("Asti")
st.write(
    f"{response.choices[0].message.content}."
)
