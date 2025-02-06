import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document

api_key = st.secrets["API_KEY"]
client = Together(api_key=api_key)

# ... (file reading functions remain the same)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant.  I will provide context from uploaded files."}]

if "file_context" not in st.session_state: # Store file context separately
    st.session_state.file_context = ""

if not st.session_state.messages or len(st.session_state.messages) == 1: # Check if only the initial system message is present
    idle = True
else:
    idle = False


if idle:
    uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()
        if file_type == "pdf":
            try:
                text = read_pdf(uploaded_file)
                st.session_state.file_context = text  # Store in file_context
                st.session_state.messages[0]["content"] = "You are a helpful assistant. Here is the context from the uploaded PDF:\n\n" + text #Update system message with context
                idle = False
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
        elif file_type == "docx":
            try:
                text = read_word(uploaded_file)
                st.session_state.file_context = text  # Store in file_context
                st.session_state.messages[0]["content"] = "You are a helpful assistant. Here is the context from the uploaded Word document:\n\n" + text #Update system message with context
                idle = False
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error reading Word document: {e}")
        else:
            st.error("Unsupported file type!")

# ... (chat display remains the same)

if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add file context to the messages sent to the model
    messages_for_model = st.session_state.messages[:]  # Create a copy
    # No need to explicitly add context here, it is already in the system message.

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=messages_for_model,
    )

    ai_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.markdown(ai_message)
