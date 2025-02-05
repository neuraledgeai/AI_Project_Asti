import streamlit as st
from together import Together

# Set page title and layout
st.set_page_config(
    page_title="AI Project Asti",
    layout="wide",
)


client = Together(api_key="22c7d3723a5c143b4f1ac02fd15b5d0d5034629c91abe3281d2f1e029c2aa371")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Chat input for user
if user_input := st.chat_input("Type your message..."):
    # Add user's message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

# Get AI response
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=st.session_state.messages,
    )

# Extract and display AI response
    ai_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.markdown(ai_message)

#response = client.chat.completions.create(
#    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
#    messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
#)

#st.title("Asti")
#st.write(
#    f"{response.choices[0].message.content}."
#)
