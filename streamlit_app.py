import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document

# Initialize Together client
client = Together(api_key="xxxxxx")

# Initialize session state for messages and uploaded document content
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
if "document_content" not in st.session_state:
    st.session_state.document_content = None
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

# Function to read PDF
def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        # Extract text and ensure paragraph separation
        page_text = page.extract_text()
        if page_text:
            text += page_text.strip() + "\n\n"  # Add extra line breaks
    return text

# Function to read Word document
def read_word(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Blank screen with file uploader if chat hasn't started
if not st.session_state.chat_started:
    st.write("### Start your chat by uploading a document or typing your query below.")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])

    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1].lower()
        try:
            if file_type == "pdf":
                st.session_state.document_content = read_pdf(uploaded_file)
            elif file_type == "docx":
                st.session_state.document_content = read_word(uploaded_file)
            st.success("Document uploaded successfully! You can now start chatting.")
            st.session_state.chat_started = True
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Display chat interface
if st.session_state.chat_started:
    if "document_content" in st.session_state and st.session_state.document_content:
        # Let AI know about the document content
        if len(st.session_state.messages) == 1:  # Add context only once
            st.session_state.messages.append(
                {"role": "system", "content": f"The user uploaded a document with the following content:\n{st.session_state.document_content}"}
            )
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    # Chat input
    if user_input := st.chat_input("Type your message..."):
        st.session_state.chat_started = True  # Ensure chat is marked as started
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
