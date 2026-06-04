import os
import streamlit as st
from dotenv import load_dotenv

import utils
import pdf_processor
import vector_store
import chatbot

# Load environment variables from .env
load_dotenv()

# App directories
UPLOAD_DIR = "uploads"
CHROMA_DIR = "chroma_db"

# Load API key from environment — no user input needed
API_KEY = os.getenv("GOOGLE_API_KEY", "")
if API_KEY == "your_api_key_here":
    API_KEY = ""

# Set environment for underlying langchain libraries
if API_KEY:
    os.environ["GOOGLE_API_KEY"] = API_KEY

# Page configuration
st.set_page_config(
    page_title="GovSchemes AI Chatbot",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== DEMO SCHEMES DATA =====================
DEMO_SCHEMES = [
    {
        "name": "Pradhan Mantri Jan Dhan Yojana",
        "short": "PMJDY",
        "icon": "🏦",
        "color": "#6366f1",
        "description": "National Mission for Financial Inclusion — zero-balance bank accounts, RuPay cards, insurance & overdraft for all.",
        "questions": [
            "What is PMJDY?",
            "What is the overdraft limit under PMJDY?",
            "Who is eligible for PMJDY?"
        ]
    },
    {
        "name": "PM Kisan Samman Nidhi",
        "short": "PM-KISAN",
        "icon": "🌾",
        "color": "#10b981",
        "description": "Direct income support of ₹6,000/year to small and marginal farmer families across India.",
        "questions": [
            "Who can apply for PM Kisan?",
            "What benefits are provided under PM Kisan?",
            "How much financial assistance is given under PM Kisan?"
        ]
    },
    {
        "name": "Ayushman Bharat (PM-JAY)",
        "short": "PM-JAY",
        "icon": "🏥",
        "color": "#f59e0b",
        "description": "World's largest health insurance scheme — ₹5 Lakh cashless cover for 55 crore beneficiaries.",
        "questions": [
            "What is Ayushman Bharat?",
            "Who can avail the Ayushman Bharat scheme?",
            "What health coverage is provided under Ayushman Bharat?"
        ]
    }
]

# ===================== TUTORIAL VIDEOS =====================
TUTORIAL_VIDEOS = [
    {
        "title": "Upload & Process PDFs",
        "description": "Learn how to upload government scheme PDF documents and index them into the vector database for AI-powered querying.",
        "steps": [
            "Click 'Browse files' in the sidebar",
            "Select one or more PDF files",
            "Click 'Process & Index PDFs'",
            "Wait for indexing to complete"
        ]
    },
    {
        "title": "Ask Questions",
        "description": "Use the chatbot to ask natural language questions about any indexed government scheme.",
        "steps": [
            "Type your question in the chat input",
            "Or click any preset question button",
            "View AI-generated answers with source citations",
            "Expand 'Verified Source Chunks' for references"
        ]
    }
]

# ===================== PREMIUM DARK THEME CSS =====================
st.markdown("""
<style>
    /* ===== Google Fonts ===== */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* ===== Global Reset ===== */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
    }

    /* ===== Dark Theme Base ===== */
    .stApp {
        background: linear-gradient(180deg, #0a0e1a 0%, #111827 50%, #0f172a 100%);
    }
    
    /* Sidebar Dark Theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #94a3b8 !important;
    }

    /* ===== Cards ===== */
    .glass-card {
        background: #141b2d;
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.35);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.1);
        transform: translateY(-2px);
    }

    /* ===== Video crisp rendering ===== */
    video, iframe {
        border-radius: 12px !important;
        image-rendering: auto;
    }

    /* ===== Minimal Chat Input Bar ===== */
    .stChatInput, div[data-testid="stChatInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    .stBottom, div[data-testid="stBottom"] {
        background: #0a0e1a !important;
        border-top: 1px solid rgba(255,255,255,0.06) !important;
    }
    div[data-testid="stBottomBlockContainer"] {
        background: transparent !important;
        padding: 0.5rem 1rem 0.8rem !important;
    }
    div[data-testid="stChatInput"] > div {
        background: #1a1f2e !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        padding: 0 !important;
    }
    div[data-testid="stChatInput"] > div:focus-within {
        border-color: rgba(255,255,255,0.15) !important;
        box-shadow: none !important;
    }
    div[data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #e2e8f0 !important;
        border: none !important;
        font-size: 0.95rem !important;
        caret-color: #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #555e6e !important;
    }
    div[data-testid="stChatInput"] button {
        background: transparent !important;
        color: #64748b !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.4rem !important;
        margin-right: 0.3rem !important;
    }
    div[data-testid="stChatInput"] button:hover {
        color: #e2e8f0 !important;
    }
    
    /* ===== Sidebar Cards ===== */
    .sidebar-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(99, 102, 241, 0.12);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
        transition: all 0.25s ease;
    }
    .sidebar-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
        background: rgba(30, 41, 59, 0.7);
    }
    .sidebar-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 0.95rem;
        color: #f1f5f9 !important;
    }
    .sidebar-card p {
        margin: 0.15rem 0;
        font-size: 0.82rem;
        color: #94a3b8 !important;
    }

    /* ===== AI Status Card ===== */
    .ai-status-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(99, 102, 241, 0.08) 100%);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .ai-status-card .status-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.3rem 0;
        font-size: 0.85rem;
        color: #e2e8f0;
    }
    .ai-status-card .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-green 2s infinite;
    }
    .ai-status-card .status-dot.connected { background: #10b981; }
    .ai-status-card .status-dot.disconnected { background: #ef4444; animation: pulse-red 2s infinite; }
    
    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5); }
        50% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    }
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.5); }
        50% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
    }

    /* ===== Scheme Cards (Sidebar) ===== */
    .scheme-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(99, 102, 241, 0.1);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
        cursor: default;
    }
    .scheme-card:hover {
        background: rgba(30, 41, 59, 0.7);
        border-left: 3px solid var(--accent-color, #6366f1);
    }
    .scheme-card .scheme-name {
        font-size: 0.88rem;
        font-weight: 600;
        color: #f1f5f9 !important;
        margin: 0;
    }
    .scheme-card .scheme-desc {
        font-size: 0.75rem;
        color: #64748b !important;
        margin: 0.25rem 0 0 0;
        line-height: 1.4;
    }

    /* ===== App Header ===== */
    .app-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #1e3a5f 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.2);
        position: relative;
        overflow: hidden;
    }
    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .app-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    .app-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 50%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
        z-index: 1;
    }
    .app-subtitle {
        font-size: 1.05rem;
        opacity: 0.85;
        margin-top: 0.5rem;
        font-weight: 300;
        color: #c7d2fe;
        position: relative;
        z-index: 1;
    }

    /* ===== Welcome Screen ===== */
    .welcome-container {
        text-align: center;
        padding: 3rem 1rem;
    }
    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
    }
    .welcome-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #c7d2fe, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .welcome-desc {
        font-size: 1rem;
        color: #94a3b8;
        max-width: 600px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
    }
    .welcome-features {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    .feature-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: left;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.1);
    }
    .feature-card .feat-icon { font-size: 1.8rem; margin-bottom: 0.5rem; display: block; }
    .feature-card .feat-title { font-size: 1rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.3rem; }
    .feature-card .feat-desc { font-size: 0.82rem; color: #64748b; line-height: 1.5; }

    /* ===== Source Chunks ===== */
    .source-container {
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        background: rgba(15, 23, 42, 0.5);
        padding: 1rem 1.2rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    .source-container:hover {
        border-color: rgba(99, 102, 241, 0.3);
        background: rgba(15, 23, 42, 0.7);
    }
    .source-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(99, 102, 241, 0.1);
        padding-bottom: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.8rem;
        font-weight: 600;
        color: #a5b4fc;
    }
    .source-badge {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
        color: #c4b5fd;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.72rem;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    .verified-badge {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(52, 211, 153, 0.15));
        color: #6ee7b7;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.2);
        margin-right: 0.5rem;
    }
    .source-text {
        font-size: 0.82rem;
        color: #cbd5e1;
        white-space: pre-wrap;
        line-height: 1.6;
    }

    /* ===== Database Stats Card ===== */
    .stats-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(99, 102, 241, 0.12);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #6366f1;
    }
    .stats-card h4 {
        margin: 0 0 0.5rem 0;
        color: #f1f5f9 !important;
        font-size: 0.95rem;
    }
    .stats-card p {
        margin: 0.15rem 0;
        color: #94a3b8 !important;
        font-size: 0.82rem;
    }
    .stats-card .status-ready {
        color: #10b981 !important;
        font-weight: 600;
    }
    .stats-card .status-empty {
        color: #ef4444 !important;
        font-weight: 600;
    }

    /* ===== Buttons ===== */
    .stButton > button {
        border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.25s ease !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* ===== Preset Question Buttons ===== */
    .stButton > button[kind="secondary"] {
        background: rgba(30, 41, 59, 0.5) !important;
        color: #c7d2fe !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        font-size: 0.82rem !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(99, 102, 241, 0.15) !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
        color: #e0e7ff !important;
    }

    /* ===== Chat Messages ===== */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(99, 102, 241, 0.08) !important;
        border-radius: 14px !important;
    }
    
    /* ===== Chat Input ===== */
    .stChatInput {
        border-color: rgba(99, 102, 241, 0.2) !important;
    }
    .stChatInput > div {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        border-radius: 12px !important;
    }
    
    /* ===== File Uploader ===== */
    .stFileUploader {
        border-radius: 12px !important;
    }

    /* ===== Expander (Source Chunks) ===== */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.4) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(99, 102, 241, 0.1) !important;
        color: #a5b4fc !important;
    }

    /* ===== Dividers ===== */
    hr {
        border-color: rgba(99, 102, 241, 0.1) !important;
    }

    /* ===== Scrollbar ===== */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }

    /* ===== Tutorial Card ===== */
    .tutorial-card {
        background: rgba(30, 41, 59, 0.3);
        border: 1px solid rgba(99, 102, 241, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.75rem;
    }
    .tutorial-card h5 {
        margin: 0 0 0.4rem 0;
        font-size: 0.9rem;
        color: #e2e8f0 !important;
    }
    .tutorial-card p {
        font-size: 0.78rem;
        color: #64748b !important;
        margin: 0.15rem 0;
        line-height: 1.5;
    }
    .tutorial-card .step {
        font-size: 0.78rem;
        color: #94a3b8 !important;
        padding-left: 0.5rem;
        border-left: 2px solid rgba(99, 102, 241, 0.2);
        margin: 0.3rem 0;
    }

    /* ===== Sidebar Logo ===== */
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }
    .sidebar-logo .logo-icon {
        font-size: 3rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    .sidebar-logo .logo-text {
        font-family: 'Outfit', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a5b4fc, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sidebar-logo .logo-sub {
        font-size: 0.72rem;
        color: #64748b !important;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ===== Scheme Section Header ===== */
    .section-header {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 1rem 0 0.5rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid rgba(99, 102, 241, 0.1);
    }
    
    /* ===== Preset question container ===== */
    .example-questions-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin-top: 1rem;
    }

    /* ===== No Documents Warning ===== */
    .lock-warning {
        background: rgba(217, 119, 6, 0.1);
        border-left: 4px solid #d97706;
        color: #fbbf24;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(217, 119, 6, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Ensure folders exist
utils.ensure_directories([UPLOAD_DIR, CHROMA_DIR])

# ===================== SESSION STATE =====================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
    if os.path.exists(UPLOAD_DIR):
        files = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith('.pdf')]
        st.session_state.uploaded_files = files

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# Auto-load vector database if API key is available and files exist
if API_KEY and st.session_state.vector_db is None:
    if os.path.exists(CHROMA_DIR) and len(st.session_state.uploaded_files) > 0:
        try:
            st.session_state.vector_db = vector_store.get_vector_store(CHROMA_DIR, API_KEY)
        except Exception:
            pass

# ===================== SIDEBAR (slim — controls only) =====================
with st.sidebar:
    # Logo / Branding
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">G</span>
        <div class="logo-text">GovSchemes AI</div>
        <div class="logo-sub">Intelligent Policy Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ---- AI Status Card ----
    is_connected = bool(API_KEY)
    status_dot_class = "connected" if is_connected else "disconnected"
    status_text = "Connected" if is_connected else "Disconnected"
    status_color = "#10b981" if is_connected else "#ef4444"
    
    st.markdown(f"""
    <div class="ai-status-card">
        <div class="status-row"><b>AI Model:</b>&nbsp; Gemini 2.0 Flash</div>
        <div class="status-row">
            <span class="status-dot {status_dot_class}"></span>
            <b>Status:</b>&nbsp; <span style="color: {status_color};">{status_text}</span>
        </div>
        <div class="status-row"><b>Embeddings:</b>&nbsp; gemini-embedding-001</div>
        <div class="status-row"><b>Vector DB:</b>&nbsp; ChromaDB</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ---- Document Management ----
    st.markdown('<div class="section-header">Document Management</div>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload Government Scheme PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload official scheme guidelines or summaries."
    )
    
    process_btn = st.button("Process & Index PDFs", type="primary", use_container_width=True)
    
    if process_btn:
        if not API_KEY:
            st.error("API Key not configured in .env file!")
        elif not uploaded_files:
            st.warning("Please upload at least one PDF file first.")
        else:
            with st.spinner("Processing & embedding documents..."):
                saved_paths = []
                for uploaded_file in uploaded_files:
                    if utils.validate_pdf(uploaded_file.name, uploaded_file.size):
                        path = utils.save_uploaded_file(uploaded_file, UPLOAD_DIR)
                        saved_paths.append(path)
                
                all_chunks = []
                for path in saved_paths:
                    try:
                        docs = pdf_processor.extract_text_from_pdf(path)
                        chunks = pdf_processor.chunk_documents(docs)
                        all_chunks.extend(chunks)
                    except Exception as e:
                        st.error(f"Error loading {os.path.basename(path)}: {str(e)}")
                
                if all_chunks:
                    try:
                        db = vector_store.get_vector_store(CHROMA_DIR, API_KEY)
                        vector_store.add_documents_to_store(db, all_chunks)
                        st.session_state.vector_db = db
                        
                        st.session_state.uploaded_files = [
                            f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith('.pdf')
                        ]
                        st.success(f"Indexed {len(saved_paths)} PDFs — {len(all_chunks)} chunks created.")
                    except Exception as e:
                        st.error(f"Error writing to database: {str(e)}")
                else:
                    st.error("No valid text could be extracted from the uploaded files.")
                    
    st.markdown("---")
    
    # ---- Database Stats ----
    st.markdown('<div class="section-header">Database Stats</div>', unsafe_allow_html=True)
    
    chunk_count = 0
    if st.session_state.vector_db is not None:
        chunk_count = vector_store.get_chunk_count(st.session_state.vector_db)
        
    num_files = len(st.session_state.uploaded_files)
    
    if chunk_count > 0:
        status_html = '<span class="status-ready">Ready for Querying</span>'
    elif num_files > 0:
        status_html = '<span style="color: #f59e0b !important; font-weight: 600;">Files Found — Click Process to Index</span>'
    else:
        status_html = '<span class="status-empty">No Documents Indexed</span>'
    
    st.markdown(f"""
    <div class="stats-card">
        <h4>System Status</h4>
        <p><b>Uploaded Files:</b> {num_files}</p>
        <p><b>Indexed Chunks:</b> {chunk_count}</p>
        <p>{status_html}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if num_files > 0:
        with st.expander("Active Documents"):
            for f in st.session_state.uploaded_files:
                st.caption(f"· {f}")
    
    st.markdown("---")
    
    # ---- Reset ----
    st.markdown('<div class="section-header">System Actions</div>', unsafe_allow_html=True)
    reset_btn = st.button("Reset Database & History", type="secondary", use_container_width=True)
    if reset_btn:
        with st.spinner("Resetting system..."):
            utils.clear_directory(UPLOAD_DIR)
            vector_store.reset_vector_store(CHROMA_DIR)
            st.session_state.chat_history = []
            st.session_state.vector_db = None
            st.session_state.uploaded_files = []
            st.session_state.pending_question = None
            st.success("System reset successfully!")
            st.rerun()


# ===================== MAIN AREA =====================

# App Header
st.markdown("""
<div class="app-header">
    <h1 class="app-title">GovSchemes AI Chatbot</h1>
    <div class="app-subtitle">AI-powered document retrieval for Indian Government Schemes — ask questions, get verified answers with source citations</div>
</div>
""", unsafe_allow_html=True)

# ===================== TABS =====================
tab_chat, tab_schemes, tab_howto = st.tabs(["Chat", "Schemes & Questions", "How to Use"])

# ===================== TAB 1: CHAT =====================
with tab_chat:
    # ---- Welcome Screen (when no chat history) ----
    if not st.session_state.chat_history and st.session_state.pending_question is None:
        st.markdown("""
        <div class="welcome-container">
            <div class="welcome-title">Welcome to GovSchemes AI</div>
            <div class="welcome-desc">
                Ask questions about government schemes using AI-powered document retrieval. 
                Upload PDF guidelines or use our pre-loaded demo schemes to get started instantly.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        st.markdown("""
        <div class="welcome-features">
            <div class="feature-card">
                <div class="feat-title">Upload & Index PDFs</div>
                <div class="feat-desc">Upload government scheme PDFs and they are automatically chunked, embedded, and indexed in a vector database.</div>
            </div>
            <div class="feature-card">
                <div class="feat-title">Semantic Search</div>
                <div class="feat-desc">Questions are matched against document chunks using cosine similarity for precise, context-aware retrieval.</div>
            </div>
            <div class="feature-card">
                <div class="feat-title">AI-Generated Answers</div>
                <div class="feat-desc">Gemini 2.0 Flash generates factual answers strictly grounded in the retrieved source documents.</div>
            </div>
            <div class="feature-card">
                <div class="feat-title">Verified Sources</div>
                <div class="feat-desc">Every answer includes verified source chunks with page numbers and relevance scores for full transparency.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Example questions grid
        st.markdown("#### Try asking a question:")
        
        example_questions = [
            "What is PMJDY?",
            "What is the overdraft limit under PMJDY?",
            "Who is eligible for PM Kisan?",
            "What health coverage does Ayushman Bharat provide?"
        ]
        
        cols = st.columns(2)
        for idx, q in enumerate(example_questions):
            with cols[idx % 2]:
                if st.button(q, key=f"welcome_{idx}", use_container_width=True):
                    st.session_state.pending_question = q
                    st.rerun()

    # ---- Chat Engine ----
    is_ready = API_KEY and num_files > 0

    if not API_KEY:
        st.markdown("""
        <div class="lock-warning">
            <b>API Key Missing:</b> Please configure your Google Gemini API Key in the <code>.env</code> file to activate the chatbot.
        </div>
        """, unsafe_allow_html=True)

    if is_ready:
        if st.session_state.vector_db is None:
            st.warning("Database is initializing. Please wait or click 'Process & Index PDFs' in the sidebar.")
        
        # Render Chat History
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                if "sources" in message and message["sources"]:
                    with st.expander("Verified Source Chunks"):
                        for idx, src in enumerate(message["sources"]):
                            st.markdown(f"""
                            <div class="source-container">
                                <div class="source-meta">
                                <span>
                                    <span class="verified-badge">Verified</span>
                                    Source {idx+1}: {src['source']} (Page {src['page']})
                                </span>
                                <span class="source-badge">Relevance: {src['score']}%</span>
                            </div>
                                <div class="source-text">{src['content']}</div>
                            </div>
                            """, unsafe_allow_html=True)

        # Determine the user query
        input_disabled = (st.session_state.vector_db is None or chunk_count == 0)
        placeholder_text = "Ask about any government scheme..." if not input_disabled else "Index PDFs to start chatting"
        
        user_query = st.chat_input(placeholder_text, disabled=input_disabled)
        
        # Check for pending question from preset buttons
        if st.session_state.pending_question and not input_disabled:
            user_query = st.session_state.pending_question
            st.session_state.pending_question = None
        
        if user_query:
            with st.chat_message("user"):
                st.markdown(user_query)
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            with st.chat_message("assistant"):
                with st.spinner("Scanning schemes database..."):
                    chunks_with_scores = chatbot.retrieve_relevant_chunks(
                        st.session_state.vector_db, 
                        user_query, 
                        k=4
                    )
                    
                    result = chatbot.generate_answer(
                        user_query, 
                        chunks_with_scores, 
                        API_KEY
                    )
                    
                    answer = result["answer"]
                    sources = result["sources"]
                    
                    st.markdown(answer)
                    
                    if sources:
                        with st.expander("Verified Source Chunks"):
                            for idx, src in enumerate(sources):
                                st.markdown(f"""
                                <div class="source-container">
                                    <div class="source-meta">
                                        <span>
                                            <span class="verified-badge">✓ Verified</span>
                                            📄 Source {idx+1}: {src['source']} (Page {src['page']})
                                        </span>
                                        <span class="source-badge">Relevance: {src['score']}%</span>
                                    </div>
                                    <div class="source-text">{src['content']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
            
            st.rerun()


# ===================== TAB 2: SCHEMES & QUESTIONS =====================
with tab_schemes:
    st.markdown("#### Available Government Schemes")
    st.markdown("<br>", unsafe_allow_html=True)
    
    scheme_cols = st.columns(3)
    for idx, scheme in enumerate(DEMO_SCHEMES):
        with scheme_cols[idx]:
            st.markdown(f"""
            <div class="glass-card" style="border-top: 3px solid {scheme['color']}; min-height: 200px;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{scheme['icon']}</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #e2e8f0; margin-bottom: 0.4rem;">{scheme['name']}</div>
                <div style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6;">{scheme['description']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Preset Questions")
    st.markdown("Click any question below to send it directly to the chatbot:")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for scheme in DEMO_SCHEMES:
        st.markdown(f"""
        <div style="margin-bottom: 0.3rem;">
            <span style="font-size: 1.1rem; font-weight: 600; color: #e2e8f0;">{scheme['icon']} {scheme['name']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        q_cols = st.columns(len(scheme["questions"]))
        for q_idx, q in enumerate(scheme["questions"]):
            with q_cols[q_idx]:
                if st.button(q, key=f"scheme_q_{scheme['short']}_{q_idx}", use_container_width=True):
                    st.session_state.pending_question = q
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)


# ===================== TAB 3: HOW TO USE =====================
with tab_howto:
    st.markdown("#### Tutorial Video")
    st.markdown("Watch this video to understand how government schemes work and how to use this chatbot:")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Embed YouTube tutorial video — direct iframe for crisp HD
    st.markdown("""
    <div style="position: relative; width: 100%; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 12px; margin-bottom: 1rem;">
        <iframe 
            src="https://www.youtube-nocookie.com/embed/h2aWGlSVr98" 
            title="Government Schemes Tutorial"
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 12px;"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
        </iframe>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Step-by-Step Guide")
    st.markdown("<br>", unsafe_allow_html=True)
    
    guide_cols = st.columns(2)
    
    for t_idx, tutorial in enumerate(TUTORIAL_VIDEOS):
        with guide_cols[t_idx]:
            st.markdown(f"""
            <div class="glass-card" style="min-height: 250px;">
                <div style="font-size: 1.1rem; font-weight: 700; color: #e2e8f0; margin-bottom: 0.8rem;">{tutorial['title']}</div>
                <div style="font-size: 0.88rem; color: #94a3b8; margin-bottom: 1rem; line-height: 1.6;">{tutorial['description']}</div>
                {''.join(f'<div style="font-size: 0.85rem; color: #c7d2fe; padding: 0.4rem 0.8rem; margin: 0.3rem 0; border-left: 3px solid rgba(99, 102, 241, 0.4); background: rgba(99, 102, 241, 0.05); border-radius: 0 8px 8px 0;">▸ {step}</div>' for step in tutorial['steps'])}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### How RAG Works")
    st.markdown("""
    <div class="glass-card">
        <div style="font-size: 1rem; font-weight: 600; color: #e2e8f0; margin-bottom: 1rem;">Retrieval-Augmented Generation Pipeline</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; text-align: center;">
            <div style="padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📄</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #c7d2fe;">1. Upload</div>
                <div style="font-size: 0.75rem; color: #64748b;">PDF documents are uploaded</div>
            </div>
            <div style="padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">✂️</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #c7d2fe;">2. Chunk</div>
                <div style="font-size: 0.75rem; color: #64748b;">Split into 1000-char segments</div>
            </div>
            <div style="padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧬</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #c7d2fe;">3. Embed</div>
                <div style="font-size: 0.75rem; color: #64748b;">Converted to 768-D vectors</div>
            </div>
            <div style="padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💾</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #c7d2fe;">4. Store</div>
                <div style="font-size: 0.75rem; color: #64748b;">Indexed in ChromaDB</div>
            </div>
            <div style="padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #c7d2fe;">5. Retrieve</div>
                <div style="font-size: 0.75rem; color: #64748b;">Top-K similarity search</div>
            </div>
            <div style="padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #c7d2fe;">6. Generate</div>
                <div style="font-size: 0.75rem; color: #64748b;">Gemini writes grounded answer</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

