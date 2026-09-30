import os
# Fix protobuf compiler descriptor compatibility issues
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

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

# Load API key from secrets, environment, or user override
API_KEY = ""

# 1. Try loading from streamlit secrets
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    elif "google_api_key" in st.secrets:
        API_KEY = st.secrets["google_api_key"]
except Exception:
    pass

# 2. Try loading from environment variables
if not API_KEY:
    API_KEY = os.getenv("GOOGLE_API_KEY", "")

if API_KEY == "your_api_key_here":
    API_KEY = ""

# Initialize API key override in session state if not already set
if "api_key_override" not in st.session_state:
    st.session_state.api_key_override = ""

# 3. Use user override if provided
if not API_KEY and st.session_state.api_key_override:
    API_KEY = st.session_state.api_key_override

# Set environment for underlying langchain libraries
if API_KEY:
    os.environ["GOOGLE_API_KEY"] = API_KEY

# Page configuration
st.set_page_config(
    page_title="JAN SAHAYAK — Independent Digital Gazette & AI Intelligence",
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
        "color": "#111111",
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
        "color": "#15803d",
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
        "color": "#b45309",
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
        "title": "Document Indexing & Registry",
        "description": "Learn how official policy gazette PDFs are uploaded, chunked, and embedded into the grounded ChromaDB vector store.",
        "steps": [
            "Click 'Browse files' in the Document Desk sidebar",
            "Select government scheme PDF documents",
            "Click 'PROCESS & INDEX DOCUMENTS'",
            "Wait for vector store confirmation"
        ]
    },
    {
        "title": "Grounded Inquiry & Synthesis",
        "description": "Query the AI assistant to receive factual, policy-grounded syntheses backed by exact document evidence citations.",
        "steps": [
            "Type your policy question into the Inquiry Desk",
            "Or select any preset question from Scheme Compendium",
            "Review the generated Policy Brief & Grounded Synthesis",
            "Expand 'Source Evidence & Document References' for verified proof"
        ]
    }
]

# ===================== EMBLEM LOGO BASE64 ENCODER =====================
import base64

