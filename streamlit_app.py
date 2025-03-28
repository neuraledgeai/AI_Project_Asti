import streamlit as st
from together import Together
from PyPDF2 import PdfReader
from docx import Document
from serpapi import GoogleSearch

# Set page title and layout
st.set_page_config(
    page_title="Asti-M1",
    layout="wide",
    page_icon="🌟"
)

# Sidebar navigation
st.sidebar.page_link("streamlit_app.py", label="Chat", icon="💬")

# Initialize Together client
api_key = st.secrets["API_KEY"]
client = Together(api_key=api_key)
serp_api_key = st.secrets["SERP_API_KEY"]

# Model names
META_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
DEEPSEEK_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"

# Function to fetch web search snippets
def fetch_snippets(query, api_key):
    params = {"engine": "google", "q": query, "api_key": api_key}
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    snippets_with_sources = []
    
    for i in organic_results:
        snippet = i.get("snippet", "")
        source = i.get("source", "Unknown Source")
        link = i.get("link", "#")
        
        if snippet:
            linked_source = f"[{source}]({link})"
            snippets_with_sources.append(f"{snippet} ({linked_source})")

    return " ".join(snippets_with_sources) if snippets_with_sources else "No relevant information found."

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
    options=["Default", "Reason", "Web Search"],
    format_func=lambda x: "Reason" if x == "Reason" else "Web Search" if x == "Web Search" else "Turbo Chat",
    default="Default"
)
st.session_state.selected_model = (
    DEEPSEEK_MODEL if model_choice == "Reason" else META_MODEL if model_choice == "Web Search" else META_MODEL
)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

placeholder = "Type your search query..." if model_choice == "Web Search" else "Type your message..."

# Chat input and streaming response  
if user_input := st.chat_input(placeholder):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response_placeholder = st.empty()
    full_response = ""

    if model_choice == "Web Search":
        # **Step 1: Ask Model If a Search is Required**
        decision_prompt = (
            f"User has turned on Web Search mode and asked: '{user_input}'. "
            "Analyze whether this requires an internet search. "
            "If yes, reply with 'YES'. If not, reply with 'NO'. No other words or sentences, only YES or NO."
        )
        
        decision_response = client.chat.completions.create(
            model=META_MODEL,
            messages=[{"role": "system", "content": decision_prompt}]
        )
        
        decision_text = decision_response.choices[0].message.content.strip().upper()

        if decision_text == "YES":
            # **Step 2: Generate a Proper Search Query**
            refine_prompt = f"User's request: {user_input}. Please make a one sentence search terms it should be concise, provide only it, no other sentences or words."
            refine_response = client.chat.completions.create(
                model=META_MODEL,
                messages=[{"role": "system", "content": refine_prompt}]
            )
            
            search_query = refine_response.choices[0].message.content.strip()
            search_results = fetch_snippets(search_query, serp_api_key)
            
            # **Step 3: Generate the Final Response**
            final_prompt = f"User asked: {user_input}. Search Results: {search_results}. Provide a clear response using bold and linked texts."
            stream = client.chat.completions.create(
                model=META_MODEL,
                messages=[{"role": "system", "content": final_prompt}],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            # **Generate a normal AI response (no web search)**
            normal_prompt = f"User: {user_input}. Respond naturally without searching the web."
            normal_response = client.chat.completions.create(
                model=META_MODEL,
                messages=[{"role": "system", "content": normal_prompt}],
                stream=True,
            )

            for chunk in normal_response:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

    else:
        # **Turbo Chat & Reason Modes (No Web Search Logic)**
        messages_with_context = [{"role": "system", "content": st.session_state.document_content}] if st.session_state.document_content else []
        messages_with_context.extend(st.session_state.messages)
        
        try:
            stream = client.chat.completions.create(
                model=st.session_state.selected_model,
                messages=messages_with_context,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_message = str(e)
            if "Input validation error" in error_message and "tokens" in error_message:
                st.warning("⚠️ Too much text, token limit reached. Start a new chat to continue.")
