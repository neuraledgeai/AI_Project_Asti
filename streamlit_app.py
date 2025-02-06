import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document

api_key = st.secrets["API_KEY"]
client = Together(api_key=api_key)

idle = 0

if idle==0:
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

    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()
        
        if file_type == "pdf":
            try:
                text = read_pdf(uploaded_file)
                #st.subheader("Extracted Text from PDF:")
                #st.text_area("PDF Content", text, height=300)
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
        
        elif file_type == "docx":
            try:
                text = read_word(uploaded_file)
                #st.subheader("Extracted Text from Word Document:")
                #st.text_area("Word Content", text, height=300)
            except Exception as e:
                st.error(f"Error reading Word document: {e}")
        
        else:
            st.error("Unsupported file type! Please upload a PDF or Word document.")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Chat input for user
if user_input := st.chat_input("Type your message..."):
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
    idle == 1
    with st.chat_message("assistant"):
        st.markdown(ai_message)
