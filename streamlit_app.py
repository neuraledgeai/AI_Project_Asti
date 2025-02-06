import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document

# Set page title and layout
st.set_page_config(
    page_title="Asti-M2",
    layout="wide",
)

# Initialize Together client
api_key = st.secrets["API_KEY"]
client = Together(api_key=api_key)

# Functions to extract text from files
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

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
if "document_content" not in st.session_state:
    st.session_state.document_content = None
#if "chat_started" not in st.session_state:
#    st.session_state.chat_started = False

with st.expander("Minimize", expanded=True):
    st.write("### Upload a document or start typing your question below.")
    uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])
    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()
        try:
            if file_type == "pdf":
                st.session_state.document_content = read_pdf(uploaded_file)
            elif file_type == "docx":
                st.session_state.document_content = read_word(uploaded_file)
                st.success("Document uploaded successfully! You can now start chatting.")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    

# Chat interface (always visible)
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add document context to the model's input if available
    if st.session_state.document_content:
        context_message = f"The user has uploaded a PDF or word document. Use the following context extracted as text to assist them:\n\n{st.session_state.document_content}\n\n"
    else:
        context_message = ""

    # Combine context and chat history for the model
    messages_with_context = [{"role": "system", "content": context_message}] + st.session_state.messages

    # Get AI response
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=messages_with_context,
    )
    ai_message = response.choices[0].message.content

    # Append AI response to the chat
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.markdown(ai_message)
