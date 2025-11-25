#!/usr/bin/env python3
"""
🧭 AI Knowledge Hub - Professional RAG Interface
Dark gradient UI with glassmorphism design
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.config import AppConfig, RAG_OPTIMIZED_MODELS
from src.orchestrator import KnowledgeOrchestrator

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="AI Knowledge Hub",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL STYLES - Inter Font + Dark Gradient Theme
# ============================================================
def inject_global_styles():
    """Inject global CSS styles for AI Knowledge Hub theme"""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* ===== BASE THEME ===== */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: linear-gradient(to bottom, #0e1117, #161b22);
            color: #e5e7eb;
        }

        /* Hide Streamlit chrome */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        .stDeployButton { display: none; }
        
        /* Keep header visible but minimal */
        header[data-testid="stHeader"] {
            background: transparent !important;
            height: auto !important;
        }
        
        /* ===== HIDE SIDEBAR COLLAPSE BUTTON ===== */
        /* Sidebar should always be visible - hide the collapse button to prevent issues */
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* Ensure sidebar is always visible */
        section[data-testid="stSidebar"] {
            transform: none !important;
            visibility: visible !important;
            opacity: 1 !important;
        }

        /* ===== SIDEBAR - CONTROL CENTER ===== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0e1117 0%, #131820 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.12);
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding: 1.5rem 1rem;
        }

        .sidebar-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .sidebar-subtitle {
            font-size: 0.75rem;
            color: rgba(148, 163, 184, 0.7);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 1.5rem;
        }

        .status-card {
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .status-card-title {
            font-size: 0.7rem;
            font-weight: 600;
            color: rgba(148, 163, 184, 0.6);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.75rem;
        }

        .metric-row {
            display: flex;
            justify-content: space-between;
            gap: 0.75rem;
        }

        .metric-box {
            flex: 1;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 8px;
            padding: 0.75rem;
            text-align: center;
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #818cf8;
            line-height: 1.2;
        }

        .metric-label {
            font-size: 0.65rem;
            color: rgba(148, 163, 184, 0.6);
            text-transform: uppercase;
            letter-spacing: 0.03em;
            margin-top: 0.25rem;
        }

        /* ===== MAIN CONTENT ===== */
        .main .block-container {
            padding: 2rem 3rem;
            max-width: 1000px;
        }

        /* ===== HEADER ===== */
        .hub-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            margin-bottom: 2rem;
        }

        .hub-logo {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
        }

        .hub-title-group {
            flex: 1;
        }

        .hub-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #fff;
            margin: 0;
            line-height: 1.2;
        }

        .hub-badge {
            display: inline-block;
            background: rgba(99, 102, 241, 0.15);
            color: #818cf8;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            border: 1px solid rgba(99, 102, 241, 0.3);
            margin-top: 0.25rem;
        }

        /* ===== WELCOME SECTION ===== */
        .welcome-section {
            text-align: center;
            padding: 4rem 2rem;
        }

        .welcome-icon {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            filter: drop-shadow(0 8px 24px rgba(99, 102, 241, 0.4));
        }

        .welcome-title {
            font-size: 2.25rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .welcome-subtitle {
            font-size: 1.1rem;
            color: rgba(148, 163, 184, 0.7);
            margin-bottom: 2.5rem;
        }

        /* ===== SUGGESTION BUTTONS ===== */
        .suggestion-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
            max-width: 600px;
            margin: 0 auto;
        }

        /* ===== CHAT MESSAGES ===== */
        .chat-message-wrapper {
            display: flex;
            margin-bottom: 1rem;
        }

        .chat-message-user {
            margin-left: auto;
            max-width: 80%;
            padding: 0.875rem 1.125rem;
            border-radius: 1.25rem 0.25rem 1.25rem 1.25rem;
            background: linear-gradient(135deg, #2b313e 0%, #1e293b 100%);
            border: 1px solid rgba(148, 163, 184, 0.2);
            color: #e5e7eb;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .chat-message-ai {
            margin-right: auto;
            max-width: 85%;
            padding: 1rem 1.25rem;
            border-radius: 0.25rem 1.25rem 1.25rem 1.25rem;
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(148, 163, 184, 0.15);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            color: #e5e7eb;
            font-size: 0.95rem;
            line-height: 1.7;
        }

        .chat-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }

        .chat-avatar-user {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            margin-left: 0.75rem;
        }

        .chat-avatar-ai {
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            margin-right: 0.75rem;
        }

        .model-tag {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(99, 102, 241, 0.1);
            color: rgba(148, 163, 184, 0.8);
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.7rem;
            margin-top: 0.75rem;
            border: 1px solid rgba(99, 102, 241, 0.15);
        }

        /* ===== SOURCES SECTION ===== */
        .sources-header {
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            font-size: 0.72rem;
            color: #9ca3af;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .source-expander {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }

        .source-quote {
            background: rgba(15, 23, 42, 0.5);
            border-left: 3px solid #6366f1;
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
            border-radius: 0 6px 6px 0;
            font-size: 0.85rem;
            color: rgba(226, 232, 240, 0.9);
            font-style: italic;
        }

        /* ===== CHAT INPUT - FLOATING PILL ===== */
        [data-testid="stChatInput"] {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 800px;
            padding: 1rem 1.5rem 1.5rem 1.5rem;
            background: linear-gradient(to top, #0e1117 60%, transparent);
            z-index: 100;
        }

        [data-testid="stChatInput"] > div {
            border-radius: 999px;
            padding: 0.5rem 1rem;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(148, 163, 184, 0.15);
            background: rgba(22, 27, 34, 0.98);
            border: 1px solid rgba(148, 163, 184, 0.2);
        }

        [data-testid="stChatInput"] textarea {
            background: transparent !important;
            border: none !important;
            color: #e5e7eb !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* ===== BUTTONS ===== */
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #7c3aed 100%);
            color: #fff;
            border: none;
            border-radius: 10px;
            padding: 0.65rem 1.25rem;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45);
        }

        .stButton > button[kind="secondary"] {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.2);
            box-shadow: none;
        }

        .stButton > button[kind="secondary"]:hover {
            background: rgba(51, 65, 85, 0.6);
            border-color: rgba(148, 163, 184, 0.3);
        }

        /* ===== INPUTS ===== */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(148, 163, 184, 0.15) !important;
            border-radius: 10px !important;
            color: #e5e7eb !important;
            font-family: 'Inter', sans-serif !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: rgba(99, 102, 241, 0.5) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }

        /* ===== SELECTBOX ===== */
        .stSelectbox > div > div {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(148, 163, 184, 0.15) !important;
            border-radius: 10px !important;
        }

        /* ===== EXPANDERS ===== */
        .streamlit-expanderHeader {
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(148, 163, 184, 0.1) !important;
            border-radius: 8px !important;
            color: #e5e7eb !important;
            font-weight: 500 !important;
        }

        .streamlit-expanderContent {
            background: rgba(15, 23, 42, 0.4) !important;
            border: 1px solid rgba(148, 163, 184, 0.08) !important;
            border-top: none !important;
            border-radius: 0 0 8px 8px !important;
        }

        /* ===== FILE UPLOADER ===== */
        [data-testid="stFileUploader"] {
            background: rgba(30, 41, 59, 0.3);
            border: 2px dashed rgba(99, 102, 241, 0.3);
            border-radius: 12px;
            padding: 1.25rem;
            transition: all 0.2s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: rgba(99, 102, 241, 0.5);
            background: rgba(30, 41, 59, 0.4);
        }

        /* ===== METRICS ===== */
        [data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 10px;
            padding: 0.75rem 1rem;
        }

        [data-testid="stMetric"] label {
            color: rgba(148, 163, 184, 0.7) !important;
            font-size: 0.75rem !important;
        }

        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #818cf8 !important;
            font-weight: 700 !important;
        }

        /* ===== DIVIDER ===== */
        hr {
            border-color: rgba(148, 163, 184, 0.1);
            margin: 1.5rem 0;
        }

        /* ===== STATUS WIDGET ===== */
        [data-testid="stStatusWidget"] {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 1px solid rgba(99, 102, 241, 0.2) !important;
            border-radius: 12px !important;
        }

        /* ===== DEBUG SECTION ===== */
        .debug-section {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(234, 179, 8, 0.2);
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
        }

        .debug-header {
            color: #fbbf24;
            font-weight: 600;
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.5);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(99, 102, 241, 0.3);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(99, 102, 241, 0.5);
        }

        /* ===== SPACER FOR FIXED INPUT ===== */
        .bottom-spacer {
            height: 120px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Call styles injection
inject_global_styles()

# ============================================================
# QUICK MODELS FOR SELECTION
# ============================================================
QUICK_MODELS = {
    "google/gemini-2.0-flash-exp:free": {"name": "Gemini 2.0 Flash", "icon": "✨", "tier": "free"},
    "google/gemini-pro-1.5": {"name": "Gemini Pro 1.5", "icon": "💎", "tier": "premium"},
    "x-ai/grok-4.1-fast": {"name": "Grok 4.1 Fast", "icon": "🚀", "tier": "premium"},
    "anthropic/claude-3.5-sonnet": {"name": "Claude 3.5 Sonnet", "icon": "🎭", "tier": "premium"},
}

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
def init_session_state():
    """Initialize session state variables"""
    if 'config' not in st.session_state:
        st.session_state.config = AppConfig.load()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'model' not in st.session_state:
        st.session_state.model = st.session_state.config.default_model
    if 'rag' not in st.session_state:
        st.session_state.rag = None
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = None
    if 'debug_mode' not in st.session_state:
        st.session_state.debug_mode = False
    if 'last_response_meta' not in st.session_state:
        st.session_state.last_response_meta = None
    if 'last_sources' not in st.session_state:
        st.session_state.last_sources = []

# ============================================================
# RAG ENGINE - LAZY LOADING
# ============================================================
def get_rag():
    """Lazy load RAG engine"""
    if st.session_state.rag is None:
        from src.rag_engine import RAGEngine
        st.session_state.rag = RAGEngine()
        st.session_state.rag.initialize()
    return st.session_state.rag

def get_rag_stats():
    """Get RAG stats safely"""
    try:
        rag = get_rag()
        return rag.get_stats()
    except Exception as e:
        return {"total_documents": 0, "total_chunks": 0, "error": str(e)}

# ============================================================
# AI CLIENT
# ============================================================
def get_client():
    """Get OpenRouter client"""
    cfg = st.session_state.config
    if cfg.openrouter_api_key:
        from src.ai_client import OpenRouterClient
        return OpenRouterClient(cfg.openrouter_api_key)
    return None

# ============================================================
# ORCHESTRATOR - LAZY LOADING
# ============================================================
def get_orchestrator():
    """
    Lazy load the Knowledge Orchestrator.
    
    The Orchestrator coordinates RAG search and LLM calls,
    providing a unified interface for the chat UI.
    
    Returns:
        KnowledgeOrchestrator instance or None if API key not configured
    """
    if st.session_state.orchestrator is None:
        rag = get_rag()
        client = get_client()
        cfg = st.session_state.config
        
        if client is None:
            return None
        
        st.session_state.orchestrator = KnowledgeOrchestrator(
            rag_engine=rag,
            ai_client=client,
            config=cfg
        )
    return st.session_state.orchestrator

# ============================================================
# CHAT LOGIC
# ============================================================
def process_query(query: str, model: str):
    """
    Process a user query through the Orchestrator (RAG + AI).
    
    This function serves as the bridge between the Streamlit UI and 
    the KnowledgeOrchestrator. It:
    1. Adds the user message to chat history
    2. Validates API key configuration
    3. Delegates to the Orchestrator for RAG search + LLM generation
    4. Stores the result in session state for UI rendering
    
    Args:
        query: The user's question or message
        model: The AI model to use for generation
    """
    cfg = st.session_state.config
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Check for API key
    if not cfg.openrouter_api_key:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "⚠️ **API Key Required**\n\nPlease add your OpenRouter API key in the sidebar to continue.",
            "model": model,
            "sources": []
        })
        return
    
    # Get orchestrator (handles RAG + LLM coordination)
    orchestrator = get_orchestrator()
    
    if orchestrator is None:
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "⚠️ **Configuration Error**\n\nUnable to initialize the orchestrator. Please check your API key.",
            "model": model,
            "sources": []
        })
        return
    
    # Delegate to orchestrator
    result = orchestrator.handle_message(
        user_message=query,
        chat_history=st.session_state.messages,
        model=model
    )
    
    # Add assistant message with orchestrator response
    st.session_state.messages.append({
        "role": "assistant", 
        "content": result.answer, 
        "model": result.model,
        "sources": result.sources
    })
    
    # Store metadata for debug panel
    st.session_state.last_response_meta = {
        "model": result.model,
        "usage": result.usage,
        "steps": result.steps,
        "success": result.success,
        "error": result.error
    }
    st.session_state.last_sources = result.sources

# ============================================================
# SIDEBAR - CONTROL CENTER
# ============================================================
def render_sidebar():
    """Render the sidebar control center"""
    with st.sidebar:
        # Title
        st.markdown('<div class="sidebar-title">🧭 AI Knowledge Hub</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-subtitle">Control Center</div>', unsafe_allow_html=True)
        
        cfg = st.session_state.config
        
        # ===== STATUS SECTION =====
        st.markdown('<div class="status-card"><div class="status-card-title">📊 Knowledge Base Status</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Get stats lazily
        if st.button("🔄 Refresh Stats", key="refresh_stats", use_container_width=True):
            st.session_state.rag = None  # Force refresh
        
        try:
            if st.session_state.rag is not None:
                stats = st.session_state.rag.get_stats()
            else:
                stats = {"total_documents": "—", "total_chunks": "—"}
        except Exception:
            stats = {"total_documents": "—", "total_chunks": "—"}
        
        with col1:
            st.metric("📄 Files", stats.get("total_documents", "—"))
        with col2:
            st.metric("🧩 Chunks", stats.get("total_chunks", "—"))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # ===== MODEL SELECTION =====
        st.markdown("#### 🤖 AI Model")
        
        model_options = list(RAG_OPTIMIZED_MODELS.keys())
        model_names = [f"{RAG_OPTIMIZED_MODELS[m]['name']} ({RAG_OPTIMIZED_MODELS[m].get('tier', 'standard')})" for m in model_options]
        
        current_idx = model_options.index(st.session_state.model) if st.session_state.model in model_options else 0
        
        selected_idx = st.selectbox(
            "Select Model",
            range(len(model_options)),
            index=current_idx,
            format_func=lambda x: model_names[x],
            label_visibility="collapsed"
        )
        
        if model_options[selected_idx] != st.session_state.model:
            st.session_state.model = model_options[selected_idx]
            cfg.default_model = model_options[selected_idx]
            cfg.save()
        
        # Model info
        model_info = RAG_OPTIMIZED_MODELS.get(st.session_state.model, {})
        if model_info:
            st.caption(f"📐 Context: {model_info.get('context', 'N/A')} • 💰 {model_info.get('cost_per_1m_tokens', 'N/A')}")
        
        st.divider()
        
        # ===== API KEY =====
        st.markdown("#### 🔑 API Key")
        key = st.text_input(
            "OpenRouter API Key",
            cfg.openrouter_api_key,
            type="password",
            label_visibility="collapsed",
            placeholder="sk-or-v1-..."
        )
        if key != cfg.openrouter_api_key:
            cfg.openrouter_api_key = key
            cfg.save()
            st.session_state.orchestrator = None  # Reset orchestrator with new API key
        
        st.caption("[Get API Key →](https://openrouter.ai/keys)")
        
        st.divider()
        
        # ===== FILE UPLOAD =====
        st.markdown("#### 📚 Add Knowledge")
        
        files = st.file_uploader(
            "Upload files",
            ['pdf', 'md', 'txt', 'json'],
            accept_multiple_files=True,
            label_visibility="collapsed",
            help="Drag & drop files or click to browse"
        )
        
        if files and st.button("📥 Add to Knowledge Base", use_container_width=True):
            knowledge_dir = Path(".cursor/knowledge")
            knowledge_dir.mkdir(parents=True, exist_ok=True)
            for f in files:
                (knowledge_dir / f.name).write_bytes(f.getbuffer())
            st.success(f"✅ Added {len(files)} file(s)!")
            st.session_state.rag = None  # Force rebuild
            st.session_state.orchestrator = None  # Reset orchestrator with new RAG
            st.rerun()
        
        st.divider()
        
        # ===== ADVANCED SETTINGS =====
        with st.expander("⚙️ Advanced Settings", expanded=False):
            cfg.temperature = st.slider(
                "Temperature",
                0.0, 1.0, cfg.temperature, 0.1,
                help="Higher = more creative, Lower = more focused"
            )
            
            cfg.top_k_results = st.slider(
                "RAG Results (top-k)",
                1, 10, cfg.top_k_results, 1,
                help="Number of knowledge chunks to include"
            )
            
            cfg.max_tokens = st.slider(
                "Max Response Tokens",
                500, 8000, cfg.max_tokens, 500,
                help="Maximum length of AI response"
            )
            
            if st.button("🔄 Rebuild RAG Index", use_container_width=True):
                st.session_state.rag = None
                st.session_state.orchestrator = None  # Reset orchestrator with new RAG
                st.success("Index will rebuild on next query")
        
        st.divider()
        
        # ===== DEBUG MODE =====
        st.session_state.debug_mode = st.checkbox(
            "🐞 Show Debug Info",
            value=st.session_state.debug_mode,
            help="Display raw API responses and metadata"
        )

# ============================================================
# RENDER CHAT MESSAGES
# ============================================================
def render_chat_messages():
    """Render chat history with custom styling"""
    for i, message in enumerate(st.session_state.messages):
        role = message.get("role", "user")
        content = message.get("content", "")
        
        if role == "user":
            # User message - right aligned
            st.markdown(
                f'''
                <div class="chat-message-wrapper">
                    <div class="chat-message-user">{content}</div>
                    <div class="chat-avatar chat-avatar-user">👤</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        else:
            # AI message - left aligned with glassmorphism
            st.markdown(
                '''
                <div class="chat-message-wrapper">
                    <div class="chat-avatar chat-avatar-ai">🧠</div>
                    <div class="chat-message-ai">
                ''',
                unsafe_allow_html=True
            )
            
            # Render markdown content properly
            st.markdown(content)
            
            # Model tag
            model_id = message.get("model", "")
            model_info = RAG_OPTIMIZED_MODELS.get(model_id, {})
            model_name = model_info.get("name", model_id.split("/")[-1] if model_id else "Unknown")
            
            st.markdown(
                f'<div class="model-tag">🤖 {model_name}</div>',
                unsafe_allow_html=True
            )
            
            st.markdown('</div></div>', unsafe_allow_html=True)
            
            # Render sources if available
            sources = message.get("sources", [])
            if sources:
                render_sources(sources)
            
            # Debug info
            if st.session_state.debug_mode and i == len(st.session_state.messages) - 1:
                render_debug_info()

def render_sources(sources):
    """Render RAG sources section"""
    if not sources:
        return
    
    st.markdown('<div class="sources-header">📚 Knowledge Sources</div>', unsafe_allow_html=True)
    
    for source in sources:
        filename = source.get("filename", "Document")
        score = source.get("score", 0)
        snippet = source.get("snippet", "")
        file_type = source.get("type", "unknown").upper()
        
        score_pct = int(round(score * 100)) if isinstance(score, float) else score
        
        header = f"📄 {filename} ({file_type}) — Match: {score_pct}%"
        
        with st.expander(header, expanded=False):
            st.markdown(
                f'<div class="source-quote">{snippet}</div>',
                unsafe_allow_html=True
            )

def render_debug_info():
    """Render debug information including orchestrator steps"""
    meta = st.session_state.last_response_meta
    if meta:
        st.markdown('<div class="debug-section">', unsafe_allow_html=True)
        st.markdown('<div class="debug-header">🐞 Debug Information</div>', unsafe_allow_html=True)
        
        # Display orchestration steps if available
        steps = meta.get("steps", [])
        if steps:
            st.markdown("**🎯 Orchestration Steps:**")
            for i, step in enumerate(steps, 1):
                step_type = step.get("type", "unknown")
                description = step.get("description", "")
                duration = step.get("duration_ms", 0)
                
                # Icon based on step type
                icon = {
                    "rag_search": "🔍",
                    "context_build": "📝",
                    "llm_call": "🤖"
                }.get(step_type, "⚙️")
                
                st.markdown(f"{i}. {icon} **{step_type}**: {description} ({duration:.1f}ms)")
                
                # Show step metadata in expander
                step_meta = step.get("metadata", {})
                if step_meta:
                    with st.expander(f"Step {i} details", expanded=False):
                        st.json(step_meta)
        
        # Display general metadata
        st.markdown("**📊 Response Metadata:**")
        display_meta = {
            "model": meta.get("model"),
            "usage": meta.get("usage"),
            "success": meta.get("success", True)
        }
        if meta.get("error"):
            display_meta["error"] = meta.get("error")
        st.json(display_meta)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# MAIN APPLICATION
# ============================================================
def main():
    """Main application entry point"""
    init_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # ===== HEADER =====
    st.markdown(
        '''
        <div class="hub-header">
            <div class="hub-logo">🧭</div>
            <div class="hub-title-group">
                <div class="hub-title">AI Knowledge Hub</div>
                <span class="hub-badge">RAG-Powered</span>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    # ===== MAIN CONTENT =====
    if not st.session_state.messages:
        # Welcome screen
        st.markdown(
            '''
            <div class="welcome-section">
                <div class="welcome-icon">🔮</div>
                <div class="welcome-title">What would you like to explore?</div>
                <div class="welcome-subtitle">Ask questions about your knowledge base</div>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        # Suggestion buttons
        suggestions = [
            ("🐳", "Docker best practices"),
            ("🏗️", "Backend architecture patterns"),
            ("🤖", "How does RAG work?"),
            ("⚡", "What is Cursor AI?"),
        ]
        
        cols = st.columns(2)
        for i, (icon, text) in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(f"{icon} {text}", key=f"suggestion_{i}", use_container_width=True):
                    with st.status("🔎 Searching knowledge base...", expanded=True) as status:
                        status.update(label="🧠 Generating response...", state="running")
                        process_query(text, st.session_state.model)
                        status.update(label="✅ Complete", state="complete", expanded=False)
                    st.rerun()
    else:
        # Chat history
        render_chat_messages()
        
        # Clear chat button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Clear Conversation", use_container_width=True):
                st.session_state.messages = []
                st.session_state.last_response_meta = None
                st.session_state.last_sources = []
                st.rerun()
    
    # Bottom spacer for fixed input
    st.markdown('<div class="bottom-spacer"></div>', unsafe_allow_html=True)
    
    # ===== CHAT INPUT =====
    if prompt := st.chat_input("Ask anything about your knowledge base..."):
        with st.status("🔎 Searching knowledge base...", expanded=True) as status:
            status.update(label="🧠 Generating response...", state="running")
            process_query(prompt, st.session_state.model)
            status.update(label="✅ Complete", state="complete", expanded=False)
        st.rerun()

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    main()
