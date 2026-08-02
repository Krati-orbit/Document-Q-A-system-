"""
Document Q&A System powered by Streamlit, PyPDF, and Google Gemini API.

Features:
- Vibrant, modern custom CSS theme (Electric Violet & Emerald accents).
- Multi-document session memory (stores uploaded PDFs across sessions).
- Conversational chat interface with multi-turn memory recall.
- Hidden API key handling (key is never exposed on UI if loaded from .env).
- Strict RAG grounding with conversational history context.
"""

import io
import os
from typing import Dict, List, Optional
import streamlit as st
import pypdf
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# ==============================================================================
# UI Styling: Multi-Theme Dynamic Engine
# ==============================================================================

THEMES = {
    "Cyber Obsidian 🌌 (Dark Mode)": {
        "bg_color": "#000000",
        "sidebar_bg": "#09090B",
        "sidebar_border": "#27272A",
        "text_color": "#FFFFFF",
        "sub_text": "#A1A1AA",
        "header_gradient": "linear-gradient(135deg, #00F2FE 0%, #4FACFE 40%, #00FF87 100%)",
        "primary_btn_bg": "linear-gradient(135deg, #00F2FE 0%, #00FF87 100%)",
        "primary_btn_text": "#000000",
        "badge_bg": "rgba(0, 242, 254, 0.15)",
        "badge_border": "#00F2FE",
        "badge_text": "#00F2FE",
        "chat_input_border": "#00F2FE",
        "expander_bg": "#121216",
        "expander_text": "#00F2FE",
        "card_bg": "#121216",
        "card_border": "#27272A",
        "input_bg": "#18181C",
        "input_text": "#FFFFFF",
        "input_border": "#3F3F46"
    },
    "Emerald Mint Luxe 🌿": {
        "bg_color": "#F0FDF4",
        "sidebar_bg": "#E6F4EA",
        "sidebar_border": "#A7F3D0",
        "text_color": "#064E3B",
        "sub_text": "#047857",
        "header_gradient": "linear-gradient(135deg, #059669 0%, #10B981 50%, #34D399 100%)",
        "primary_btn_bg": "linear-gradient(135deg, #059669 0%, #10B981 100%)",
        "primary_btn_text": "#FFFFFF",
        "badge_bg": "#DCFCE7",
        "badge_border": "#6EE7B7",
        "badge_text": "#065F46",
        "chat_input_border": "#10B981",
        "expander_bg": "#E6F4EA",
        "expander_text": "#065F46",
        "card_bg": "#FFFFFF",
        "card_border": "#A7F3D0",
        "input_bg": "#FFFFFF",
        "input_text": "#064E3B",
        "input_border": "#6EE7B7"
    },
    "Arctic Teal & Frost ❄️": {
        "bg_color": "#F8FAFC",
        "sidebar_bg": "#F1F5F9",
        "sidebar_border": "#CBD5E1",
        "text_color": "#0F172A",
        "sub_text": "#334155",
        "header_gradient": "linear-gradient(135deg, #0EA5E9 0%, #2563EB 50%, #6366F1 100%)",
        "primary_btn_bg": "linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%)",
        "primary_btn_text": "#FFFFFF",
        "badge_bg": "#E0F2FE",
        "badge_border": "#93C5FD",
        "badge_text": "#1E40AF",
        "chat_input_border": "#0EA5E9",
        "expander_bg": "#F1F5F9",
        "expander_text": "#1E40AF",
        "card_bg": "#FFFFFF",
        "card_border": "#CBD5E1",
        "input_bg": "#FFFFFF",
        "input_text": "#0F172A",
        "input_border": "#94A3B8"
    },
    "Warm Sunset & Amber 🌅": {
        "bg_color": "#FAF7F2",
        "sidebar_bg": "#F5EFE6",
        "sidebar_border": "#FED7AA",
        "text_color": "#451A03",
        "sub_text": "#78350F",
        "header_gradient": "linear-gradient(135deg, #D97706 0%, #EA580C 50%, #E11D48 100%)",
        "primary_btn_bg": "linear-gradient(135deg, #D97706 0%, #EA580C 100%)",
        "primary_btn_text": "#FFFFFF",
        "badge_bg": "#FEF3C7",
        "badge_border": "#FDE68A",
        "badge_text": "#92400E",
        "chat_input_border": "#D97706",
        "expander_bg": "#F5EFE6",
        "expander_text": "#78350F",
        "card_bg": "#FFFFFF",
        "card_border": "#FDBA74",
        "input_bg": "#FFFFFF",
        "input_text": "#451A03",
        "input_border": "#FDBA74"
    }
}


