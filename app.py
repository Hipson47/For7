#!/usr/bin/env python3
"""
📓 RAG Knowledge Assistant - NotebookLM Style
Professional AI-powered knowledge base
"""

import streamlit as st
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.config import AppConfig, RAG_OPTIMIZED_MODELS

# Page config
st.set_page_config(
    page_title="Knowledge Assistant",
    page_icon="📓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { background: linear-gradient(180deg, #0f0f15 0%, #1a1a24 100%); }
    #MainMenu, footer, .stDeployButton { visibility: hidden; }
    .block-container { padding: 2rem; max-width: 900px; }
    
    .header { display: flex; align-items: center; gap: 12px; padding: 1rem 0 2rem 0; 
              border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 2rem; }
    .logo { width: 42px; height: 42px; background: linear-gradient(135deg, #6366f1, #8b5cf6); 
            border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; }
    .title { font-size: 1.3rem; font-weight: 600; color: #fff; font-family: 'Inter', sans-serif; }
    .badge { background: rgba(99,102,241,0.2); color: #818cf8; padding: 4px 10px; 
             border-radius: 20px; font-size: 11px; font-weight: 600; }
    
    .welcome { text-align: center; padding: 4rem 0; }
    .welcome-title { font-size: 2.5rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }
    .welcome-sub { font-size: 1.1rem; color: rgba(255,255,255,0.5); margin-bottom: 2rem; }
    
    .user-msg { background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3);
                border-radius: 16px; padding: 1rem 1.25rem; margin: 1rem 0; color: #fff; }
    .bot-msg { padding: 1rem 0; color: rgba(255,255,255,0.9); line-height: 1.8; }
    .model-tag { display: inline-block; background: rgba(255,255,255,0.05); padding: 4px 10px;
                 border-radius: 12px; font-size: 0.75rem; color: rgba(255,255,255,0.5); margin-top: 0.5rem; }
    
    section[data-testid="stSidebar"] { background: #0f0f15; border-right: 1px solid rgba(255,255,255,0.08); }
    section[data-testid="stSidebar"] h2 { font-size: 0.85rem; font-weight: 600; 
                                           color: rgba(255,255,255,0.4); text-transform: uppercase; }
    
    [data-testid="stFileUploader"] { background: rgba(255,255,255,0.02); 
                                      border: 2px dashed rgba(255,255,255,0.1); border-radius: 12px; padding: 1rem; }
    
    .stButton > button { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff;
                         border: none; border-radius: 10px; padding: 0.6rem 1.2rem; font-weight: 500; }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 20px rgba(99,102,241,0.4); }
    
    .stTextInput > div > div > input { background: rgba(255,255,255,0.03); 
                                        border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; color: #fff; }
    
    .stat-box { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
                border-radius: 10px; padding: 1rem; text-align: center; }
    .stat-val { font-size: 1.5rem; font-weight: 600; color: #818cf8; }
    .stat-lbl { font-size: 0.75rem; color: rgba(255,255,255,0.4); }
</style>
""", unsafe_allow_html=True)

# Quick models
QUICK_MODELS = {
    "google/gemini-2.0-flash-exp:free": {"name": "Gemini 2.0", "icon": "✨"},
    "google/gemini-pro-1.5": {"name": "Gemini Pro", "icon": "💎"},
    "x-ai/grok-4.1-fast": {"name": "Grok 4.1", "icon": "🚀"},
    "anthropic/claude-3.5-sonnet": {"name": "Claude 3.5", "icon": "🎭"},
}

def init():
    if 'config' not in st.session_state:
        st.session_state.config = AppConfig.load()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'model' not in st.session_state:
        st.session_state.model = st.session_state.config.default_model
    if 'rag' not in st.session_state:
        st.session_state.rag = None

def get_rag():
    """Lazy load RAG engine"""
    if st.session_state.rag is None:
        from src.rag_engine import RAGEngine
        st.session_state.rag = RAGEngine()
        st.session_state.rag.initialize()
    return st.session_state.rag

def get_client():
    cfg = st.session_state.config
    if cfg.openrouter_api_key:
        from src.ai_client import OpenRouterClient
        return OpenRouterClient(cfg.openrouter_api_key)
    return None

def ask(query: str, model: str):
    cfg = st.session_state.config
    st.session_state.messages.append({"role": "user", "content": query})
    
    if not cfg.openrouter_api_key:
        st.session_state.messages.append({"role": "assistant", "content": "⚠️ Add API Key in sidebar", "model": model})
        return
    
    # Get context from RAG
    context = "No context available."
    try:
        rag = get_rag()
        context = rag.get_context_for_query(query, top_k=cfg.top_k_results)
    except Exception as e:
        context = f"Error: {e}"
    
    prompt = f"""You are a helpful assistant. Answer based on context.
Rules: Answer in user's language, be concise, use Markdown, cite sources.

Context:
{context}"""
    
    msgs = [{"role": "system", "content": prompt}, {"role": "user", "content": query}]
    
    client = get_client()
    if client:
        resp = client.chat_completion(msgs, model, cfg.temperature, cfg.max_tokens)
        if resp.success:
            st.session_state.messages.append({"role": "assistant", "content": resp.content, "model": model})
        else:
            st.session_state.messages.append({"role": "assistant", "content": f"❌ {resp.error}", "model": model})

def sidebar():
    with st.sidebar:
        st.markdown("## 🔧 Settings")
        cfg = st.session_state.config
        
        st.markdown("#### API Key")
        key = st.text_input("Key", cfg.openrouter_api_key, type="password", label_visibility="collapsed", placeholder="sk-or-v1-...")
        if key != cfg.openrouter_api_key:
            cfg.openrouter_api_key = key
            cfg.save()
            st.rerun()
        st.caption("[Get API Key →](https://openrouter.ai/keys)")
        
        st.divider()
        st.markdown("#### 📚 Sources")
        
        files = st.file_uploader("Files", ['pdf','md','txt','json'], True, label_visibility="collapsed")
        if files and st.button("📥 Add", use_container_width=True):
            d = Path(".cursor/knowledge")
            d.mkdir(parents=True, exist_ok=True)
            for f in files:
                (d/f.name).write_bytes(f.getbuffer())
            st.success(f"Added {len(files)} files!")
            st.session_state.rag = None  # Reset RAG
            st.rerun()
        
        # Stats (lazy load)
        if st.button("📊 Show Stats"):
            try:
                stats = get_rag().get_stats()
                st.metric("Documents", stats["total_documents"])
                st.metric("Chunks", stats.get("total_chunks", 0))
            except Exception as e:
                st.error(f"Error: {e}")
        
        st.divider()
        with st.expander("⚙️ Advanced"):
            cfg.temperature = st.slider("Temperature", 0.0, 1.0, cfg.temperature, 0.1)
            cfg.top_k_results = st.slider("RAG Results", 1, 10, cfg.top_k_results)
            if st.button("🔄 Rebuild"):
                st.session_state.rag = None
                st.rerun()

def main():
    init()
    cfg = st.session_state.config
    sidebar()
    
    # Header
    st.markdown('<div class="header"><div class="logo">📓</div><span class="title">Knowledge Assistant</span><span class="badge">RAG</span></div>', unsafe_allow_html=True)
    
    # Content
    if not st.session_state.messages:
        st.markdown('<div class="welcome"><div class="welcome-title">What would you like to explore?</div><div class="welcome-sub">Ask questions about your knowledge base</div></div>', unsafe_allow_html=True)
        
        sugs = [("🐳", "Docker best practices"), ("🏗️", "Backend architecture"), ("🤖", "How does RAG work?"), ("⚡", "What is Cursor AI?")]
        cols = st.columns(4)
        for i, (icon, text) in enumerate(sugs):
            with cols[i]:
                if st.button(f"{icon} {text}", key=f"s{i}", use_container_width=True):
                    ask(text, st.session_state.model)
                    st.rerun()
    else:
        for m in st.session_state.messages:
            if m["role"] == "user":
                st.markdown(f'<div class="user-msg">{m["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="bot-msg">', unsafe_allow_html=True)
                st.markdown(m["content"])
                if "model" in m:
                    info = RAG_OPTIMIZED_MODELS.get(m["model"], {})
                    st.markdown(f'<div class="model-tag">🤖 {info.get("name", m["model"].split("/")[-1])}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Spacer
    st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
    
    # Model selector
    st.markdown("---")
    st.markdown("**Model:**")
    mcols = st.columns(len(QUICK_MODELS))
    for i, (mid, info) in enumerate(QUICK_MODELS.items()):
        with mcols[i]:
            sel = st.session_state.model == mid
            if st.button(f"{info['icon']} {info['name']}", key=f"m{i}", type="primary" if sel else "secondary", use_container_width=True):
                st.session_state.model = mid
                cfg.default_model = mid
                cfg.save()
                st.rerun()
    
    # Input
    c1, c2 = st.columns([9, 1])
    with c1:
        q = st.text_input("Q", placeholder="Ask anything...", label_visibility="collapsed", key="q")
    with c2:
        send = st.button("➤", type="primary", use_container_width=True)
    
    if q and send:
        with st.spinner("Thinking..."):
            ask(q, st.session_state.model)
        st.rerun()
    
    if st.session_state.messages and st.button("🗑️ Clear"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
