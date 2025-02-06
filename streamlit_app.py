import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document

api_key = st.secrets["API_KEY"]
client = Together(api_key=api_key)

# Initialize idle based on whether there are messages (chat started)
if "messages" not in st.session_state or not st.session_state.messages:
    idle = True
else:
    idle = False

# Functions to read files (same as before)
def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text.strip() + "\n\n"
    return text

def read_word(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


if idle:  # Show file uploader only if idle
    uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()
        if file_type == "pdf":
            try:
                text = read_pdf(uploaded_file)
                st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant. Here is the context from the uploaded PDF:\n\n" + text}] # Include extracted text as context
                idle = False # Set idle to False after file upload
                #st.experimental_rerun() # Rerun to hide the uploader and show the chat
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
        elif file_type == "docx":
            try:
                text = read_word(uploaded_file)
                st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant. Here is the context from the uploaded Word document:\n\n" + text}] # Include extracted text as context
                idle = False # Set idle to False after file upload
                #st.experimental_rerun() # Rerun to hide the uploader and show the chat
            except Exception as e:
                st.error(f"Error reading Word document: {e}")
        else:
            st.error("Unsupported file type! Please upload a PDF or Word document.")

# Chat logic (same as before, but now always displayed)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=st.session_state.messages,
    )

    ai_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.markdown(ai_message)
