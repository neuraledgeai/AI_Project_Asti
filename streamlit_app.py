import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document

# Initialize Together client
api_key = st.secrets["API_KEY"]
client = Together(api_key=api_key)

# Initialize session state variables
if "messages" not in st.session_state:
    # Only include messages we want to display (system messages used for context won't be shown)
    st.session_state.messages = []
if "document_content" not in st.session_state:
    st.session_state.document_content = None
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

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

# --- Top of the App: File Uploader (only if chat hasn't started) ---
if not st.session_state.chat_started:
    st.write("### Welcome! Start by uploading a document (PDF or Word) or type your query below.")
    uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        try:
            if file_type == "pdf":
                st.session_state.document_content = read_pdf(uploaded_file)
            elif file_type == "docx":
                st.session_state.document_content = read_word(uploaded_file)
            st.success("Document uploaded successfully! You can now start chatting.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# --- Chat Display: Show conversation history (only user & assistant messages) ---
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# --- Chat Input ---
user_input = st.chat_input("Type your message...")

if user_input:
    # Mark that chat has started so uploader is no longer shown
    st.session_state.chat_started = True

    # Append user's message to the conversation history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # If a document was uploaded, add a context message for the AI just once.
    # This system message will not be shown to the user.
    if st.session_state.document_content and not any(
        msg.get("role") == "system" and "uploaded document" in msg.get("content", "")
        for msg in st.session_state.messages
    ):
        context_message = {
            "role": "system",
            "content": "The user has uploaded a document. Use its content as context when answering questions."
        }
        st.session_state.messages.insert(0, context_message)

    # Get AI response
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=st.session_state.messages,
    )
    ai_message = response.choices[0].message.content

    # Append AI response to conversation history and display it
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.markdown(ai_message)
