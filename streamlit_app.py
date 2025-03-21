import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document
import re

# Initialize the app
def initialize_app():
    st.set_page_config(
        page_title="Asti-M1",
        layout="wide",
        page_icon="🌟"
    )

# Create the sidebar
def create_sidebar():
    st.sidebar.page_link("streamlit_app.py", label="Chat", icon="💬")
    with st.sidebar.expander("Legal and Support"):
        st.page_link("pages/Terms_&_Conditions.py", label="Terms & Conditions", icon="📜")
        st.page_link("pages/Privacy_Policy.py", label="Privacy policy", icon="🛡️")
        st.page_link("pages/About_Us.py", label="About Us", icon="ℹ️")
        st.page_link("pages/Refund_policy.py", label="Refund policy", icon="🔄")
        st.page_link("pages/Contact_Us.py", label="Contact Us", icon="📞")

# Initialize the Together client
def initialize_together_client():
    api_key = st.secrets["API_KEY"]
    client = Together(api_key=api_key)
    return client

# Read a PDF file
def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = "\n\n".join(page.extract_text().strip() for page in pdf_reader.pages if page.extract_text())
    return text

# Read a Word file
def read_word(file):
    doc = Document(file)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

# Handle file upload
def handle_file_upload():
    uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".pdf"):
                return read_pdf(uploaded_file)
            elif uploaded_file.name.endswith(".docx"):
                return read_word(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Handle chat input and response
def handle_chat_input(client, document_content, selected_model):
    user_input = st.chat_input("Type your message...")
    if user_input:
        messages = [{"role": "user", "content": user_input}]
        if document_content:
            messages.insert(0, {"role": "system", "content": f"The user uploaded a document. Context:\n\n{document_content}\n\n"})
        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=messages,
                stream=True,
            )
            full_response = ""
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    clean_response = re.sub(r"", "", full_response, flags=re.DOTALL).strip()
                    st.markdown(clean_response)
            think_match = re.search(r"", full_response, re.DOTALL)
            if think_match:
                with st.expander("🤔 Model's Thought Process"):
                    st.markdown(think_match.group(1).strip())
        except Exception as e:
            st.error(f"Error: {e}")

# Main function
def main():
    initialize_app()
    create_sidebar()
    client = initialize_together_client()
    document_content = None
    selected_model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
    with st.expander("📄 Upload a Document (Optional)", expanded=True):
        uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".pdf"):
                    document_content = read_pdf(uploaded_file)
                elif uploaded_file.name.endswith(".docx"):
                    document_content = read_word(uploaded_file)
                st.success("✅ Document uploaded successfully! You can now start chatting.")
            except Exception as e:
                st.error(f"Error reading file: {e}")
        model_choice = st.segmented_control(
            "",
            options=["Default", "Reason"],
            format_func=lambda x: "Reason" if x == "Reason" else "Turbo Chat",
            default="Default"
        )
        if model_choice == "Reason":
            selected_model = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"
    handle_chat_input(client, document_content, selected_model)

if __name__ == "__main__":
    main()