EMBLEM_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 240" width="140" height="168">
  <g stroke="#111111" stroke-width="1.8" fill="none" stroke-linejoin="round" stroke-linecap="round">
    <path d="M 35 130 C 35 45, 165 45, 165 130" stroke-width="2.2"/>
    <path d="M 43 130 C 43 54, 157 54, 157 130" stroke-width="1.2"/>
    <line x1="100" y1="28" x2="100" y2="52" stroke-width="1"/>
    <line x1="80" y1="33" x2="87" y2="54" stroke-width="1"/>
    <line x1="120" y1="33" x2="113" y2="54" stroke-width="1"/>
    <line x1="62" y1="45" x2="74" y2="63" stroke-width="1"/>
    <line x1="138" y1="45" x2="126" y2="63" stroke-width="1"/>
    <line x1="48" y1="65" x2="64" y2="76" stroke-width="1"/>
    <line x1="152" y1="65" x2="136" y2="76" stroke-width="1"/>
    <path d="M 52 130 C 52 68, 148 68, 148 130" stroke-width="1.2"/>
    <path d="M 25 195 C 60 185, 100 195, 100 195 C 100 195, 140 185, 175 195 L 175 208 C 140 198, 100 208, 100 208 C 100 198, 60 198, 25 208 Z" fill="#f7f5f0" stroke-width="2"/>
    <path d="M 30 198 C 62 189, 100 198, 100 198 C 100 198, 138 189, 170 198" stroke-width="1.2"/>
    <line x1="100" y1="195" x2="100" y2="208" stroke-width="1.5"/>
    <path d="M 38 165 L 162 165 L 156 188 L 44 188 Z" fill="#f7f5f0" stroke-width="2"/>
    <circle cx="100" cy="176" r="9" stroke-width="2" fill="#f7f5f0"/>
    <circle cx="100" cy="176" r="2" fill="#111111"/>
    <line x1="100" y1="167" x2="100" y2="185" stroke-width="1"/>
    <line x1="91" y1="176" x2="109" y2="176" stroke-width="1"/>
    <line x1="94" y1="170" x2="106" y2="182" stroke-width="1"/>
    <line x1="94" y1="182" x2="106" y2="170" stroke-width="1"/>
    <circle cx="62" cy="176" r="4" stroke-width="1.2"/>
    <circle cx="138" cy="176" r="4" stroke-width="1.2"/>
    <line x1="32" y1="162" x2="168" y2="162" stroke-width="2.2"/>
    <path d="M 86 68 Q 80 54 90 52 Q 98 50 100 56 Q 102 50 110 52 Q 120 54 114 68 Z" fill="#f7f5f0" stroke-width="1.8"/>
    <path d="M 84 56 L 78 48 L 86 51 Z" fill="#111111"/>
    <path d="M 116 56 L 122 48 L 114 51 Z" fill="#111111"/>
    <path d="M 91 75 C 91 68 109 68 109 75 C 109 82 91 82 91 75 Z" fill="#f7f5f0" stroke-width="1.8"/>
    <circle cx="100" cy="72" r="2.5" fill="#111111"/>
    <path d="M 94 79 Q 100 83 106 79" stroke-width="1.5"/>
    <circle cx="93" cy="64" r="2.2" fill="#111111"/>
    <circle cx="107" cy="64" r="2.2" fill="#111111"/>
    <path d="M 89 61 Q 94 58 98 62" stroke-width="1.5"/>
    <path d="M 111 61 Q 106 58 102 62" stroke-width="1.5"/>
    <path d="M 82 82 C 74 95, 76 120, 78 160 L 122 160 C 124 120, 126 95, 118 82 Z" fill="#f7f5f0" stroke-width="1.8"/>
    <path d="M 86 88 Q 98 96 84 106" stroke-width="1.2"/>
    <path d="M 114 88 Q 102 96 116 106" stroke-width="1.2"/>
    <path d="M 84 110 Q 98 118 86 130" stroke-width="1.2"/>
    <path d="M 116 110 Q 102 118 114 130" stroke-width="1.2"/>
    <path d="M 86 134 Q 98 142 86 155" stroke-width="1.2"/>
    <path d="M 114 134 Q 102 142 114 155" stroke-width="1.2"/>
    <path d="M 78 74 C 64 66 48 78 52 98 C 56 118 66 140 76 160 L 80 160 C 74 140 68 118 70 98 Z" fill="#f7f5f0" stroke-width="1.8"/>
    <path d="M 50 82 C 44 78 42 70 50 66 C 56 68 56 76 54 82 Z" fill="#111111"/>
    <circle cx="56" cy="78" r="2" fill="#111111"/>
    <path d="M 60 90 Q 72 96 58 106" stroke-width="1.2"/>
    <path d="M 58 110 Q 72 116 60 130" stroke-width="1.2"/>
    <path d="M 122 74 C 136 66 152 78 148 98 C 144 118 134 140 124 160 L 120 160 C 126 140 132 118 130 98 Z" fill="#f7f5f0" stroke-width="1.8"/>
    <path d="M 150 82 C 156 78 158 70 150 66 C 144 68 144 76 146 82 Z" fill="#111111"/>
    <circle cx="144" cy="78" r="2" fill="#111111"/>
    <path d="M 140 90 Q 128 96 142 106" stroke-width="1.2"/>
    <path d="M 142 110 Q 128 116 140 130" stroke-width="1.2"/>
  </g>