def apply_custom_theme(theme_name: str = "Emerald Mint Luxe 🌿"):
    """Injects high-end, modern CSS styling tailored dynamically to the selected theme with strict text visibility rules."""
    t = THEMES.get(theme_name, THEMES["Emerald Mint Luxe 🌿"])
    
    st.markdown(
        f"""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* Set CSS variables dynamically */
        :root, [data-testid="stAppViewContainer"], .stApp {{
            --text-color: {t['text_color']} !important;
            --background-color: {t['bg_color']} !important;
            --secondary-background-color: {t['sidebar_bg']} !important;
        }}

        /* Base App Container, Header & Main Container Background Fix */
        html, body, [data-testid="stAppViewContainer"], .stApp,
        header[data-testid="stHeader"], section.main, [data-testid="stMain"],
        .block-container, [data-testid="stBottom"], [data-testid="stBottom"] > div,
        [data-testid="stVerticalBlock"] {{
            background-color: {t['bg_color']} !important;
            color: {t['text_color']} !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        header[data-testid="stHeader"] {{
            background-color: transparent !important;
        }}

        /* Universal Text Color Overrides for High Visibility */
        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] span,
        [data-testid="stAppViewContainer"] label,
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] h4,
        [data-testid="stAppViewContainer"] h5,
        [data-testid="stAppViewContainer"] h6,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] strong,
        .stSelectbox label, .stTextInput label, .stFileUploader label {{
            color: {t['text_color']} !important;
        }}

        /* Header styling */
        .main-title {{
            font-size: 2.4rem;
            font-weight: 800;
            background: {t['header_gradient']};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
            letter-spacing: -0.02em;
        }}
        
        .sub-subtitle {{
            color: {t['sub_text']} !important;
            font-size: 1.05rem;
            font-weight: 500;
            margin-bottom: 1.8rem;
        }}

        .stCaption, [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {{
            color: {t['sub_text']} !important;
        }}

        /* Sidebar Styling & Text */
        section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {{
            background-color: {t['sidebar_bg']} !important;
            border-right: 1px solid {t['sidebar_border']} !important;
        }}

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: {t['text_color']} !important;
        }}

        /* Inputs, Selectboxes, Dropdowns & Textareas */
        input, textarea, div[data-baseweb="select"] > div, div[data-baseweb="input"] {{
            background-color: {t['input_bg']} !important;
            color: {t['input_text']} !important;
            border-color: {t['input_border']} !important;
        }}

        div[data-baseweb="select"] span, div[data-baseweb="select"] div {{
            color: {t['input_text']} !important;
        }}

        ul[data-baseweb="menu"], ul[data-baseweb="menu"] li, div[data-baseweb="popover"] * {{
            background-color: {t['sidebar_bg']} !important;
            color: {t['text_color']} !important;
        }}

        /* File Uploader Box Fix */
        [data-testid="stFileUploader"] section,
        section[data-testid="stFileUploaderDropzone"] {{
            background-color: {t['input_bg']} !important;
            border: 1.5px dashed {t['input_border']} !important;
            border-radius: 12px !important;
        }}

        [data-testid="stFileUploader"] section p,
        [data-testid="stFileUploader"] section span,
        [data-testid="stFileUploader"] section small,
        section[data-testid="stFileUploaderDropzone"] p,
        section[data-testid="stFileUploaderDropzone"] span,
        section[data-testid="stFileUploaderDropzone"] small {{
            color: {t['text_color']} !important;
        }}

        /* Upload / Browse Files Button Fix (Black text on white button) */
        [data-testid="stFileUploader"] button,
        [data-testid="stFileUploaderDropzone"] button,
        section[data-testid="stFileUploaderDropzone"] button,
        button[data-testid="baseButton-secondary"] {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid #CBD5E1 !important;
            font-weight: 700 !important;
        }}

        [data-testid="stFileUploader"] button *,
        [data-testid="stFileUploaderDropzone"] button *,
        section[data-testid="stFileUploaderDropzone"] button *,
        button[data-testid="baseButton-secondary"] * {{
            color: #000000 !important;
            fill: #000000 !important;
            stroke: #000000 !important;
        }}

        /* Chat Input Bar Fix */
        [data-testid="stBottom"] {{
            background-color: {t['bg_color']} !important;
        }}

        [data-testid="stChatInput"], .stChatInputContainer {{
            background-color: {t['card_bg']} !important;
            border: 1.5px solid {t['chat_input_border']} !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        }}

        [data-testid="stChatInput"] textarea, .stChatInputContainer textarea {{
            background-color: transparent !important;
            color: {t['text_color']} !important;
            font-size: 1rem !important;
        }}

        [data-testid="stChatInput"] textarea::placeholder, .stChatInputContainer textarea::placeholder {{
            color: {t['sub_text']} !important;
            opacity: 0.8 !important;
        }}

        /* Custom Card / Badge Containers */
        .metric-badge {{
            background: {t['badge_bg']} !important;
            border: 1px solid {t['badge_border']} !important;
            border-radius: 10px;
            padding: 8px 14px;
            color: {t['badge_text']} !important;
            font-weight: 700;
            font-size: 0.88rem;
            display: inline-block;
            margin-bottom: 10px;
        }}

        /* Primary Button Styling */
        div.stButton > button[kind="primary"] {{
            background: {t['primary_btn_bg']} !important;
            border: none !important;
            color: {t['primary_btn_text']} !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 14px rgba(0, 242, 254, 0.3) !important;
            transition: all 0.2s ease-in-out !important;
        }}

        div.stButton > button[kind="primary"]:hover {{
            transform: translateY(-2px) !important;
            filter: brightness(1.15);
        }}

        /* Chat Message Cards & Content */
        [data-testid="stChatMessage"] {{
            background-color: {t['card_bg']} !important;
            border: 1px solid {t['card_border']} !important;
            border-radius: 14px !important;
            margin-bottom: 10px;
        }}

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {{
            color: {t['text_color']} !important;
        }}

        /* Expander Styling */
        .streamlit-expanderHeader {{
            background-color: {t['expander_bg']} !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            color: {t['expander_text']} !important;
        }}

        .streamlit-expanderHeader * {{
            color: {t['expander_text']} !important;
        }}

        .streamlit-expanderContent {{
            background-color: {t['card_bg']} !important;
            border: 1px solid {t['card_border']} !important;
            border-radius: 0 0 10px 10px !important;
        }}

        /* Custom Alert Cards */
        .stSuccess, .stInfo {{
            border-radius: 12px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )






# ==============================================================================
# Helper Functions: PDF Processing & GenAI Execution
# ==============================================================================

def extract_text_from_pdf(uploaded_file: io.BytesIO) -> str:
    """
    Extracts text content from all pages of an uploaded PDF file safely using pypdf.

    Args:
        uploaded_file (io.BytesIO): The uploaded PDF file buffer.

    Returns:
        str: Accumulated text content from all pages.

    Raises:
        ValueError: If no readable text is found in the PDF.
        Exception: For errors encountered during PDF parsing.
    """
    try:
        reader = pypdf.PdfReader(uploaded_file)
        extracted_text = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

        full_text = "\n\n".join(extracted_text).strip()

        if not full_text:
            raise ValueError(
                "No readable text could be extracted from this PDF. "
                "The document might be scanned (image-only), empty, or password-protected."
            )

        return full_text

    except pypdf.errors.PdfReadError as e:
        raise Exception(f"Failed to read PDF file structure: {str(e)}") from e
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Unexpected error while processing PDF: {str(e)}") from e


def generate_rag_response(
    api_key: str,
    context_text: str,
    chat_history: List[Dict[str, str]],
    user_query: str,
    model_name: str = "gemini-3.6-flash"
) -> str:
    """
    Queries Google Gemini API using a strict RAG system prompt with conversation history context.

    Args:
        api_key (str): Google Gemini API Key.
        context_text (str): Combined text content from uploaded document(s).
        chat_history (List[Dict[str, str]]): List of previous messages in session.
        user_query (str): The latest user question.
        model_name (str, optional): Gemini model to use. Defaults to "gemini-3.6-flash".

    Returns:
        str: Grounded response generated by Gemini.
    """
    if not api_key:
        raise ValueError("Google Gemini API Key is missing. Please configure it in .env or sidebar.")
    if not context_text:
        raise ValueError("No document content found in repository. Please upload a PDF first.")
    if not user_query:
        raise ValueError("User question is empty.")

    # Configure Gemini API key securely
    genai.configure(api_key=api_key)

    # Format previous conversation turns (includes up to last 12 messages for full context memory)
    history_str = ""
    if chat_history:
        recent_history = chat_history[-12:]
        history_lines = [f"{msg['role'].capitalize()}: {msg['content']}" for msg in recent_history]
        history_str = "\n".join(history_lines)

    # RAG System Prompt Design
    system_prompt = (
        "You are an expert Document Q&A AI agent adhering strictly to Retrieval-Augmented Generation (RAG) principles.\n"
        "Your task is to answer user questions accurately based ONLY on the provided Document Context below.\n\n"
        "STRICT CONSTRAINTS:\n"
        "1. Answer ONLY using the facts directly mentioned in the Document Context.\n"
        "2. Do NOT use external knowledge, extrapolate beyond the text, or assume unmentioned facts.\n"
        "3. If the answer cannot be found or deduced directly from the context, state clearly: "
        "\"I cannot find the answer to this question in the provided document(s).\"\n"
        "4. You have access to the CONVERSATION HISTORY below. Use it to resolve pronouns, references to previous questions, "
        "and follow-up requests (e.g., 'What was my first question?', 'Explain your previous answer in more detail'). "
        "Always keep factual assertions grounded strictly in the Document Context.\n"
        "5. Keep your answers factual, structured, and professional.\n\n"
        "--- DOCUMENT CONTEXT ---\n"
        f"{context_text}\n"
        "--- END OF DOCUMENT CONTEXT ---\n\n"
    )

    if history_str:
        system_prompt += f"--- CONVERSATION HISTORY ---\n{history_str}\n--- END OF CONVERSATION HISTORY ---\n\n"

    full_prompt = f"{system_prompt}User Question: {user_query}\nAnswer:"

    try:
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content(full_prompt)

        if response and response.text:
            return response.text.strip()
        else:
            return "No response was generated by the model. Please check your query and try again."

    except GoogleAPIError as e:
        raise GoogleAPIError(f"Gemini API Error: {str(e)}") from e
    except Exception as e:
        raise Exception(f"Failed to generate answer: {str(e)}") from e


# ==============================================================================
# Streamlit UI Rendering
# ==============================================================================

def main():
    st.set_page_config(
        page_title="Document Q&A Agent",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize Session State Variables
    if "documents" not in st.session_state:
        st.session_state.documents = {}  # {filename: extracted_text}
    if "messages" not in st.session_state:
        st.session_state.messages = []  # [{"role": "user"/"assistant", "content": "..."}]
    if "selected_theme" not in st.session_state:
        st.session_state.selected_theme = "Emerald Mint Luxe 🌿"

    # Inject Active Custom Theme
    apply_custom_theme(st.session_state.selected_theme)

    # Header section with custom CSS classes
    st.markdown('<div class="main-title">✨ Conversational Document Q&A Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-subtitle">Upload your PDF documents into memory and chat naturally with your AI Agent.</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------------------------
    # Sidebar: Security, Document Repository & Settings
    # --------------------------------------------------------------------------
    with st.sidebar:
        # 0. Visual Theme Customization Selector
        st.header("🎨 Visual Theme")
        chosen_theme = st.selectbox(
            "Interface Style Preset",
            options=list(THEMES.keys()),
            index=list(THEMES.keys()).index(st.session_state.selected_theme),
            help="Switch between distinct modern aesthetic presets instantly."
        )
        if chosen_theme != st.session_state.selected_theme:
            st.session_state.selected_theme = chosen_theme
            st.rerun()

        st.divider()

        st.header("⚙️ Security & Model")

        # 1. API Key Handling (Hidden Security)
        env_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        
        if env_api_key:
            st.success("🔒 API Key: Loaded securely from `.env` environment.")
            effective_api_key = env_api_key
        else:
            st.warning("⚠️ `.env` key not found. Enter API key below:")
            manual_api_key = st.text_input(
                "Google Gemini API Key",
                type="password",
                placeholder="AIzaSy...",
                help="Your API key will remain encrypted and hidden in session memory."
            )
            effective_api_key = manual_api_key

        selected_model = st.selectbox(
            "Gemini AI Model",
            options=["gemini-3.6-flash", "gemini-flash-latest", "gemini-2.5-pro", "gemini-2.0-flash"],
            index=0,
            help="Select the Gemini AI model to use."
        )

        st.divider()

        # 2. Document Upload & Repository Management
        st.header("📂 Document Memory")
        uploaded_files = st.file_uploader(
            "Upload PDF document(s)",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload one or multiple PDFs into session memory."
        )

        if uploaded_files:
            for file in uploaded_files:
                if file.name not in st.session_state.documents:
                    with st.spinner(f"Extracting text from '{file.name}'..."):
                        try:
                            text = extract_text_from_pdf(file)
                            st.session_state.documents[file.name] = text
                            st.toast(f"Added '{file.name}' to memory!", icon="✨")
                        except Exception as e:
                            st.error(f"Error reading '{file.name}': {str(e)}")

        # Display Document Repository List
        if st.session_state.documents:
            st.markdown(
                f'<div class="metric-badge">📚 Saved Documents: {len(st.session_state.documents)}</div>',
                unsafe_allow_html=True
            )
            for doc_name, doc_text in list(st.session_state.documents.items()):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.caption(f"📄 **{doc_name}** ({len(doc_text.split())} words)")
                with col2:
                    if st.button("🗑️", key=f"del_{doc_name}", help=f"Remove {doc_name}"):
                        del st.session_state.documents[doc_name]
                        st.rerun()

            doc_scope = st.selectbox(
                "Active Query Scope",
                options=["All Documents (Combined)"] + list(st.session_state.documents.keys()),
                index=0,
                help="Choose whether to query across all uploaded documents or a specific file."
            )

            if st.button("🧹 Clear All Documents", use_container_width=True):
                st.session_state.documents = {}
                st.session_state.messages = []
                st.rerun()
        else:
            doc_scope = "All Documents (Combined)"
            st.info("💡 No documents uploaded yet. Upload a PDF above to get started.")

        st.divider()

        # 3. Chat Control
        if st.session_state.messages:
            if st.button("💬 Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        st.caption("Powered by Streamlit, PyPDF & Google Gemini API")

    # --------------------------------------------------------------------------
    # Main Content Area: Document Preview & Chat Interface
    # --------------------------------------------------------------------------

    # Assemble Document Context based on Scope Selection
    active_context = ""
    if st.session_state.documents:
        if doc_scope == "All Documents (Combined)":
            context_chunks = [
                f"=== DOCUMENT: {name} ===\n{text}"
                for name, text in st.session_state.documents.items()
            ]
            active_context = "\n\n".join(context_chunks)
        else:
            active_context = f"=== DOCUMENT: {doc_scope} ===\n" + st.session_state.documents.get(doc_scope, "")

        # Expandable Document Content Inspector
        with st.expander(f"🔍 Inspect Document Context Memory ({doc_scope})", expanded=False):
            st.text_area(
                label="Extracted Text Memory Context",
                value=active_context,
                height=220,
                disabled=True
            )

    # Render Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat Input Box for Agent Interactions
    if prompt := st.chat_input("Ask any question about your uploaded document(s)..."):
        # Validate inputs
        if not effective_api_key:
            st.error("🔑 Google Gemini API Key is missing. Please configure it in your `.env` or sidebar.")
        elif not st.session_state.documents:
            st.warning("⚠️ Please upload at least one PDF document before asking questions.")
        else:
            # Display User Message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Generate and Display Assistant Response
            with st.chat_message("assistant"):
                with st.spinner("✨ AI Agent is analyzing document memory..."):
                    try:
                        response_text = generate_rag_response(
                            api_key=effective_api_key,
                            context_text=active_context,
                            chat_history=st.session_state.messages[:-1],  # previous turns
                            user_query=prompt,
                            model_name=selected_model
                        )
                        st.write(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})

                    except GoogleAPIError as g_err:
                        st.error(f"❌ Gemini API Error: {str(g_err)}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
