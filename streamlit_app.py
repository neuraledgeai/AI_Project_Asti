import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader
from docx import Document
import re

# Set page title and layout
st.set_page_config(
    page_title="Asti-M1hh",
    layout="wide",
    page_icon="🌟"
)

# Sidebar navigation
st.sidebar.page_link("streamlit_app.py", label="Chat", icon="💬")
with st.sidebar.expander("Legal and Support"):
    st.page_link("pages/Terms_&_Conditions.py", label="Terms & Conditions", icon="📜")
    st.page_link("pages/Privacy_Policy.py", label="Privacy policy", icon="🛡️")
    st.page_link("pages/About_Us.py", label="About Us", icon="ℹ️")
    st.page_link("pages/Refund_policy.py", label="Refund policy", icon="🔄")
    st.page_link("pages/Contact_Us.py", label="Contact Us", icon="📞")

# Load Hugging Face model
pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-V3-0324", trust_remote_code=True)

# Functions to extract text from files
def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = "\n\n".join(page.extract_text().strip() for page in pdf_reader.pages if page.extract_text())
    return text

def read_word(file):
    doc = Document(file)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_content" not in st.session_state:
    st.session_state.document_content = None

# File upload section
with st.expander("📄 Upload a Document (Optional)", expanded=True):
    uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".pdf"):
                st.session_state.document_content = read_pdf(uploaded_file)
            elif uploaded_file.name.endswith(".docx"):
                st.session_state.document_content = read_word(uploaded_file)
            st.success("✅ Document uploaded successfully! You can now start chatting.")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and streaming response
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add document context if available
    context_message = f"The user uploaded a document. Context:\n\n{st.session_state.document_content}\n\n" if st.session_state.document_content else ""
    messages_with_context = context_message + user_input

    # Placeholder for streaming response
    response_placeholder = st.empty()
    full_response = ""
    
    try:
        # Stream AI response
        response_generator = pipe(messages_with_context, max_new_tokens=512, do_sample=True)
        for chunk in response_generator:
            full_response += chunk["generated_text"]
            clean_response = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL).strip()
            response_placeholder.markdown(clean_response)

        # Append final AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": clean_response})
        response_placeholder.markdown(clean_response)
    
    except Exception as e:
        st.error(f"❌ Error generating response: {e}")
