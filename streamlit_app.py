import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document

# Set page title and layout
st.set_page_config(
    page_title="Asti-M1",
    layout="wide",
)

# Initialize Together client
api_key = st.secrets["API_KEY"]
client = Together(api_key=api_key)

# Model options
model_options = {
    "DeepSeek (Reasoning Model)": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    "Meta LLaMA 3.3 (Instruct Turbo)": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
}

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
if "document_content" not in st.session_state:
    st.session_state.document_content = None
if "selected_model" not in st.session_state:
    st.session_state.selected_model = list(model_options.values())[0]  # Default model

# Model selector
with st.sidebar:
    st.write("## Model Selection")
    selected_model_name = st.selectbox(
        "Choose the AI model for this chat:",
        list(model_options.keys()),
        index=list(model_options.values()).index(st.session_state.selected_model)
    )
    st.session_state.selected_model = model_options[selected_model_name]

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

# File uploader and document processing
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

# Display chat messages
for message in st.session_state.messages:
    role = message["role"]
    with st.chat_message(role):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add document context if available
    if st.session_state.document_content:
        context_message = f"The user has uploaded a document. Use the following context to assist them:\n\n{st.session_state.document_content}\n\n"
    else:
        context_message = ""

    # Combine context and chat history
    messages_with_context = [{"role": "system", "content": context_message}] + st.session_state.messages

    # Get AI response using the selected model
    response = client.chat.completions.create(
        model=st.session_state.selected_model,
        messages=messages_with_context,
    )
    ai_message = response.choices[0].message.content

    # Append and display AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.markdown(ai_message)