</svg>"""

EMBLEM_B64 = base64.b64encode(EMBLEM_SVG.encode('utf-8')).decode('utf-8')
EMBLEM_HTML = f'<img src="data:image/svg+xml;base64,{EMBLEM_B64}" width="140" height="168" style="display: block; margin: 0 auto 0.8rem auto;" alt="Jan Sahayak Emblem" />'

# ===================== JAN SAHAYAK GAZETTE STYLING =====================
st.markdown("""
<style>
    /* ===== Google Fonts ===== */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400;1,600&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* ===== Global Background & Body Reset ===== */
    html, body, [class*="css"], .stApp {
        background-color: #f7f5f0 !important;
        color: #1a1a1a !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main block container padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 1200px !important;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #111111 !important;
        font-weight: 700;
    }

    /* ===== Sidebar Gazette Styling ===== */
    section[data-testid="stSidebar"] {
        background-color: #e5dfd2 !important;
        border-right: 1px solid #d0c8b6 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #3e3a33 !important;
    }

    /* Sidebar Top Utility Desk Title */
    .utility-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: 2px;
        color: #111111;
        text-transform: uppercase;
        margin: 0;
        padding-top: 0.2rem;
    }
    .utility-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 1.5px;
        color: #555046;
        text-transform: uppercase;
        margin-top: 0.2rem;
        margin-bottom: 1rem;
    }
    .gazette-hr {
        border: none;
        border-top: 1px solid #cbbfa8;
        margin: 0.8rem 0 1.2rem 0;
    }

    /* ===== Sidebar Section Cards (EXPLICIT VISUAL SEPARATION) ===== */
    .sidebar-section-card {
        background-color: #ded6c4 !important;
        border: 1px solid #c7beaa !important;
        border-radius: 8px !important;
        padding: 1.1rem !important;
        margin-bottom: 1.25rem !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
    }
    .sidebar-section-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #2b2722;
        text-transform: uppercase;
        padding-bottom: 0.5rem;
        margin-bottom: 0.8rem;
        border-bottom: 1px solid #c7beaa;
    }

    /* System Status Table Styling */
    .status-grid {
        display: flex;
        flex-direction: column;
        gap: 0.55rem;
    }
    .status-row-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.82rem;
    }
    .status-row-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        font-weight: 600;
        color: #555047;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .status-row-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        font-weight: 700;
        color: #111111;
    }
    .status-badge-connected {
        color: #15803d;
        font-weight: 700;
    }
    .status-badge-disconnected {
        color: #b91c1c;
        font-weight: 700;
    }

    /* Document Desk Label & Icon */
    .doc-desk-label {
        font-size: 0.88rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .doc-desk-info {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        border: 1px solid #888;
        font-size: 0.7rem;
        color: #555;
        font-family: sans-serif;
    }

    /* ===== Gazette Top Header Banner ===== */
    .gazette-top-banner {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
        margin-bottom: 1.5rem;
    }
    .gazette-emblem-svg {
        display: block;
        margin: 0 auto 0.8rem auto;
    }
    .gazette-main-title {
        font-family: 'Playfair Display', 'Cinzel', Georgia, serif;
        font-size: 3.4rem;
        font-weight: 900;
        letter-spacing: 4px;
        color: #111111;
        margin: 0;
        line-height: 1.05;
        text-transform: uppercase;
    }
    .gazette-tagline {
        font-family: 'Playfair Display', Georgia, serif;
        font-style: italic;
        font-size: 1.05rem;
        color: #4a453e;
        margin-top: 0.6rem;
        letter-spacing: 0.2px;
    }
    .gazette-double-rule {
        border: none;
        border-top: 2px solid #1a1a1a;
        border-bottom: 1px solid #1a1a1a;
        height: 3px;
        margin: 1.4rem 0 1.6rem 0;
    }

    /* ===== Custom Streamlit Tabs Styling ===== */
    div[data-testid="stTabs"] {
        background-color: transparent !important;
    }
    div[data-baseweb="tab-list"] {
        gap: 1.5rem !important;
        border-bottom: 1px solid #dcd5c6 !important;
        padding-bottom: 0.2rem !important;
    }
    button[data-baseweb="tab"] {
        font-family: 'Playfair Display', Georgia, serif !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
        color: #555047 !important;
        background: transparent !important;
        border: none !important;
        padding: 0.5rem 0.5rem !important;
        text-transform: uppercase !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #111111 !important;
        border-bottom: 3px solid #111111 !important;
    }

    /* ===== Visual Section Cards in Main Area (SEPARATION) ===== */
    .main-section-card {
        background-color: #f4f0e6;
        border: 1px solid #d6cfc0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }
    .submitted-inquiry-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.8px;
        color: #666157;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .inquiry-heading {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #111111;
        margin: 0 0 1.2rem 0;
        line-height: 1.3;
    }

    /* Policy Brief & Grounded Synthesis Container */
    .policy-synthesis-card {
        background-color: #fbf9f4;
        border: 1px solid #cfc7b6;
        border-radius: 6px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }
    .synthesis-header-strip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 2px;
        color: #666157;
        text-transform: uppercase;
        padding-bottom: 0.6rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e0d8c9;
    }
    .synthesis-body-text {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.08rem;
        line-height: 1.75;
        color: #1a1a1a;
    }

    /* Verified Source Chunk Cards */
    .source-gazette-card {
        background-color: #f4f0e6;
        border: 1px solid #d5cebf;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .source-gazette-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e0d8c8;
        padding-bottom: 0.4rem;
        margin-bottom: 0.6rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
        color: #44403c;
    }
    .verified-pill {
        background-color: #15803d;
        color: #ffffff;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-right: 0.5rem;
        text-transform: uppercase;
    }
    .relevance-pill {
        background-color: #eae3d3;
        border: 1px solid #c9c2b0;
        color: #44403c;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
    }
    .source-gazette-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.85rem;
        line-height: 1.6;
        color: #2b2723;
        white-space: pre-wrap;
    }

    /* ===== Primary Black Gazette Buttons ===== */
    div.stButton > button, .stButton > button[kind="primary"] {
        background-color: #111111 !important;
        color: #ffffff !important;
        font-family: 'JetBrains Mono', 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
        border-radius: 4px !important;
        border: 1px solid #000000 !important;
        padding: 0.65rem 1.2rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    /* Force inner paragraph and text nodes to be crisp white */
    div.stButton > button p,
    div.stButton > button[kind="primary"] p,
    div.stButton > button span,
    div.stButton > button div {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    div.stButton > button:hover {
        background-color: #2d2b27 !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.18) !important;
        transform: translateY(-1px) !important;
    }

    /* Secondary / Preset Question Buttons */
    .stButton > button[kind="secondary"] {
        background-color: #eae4d7 !important;
        color: #111111 !important;
        border: 1px solid #c8c0ae !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0 !important;
        text-transform: none !important;
        text-align: left !important;
        border-radius: 6px !important;
    }
    .stButton > button[kind="secondary"] p,
    .stButton > button[kind="secondary"] span {
        color: #111111 !important;
        font-weight: 600 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #dfd7c7 !important;
        border-color: #a89f8b !important;
        color: #000000 !important;
    }

    /* ===== Bottom Dock Chat Input ===== */
    .stBottom, div[data-testid="stBottom"] {
        background-color: #f7f5f0 !important;
        border-top: 1px solid #dcd5c6 !important;
    }
    div[data-testid="stBottomBlockContainer"] {
        background-color: transparent !important;
        padding: 0.6rem 1rem 1rem !important;
    }
    div[data-testid="stChatInput"] > div {
        background-color: #ffffff !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 4px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #111111 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #777267 !important;
        font-style: italic;
    }

    /* File Uploader Box Styling */
    div[data-testid="stFileUploader"] {
        background-color: #fbf9f4 !important;
        border: 1px dashed #bbb3a2 !important;
        border-radius: 6px !important;
        padding: 0.5rem !important;
    }
    
    /* Expanders Styling */
    .streamlit-expanderHeader {
        background-color: #ece6d9 !important;
        border: 1px solid #d4cdbe !important;
        border-radius: 6px !important;
        color: #111111 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }

    /* Scheme Compendium Glass Cards */
    .scheme-gazette-card {
        background-color: #f3efe6;
        border: 1px solid #d5cebe;
        border-radius: 8px;
        padding: 1.4rem;
        height: 100%;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }
    .scheme-gazette-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #111111;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .scheme-gazette-desc {
        font-size: 0.88rem;
        color: #555047;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Ensure required storage folders exist
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

if "query_cache" not in st.session_state:
    st.session_state.query_cache = {}

# Auto-load vector database if API key is available and files exist
if API_KEY and st.session_state.vector_db is None:
    if os.path.exists(CHROMA_DIR) and len(st.session_state.uploaded_files) > 0:
        try:
            st.session_state.vector_db = vector_store.get_vector_store(CHROMA_DIR, API_KEY)
        except Exception:
            pass

# ===================== SIDEBAR (UTILITY DESK) =====================
with st.sidebar:
    st.markdown("""
    <div>
        <div class="utility-header">UTILITY DESK</div>
        <div class="utility-sub">SYSTEM REGISTRY & INGESTION</div>
    </div>
    <hr class="gazette-hr" />
    """, unsafe_allow_html=True)
    
    # ---- CARD 1: SYSTEM STATUS (EXPLICIT VISUAL SEPARATION) ----
    is_connected = bool(API_KEY)
    status_class = "status-badge-connected" if is_connected else "status-badge-disconnected"
    status_label = "CONNECTED" if is_connected else "DISCONNECTED"
    dot_color = "#15803d" if is_connected else "#b91c1c"
    
    num_files = len(st.session_state.uploaded_files)
    chunk_count = 0
    if st.session_state.vector_db is not None:
        chunk_count = vector_store.get_chunk_count(st.session_state.vector_db)
    
    st.markdown(f"""
    <div class="sidebar-section-card">
        <div class="sidebar-section-title">SYSTEM STATUS</div>
        <div class="status-grid">
            <div class="status-row-item">
                <span class="status-row-label">AI SERVICE</span>
                <span class="status-row-val {status_class}">
                    <span style="color: {dot_color}; font-size: 1rem;">●</span> {status_label}
                </span>
            </div>
            <div class="status-row-item">
                <span class="status-row-label">MODEL</span>
                <span class="status-row-val">Gemini 3.6 Flash</span>
            </div>
            <div class="status-row-item">
                <span class="status-row-label">VECTOR STORE</span>
                <span class="status-row-val">ChromaDB</span>
            </div>
            <div class="status-row-item">
                <span class="status-row-label">INDEXED</span>
                <span class="status-row-val">{num_files} DOCS</span>
            </div>
            <div class="status-row-item">
                <span class="status-row-label">CHUNKS</span>
                <span class="status-row-val">{chunk_count}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ---- CARD 2: DOCUMENT DESK (EXPLICIT VISUAL SEPARATION) ----
    st.markdown("""
    <div class="sidebar-section-card">
        <div class="sidebar-section-title">DOCUMENT DESK</div>
        <div class="doc-desk-label">
            Upload Scheme PDF Files <span class="doc-desk-info" title="Upload government scheme PDF files for AI retrieval">?</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload Scheme PDF Files",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="200MB per file • PDF"
    )
    
    process_btn = st.button("PROCESS & INDEX DOCUMENTS", type="primary", use_container_width=True)
    
    if process_btn:
        if not API_KEY:
            st.error("API Key missing! Configure GOOGLE_API_KEY in environment or input field below.")
        elif not uploaded_files:
            st.warning("Please upload at least one PDF file first.")
        else:
            with st.spinner("Indexing documents into ChromaDB..."):
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
                        st.success(f"Successfully indexed {len(saved_paths)} PDFs ({len(all_chunks)} chunks).")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error writing to database: {str(e)}")
                else:
                    st.error("No valid text extracted from PDF files.")
    
    if num_files > 0:
        with st.expander("Indexed Files Archive"):
            for f in st.session_state.uploaded_files:
                st.markdown(f"• **{f}**")

    # ---- CARD 3: API KEY & SYSTEM CONTROLS ----
    if not API_KEY or st.session_state.api_key_override:
        st.markdown('<div class="sidebar-section-card"><div class="sidebar-section-title">API CONFIGURATION</div></div>', unsafe_allow_html=True)
        user_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.api_key_override,
            placeholder="Enter AIzaSy... API Key"
        )
        if user_key != st.session_state.api_key_override:
            st.session_state.api_key_override = user_key
            st.rerun()

    # Reset System Button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Reset Database & History", type="secondary", use_container_width=True):
        with st.spinner("Resetting system state..."):
            utils.clear_directory(UPLOAD_DIR)
            vector_store.reset_vector_store(CHROMA_DIR)
            st.session_state.chat_history = []
            st.session_state.vector_db = None
            st.session_state.uploaded_files = []
            st.session_state.pending_question = None
            st.session_state.query_cache = {}
            st.success("System reset complete.")
            st.rerun()

# ===================== GAZETTE TOP HEADER =====================
st.markdown(f"""
<div class="gazette-top-banner">
    {EMBLEM_HTML}
    <div class="gazette-main-title">JAN SAHAYAK</div>
    <div class="gazette-tagline">An independent digital gazette and grounded AI intelligence system for Indian government policy.</div>
    <hr class="gazette-double-rule" />
</div>
""", unsafe_allow_html=True)

# ===================== MAIN TABS =====================
tab_inquiry, tab_schemes, tab_methodology = st.tabs(["INQUIRY DESK", "SCHEME COMPENDIUM", "SYSTEM METHODOLOGY"])

# ===================== TAB 1: INQUIRY DESK =====================
with tab_inquiry:
    is_ready = bool(API_KEY) and chunk_count > 0

    # Determine default question if history exists or pending
    active_question = None
    if st.session_state.pending_question:
        active_question = st.session_state.pending_question
        st.session_state.pending_question = None
    elif st.session_state.chat_history:
        # Find latest user question
        for msg in reversed(st.session_state.chat_history):
            if msg["role"] == "user":
                active_question = msg["content"]
                break

    # If demo files need generation
    if num_files == 0:
        st.markdown("""
        <div class="main-section-card" style="border-left: 4px solid #111111;">
            <div class="submitted-inquiry-tag">NOTICE: NO DOCUMENTS INDEXED</div>
            <div style="font-size: 0.95rem; color: #44403c; line-height: 1.6; margin-top: 0.5rem;">
                The gazette registry is currently empty. Upload scheme PDF guidelines in the <b>DOCUMENT DESK</b> sidebar, or generate official demo scheme assets below to commence AI inquiry.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Generate & Load Demo Scheme PDFs", type="primary", use_container_width=True):
            with st.spinner("Generating policy PDFs..."):
                try:
                    import generate_dummy_assets
                    generate_dummy_assets.ensure_directories([UPLOAD_DIR])
                    generate_dummy_assets.create_dummy_pdf(os.path.join(UPLOAD_DIR, "scheme_summary.pdf"))
                    generate_dummy_assets.create_ayushman_bharat_pdf(os.path.join(UPLOAD_DIR, "ayushman_bharat.pdf"))
                    st.session_state.uploaded_files = [
                        f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith('.pdf')
                    ]
                    st.success("Demo scheme PDFs created. Click 'PROCESS & INDEX DOCUMENTS' in sidebar.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating assets: {str(e)}")

    elif chunk_count == 0:
        st.markdown("""
        <div class="main-section-card" style="border-left: 4px solid #b45309;">
            <div class="submitted-inquiry-tag" style="color: #b45309;">ACTION REQUIRED: INDEXING PENDING</div>
            <div style="font-size: 0.95rem; color: #44403c; line-height: 1.6; margin-top: 0.5rem;">
                Uploaded PDFs detected in registry. Click <b>"PROCESS & INDEX DOCUMENTS"</b> in the sidebar to build ChromaDB embeddings.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Render Active Submitted Inquiry Display (Matching Screenshot Exact Structure)
    if active_question:
        st.markdown(f"""
        <div style="margin-bottom: 1.2rem;">
            <div class="submitted-inquiry-tag">SUBMITTED INQUIRY</div>
            <div class="inquiry-heading">{active_question}</div>
        </div>
        """, unsafe_allow_html=True)

    # Render History / Active Synthesis Output
    if st.session_state.chat_history:
        # Display the most recent assistant answer with exact screenshot formatting
        last_user = None
        last_assistant = None

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                last_user = msg["content"]
            elif msg["role"] == "assistant":
                last_assistant = msg

        if last_assistant:
            # POLICY BRIEF & GROUNDED SYNTHESIS CARD (CLEAR VISUAL SEPARATION)
            st.markdown(f"""
            <div class="policy-synthesis-card">
                <div class="synthesis-header-strip">POLICY BRIEF & GROUNDED SYNTHESIS</div>
                <div class="synthesis-body-text">{last_assistant['content']}</div>
            </div>
            """, unsafe_allow_html=True)

            # SOURCE EVIDENCE ACCORDION
            if "sources" in last_assistant and last_assistant["sources"]:
                with st.expander("SOURCE EVIDENCE & DOCUMENT REFERENCES"):
                    for idx, src in enumerate(last_assistant["sources"]):
                        st.markdown(f"""
                        <div class="source-gazette-card">
                            <div class="source-gazette-meta">
                                <span>
                                    <span class="verified-pill">VERIFIED</span>
                                    Source {idx+1}: {src['source']} (Page {src['page']})
                                </span>
                                <span class="relevance-pill">Relevance: {src['score']}%</span>
                            </div>
                            <div class="source-gazette-text">{src['content']}</div>
                        </div>
                        """, unsafe_allow_html=True)

    elif is_ready and not active_question:
        # Initial Inquiry Desk Welcome & Preset Question Grid
        st.markdown("""
        <div class="main-section-card">
            <div class="submitted-inquiry-tag">GAZETTE INQUIRY DESK</div>
            <div style="font-size: 0.95rem; color: #4a453e; line-height: 1.6; margin-bottom: 1rem;">
                Select a preset government scheme question below or submit a custom inquiry via the input desk:
            </div>
        </div>
        """, unsafe_allow_html=True)

        preset_qs = [
            "What is PMJDY?",
            "What is the overdraft limit under PMJDY?",
            "Who can apply for PM Kisan?",
            "What health coverage is provided under Ayushman Bharat?"
        ]

        q_cols = st.columns(2)
        for idx, q in enumerate(preset_qs):
            with q_cols[idx % 2]:
                if st.button(q, key=f"init_q_{idx}", type="secondary", use_container_width=True):
                    st.session_state.pending_question = q
                    st.rerun()

    # Chat Input Box at Bottom (Matching Screenshot Placeholder)
    input_placeholder = "Submit inquiry on any government scheme..." if is_ready else "Index PDFs to submit inquiries"
    user_query = st.chat_input(input_placeholder, disabled=not is_ready)

    if user_query:
        # Trigger answer generation
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        cache = st.session_state.query_cache
        if user_query in cache:
            answer = cache[user_query]["answer"]
            sources = cache[user_query]["sources"]
        else:
            with st.spinner("Scanning policy documents & synthesizing brief..."):
                chunks_with_scores = chatbot.retrieve_relevant_chunks(
                    st.session_state.vector_db,
                    user_query,
                    k=3
                )
                result = chatbot.generate_answer(
                    user_query,
                    chunks_with_scores,
                    API_KEY
                )
                answer = result["answer"]
                sources = result["sources"]
                cache[user_query] = {"answer": answer, "sources": sources}

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })
        st.rerun()

# ===================== TAB 2: SCHEME COMPENDIUM =====================
with tab_schemes:
    st.markdown("""
    <div style="margin-bottom: 1.2rem;">
        <div class="submitted-inquiry-tag">NATIONAL SCHEME COMPENDIUM</div>
        <div style="font-size: 0.95rem; color: #555047;">Official repositories and key statutory inquiries for major government initiatives:</div>
    </div>
    """, unsafe_allow_html=True)

    scheme_cols = st.columns(3)
    for idx, scheme in enumerate(DEMO_SCHEMES):
        with scheme_cols[idx]:
            st.markdown(f"""
            <div class="scheme-gazette-card">
                <div style="font-size: 2rem; margin-bottom: 0.3rem;">{scheme['icon']}</div>
                <div class="scheme-gazette-title">{scheme['name']}</div>
                <div class="scheme-gazette-desc">{scheme['description']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><hr class='gazette-hr'/><br>", unsafe_allow_html=True)
    st.markdown('<div class="submitted-inquiry-tag">PRESET STATUTORY INQUIRIES</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    for scheme in DEMO_SCHEMES:
        st.markdown(f"""
        <div style="font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 700; color: #111; margin-bottom: 0.6rem;">
            {scheme['icon']} {scheme['name']} ({scheme['short']})
        </div>
        """, unsafe_allow_html=True)

        q_cols = st.columns(len(scheme["questions"]))
        for q_idx, q in enumerate(scheme["questions"]):
            with q_cols[q_idx]:
                if st.button(q, key=f"compendium_q_{scheme['short']}_{q_idx}", type="secondary", use_container_width=True):
                    st.session_state.pending_question = q
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

# ===================== TAB 3: SYSTEM METHODOLOGY =====================
with tab_methodology:
    st.markdown("""
    <div style="margin-bottom: 1.2rem;">
        <div class="submitted-inquiry-tag">SYSTEM METHODOLOGY & RAG PIPELINE</div>
        <div style="font-size: 0.95rem; color: #555047;">Technical architecture governing grounded policy document retrieval and AI intelligence synthesis:</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-section-card">
        <div class="submitted-inquiry-tag">RETRIEVAL-AUGMENTED GENERATION (RAG) ARCHITECTURE</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; text-align: center; margin-top: 1rem;">
            <div style="background: #fbf9f4; padding: 1rem; border-radius: 6px; border: 1px solid #dcd5c6;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">📄</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700;">1. INGESTION</div>
                <div style="font-size: 0.75rem; color: #666; margin-top: 0.2rem;">PDF Policy Guidelines</div>
            </div>
            <div style="background: #fbf9f4; padding: 1rem; border-radius: 6px; border: 1px solid #dcd5c6;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">✂️</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700;">2. CHUNKING</div>
                <div style="font-size: 0.75rem; color: #666; margin-top: 0.2rem;">1000-char segments</div>
            </div>
            <div style="background: #fbf9f4; padding: 1rem; border-radius: 6px; border: 1px solid #dcd5c6;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">🧬</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700;">3. EMBEDDING</div>
                <div style="font-size: 0.75rem; color: #666; margin-top: 0.2rem;">768-D Vector Space</div>
            </div>
            <div style="background: #fbf9f4; padding: 1rem; border-radius: 6px; border: 1px solid #dcd5c6;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">💾</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700;">4. CHROMA DB</div>
                <div style="font-size: 0.75rem; color: #666; margin-top: 0.2rem;">Similarity Index</div>
            </div>
            <div style="background: #fbf9f4; padding: 1rem; border-radius: 6px; border: 1px solid #dcd5c6;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">🔍</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700;">5. RETRIEVAL</div>
                <div style="font-size: 0.75rem; color: #666; margin-top: 0.2rem;">Cosine Similarity</div>
            </div>
            <div style="background: #fbf9f4; padding: 1rem; border-radius: 6px; border: 1px solid #dcd5c6;">
                <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">🤖</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700;">6. SYNTHESIS</div>
                <div style="font-size: 0.75rem; color: #666; margin-top: 0.2rem;">Gemini Grounded Brief</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="submitted-inquiry-tag">TUTORIAL MEDIA & DEMONSTRATION</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Embed YouTube video container with gazette border
    st.markdown("""
    <div style="position: relative; width: 100%; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px; border: 1px solid #d5cebe; margin-bottom: 1.5rem;">
        <iframe 
            src="https://www.youtube-nocookie.com/embed/h2aWGlSVr98" 
            title="Government Schemes Tutorial"
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 8px;"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
        </iframe>
    </div>
    """, unsafe_allow_html=True)

    guide_cols = st.columns(2)
    for t_idx, tutorial in enumerate(TUTORIAL_VIDEOS):
        with guide_cols[t_idx]:
            steps_html = ''.join([
                f'<div style="font-size: 0.84rem; color: #222; padding: 0.35rem 0.7rem; margin: 0.3rem 0; border-left: 3px solid #111111; background: #fbf9f4; border-radius: 0 4px 4px 0;">▸ {step}</div>'
                for step in tutorial['steps']
            ])
            st.markdown(f"""
            <div class="main-section-card" style="height: 100%;">
                <div style="font-family: 'Playfair Display', serif; font-size: 1.15rem; font-weight: 700; color: #111; margin-bottom: 0.5rem;">{tutorial['title']}</div>
                <div style="font-size: 0.85rem; color: #555047; margin-bottom: 0.8rem; line-height: 1.5;">{tutorial['description']}</div>
                {steps_html}
            </div>
            """, unsafe_allow_html=True)
