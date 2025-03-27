import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document
import re

# Set page title and layout
st.set_page_config(
    page_title="Asti-M1",
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

# Initialize Together client
api_key = st.secrets["API_KEY"]
client = Together(api_key=api_key)

# Model names
META_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
DEEPSEEK_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"

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
if "selected_model" not in st.session_state:
    st.session_state.selected_model = META_MODEL

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

    # Model switch using segmented control
    model_choice = st.segmented_control(
        "",
        options=["Default", "Reason"],
        format_func=lambda x: "Reason" if x == "Reason" else "Turbo Chat",
        default="Default"
    )
    st.session_state.selected_model = DEEPSEEK_MODEL if model_choice == "Reason" else META_MODEL

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
    messages_with_context = [{"role": "system", "content": context_message}] if context_message else []
    messages_with_context.extend(st.session_state.messages)

    # Placeholder for streaming response
    response_placeholder = st.empty()
    full_response = ""

    try:
        # Stream AI response
        stream = client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=messages_with_context,
            stream=True,
        )

        think_content = None
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                # Remove <think> part dynamically
                clean_response = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL).strip()
                response_placeholder.markdown(clean_response)  # Update single placeholder (Prevents auto-scrolling)

        # Extract "thinking" content if present
        think_match = re.search(r"<think>(.*?)</think>", full_response, re.DOTALL)
        if think_match:
            think_content = think_match.group(1).strip()

        # Append final AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": clean_response})
        response_placeholder.markdown(clean_response)  # Ensure final update

        # Show "thinking" process if it exists
        if think_content:
            with st.expander("🤔 Model's Thought Process"):
                st.markdown(think_content)

    except Exception as e:
        error_message = str(e)
        if "Input validation error" in error_message and "tokens" in error_message:
            st.warning("⚠️ Token limit reached for Reason mode. Please start a new chat to continue with Reason mode or switch to Default mode and continue here.")
