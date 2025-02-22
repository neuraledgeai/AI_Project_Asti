import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document

# Set page title and layout
st.set_page_config(page_title="Asti-M1", layout="wide")

# Initialize Together client
api_key = st.secrets["API_KEY"]
client = Together(api_key=api_key)

# Model options
DEEPSEEK_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"
META_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo"

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_content" not in st.session_state:
    st.session_state.document_content = None

# Model selector using segmented control
#model_choice = st.segmented_control("Choose mode:", ["Reason"])
#st.session_state.selected_model = DEEPSEEK_MODEL if model_choice == "Reason" else META_MODEL

# Functions to extract text from files
def read_pdf(file):
    pdf_reader = PdfReader(file)
    return "".join(page.extract_text() or "" for page in pdf_reader.pages)

def read_word(file):
    doc = Document(file)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

# File uploader and document processing
with st.expander("Minimize", expanded=True):
    st.write("### Upload a document or start typing your question below.")
    uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".pdf"):
                st.session_state.document_content = read_pdf(uploaded_file)
            else:
                st.session_state.document_content = read_word(uploaded_file)
            st.success("Document uploaded successfully! You can now start chatting.")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    # Model selector using segmented control
    model_choice = st.segmented_control("Choose mode:", ["Reason"])
    st.session_state.selected_model = DEEPSEEK_MODEL if model_choice == "Reason" else META_MODEL

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add document context if available
    context_message = (
        f"The user uploaded a document. Context:\n\n{st.session_state.document_content}\n\n"
        if st.session_state.document_content else ""
    )

    # Combine context and chat history
    messages_with_context = [{"role": "system", "content": context_message}] if context_message else []
    messages_with_context.extend(st.session_state.messages)

    try:
        # Generate AI response
        response = client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=messages_with_context,
            max_tokens=1000,  # Keep output reasonable
        )
        ai_message = response.choices[0].message.content
    
        # Separate <think> part from the main response
        think_pattern = re.compile(r"<think>(.*?)</think>", re.DOTALL)
        think_match = think_pattern.search(ai_message)
        think_content = think_match.group(1).strip() if think_match else None
        clean_response = think_pattern.sub("", ai_message).strip()
    
        # Append and display AI response
        st.session_state.messages.append({"role": "assistant", "content": clean_response})
        with st.chat_message("assistant"):
            st.markdown(clean_response)
    
            # Show "thinking" part in an expander if it exists
            if think_content:
                with st.expander("🤔 Model's Thought Process (Click to view)"):
                    st.markdown(think_content)
    
    except Exception as e:
        error_message = str(e)
        if "Input validation error" in error_message and "tokens" in error_message:
            st.warning(
                "⚠️ Token limit reached for Reason mode. Please start a new chat to continue with Reason mode "
                "or switch to Default mode and continue here."
            )
