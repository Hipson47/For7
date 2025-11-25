#!/usr/bin/env python3
"""
🤖 RAG Knowledge Assistant - Modern GUI
AI-powered knowledge base assistant with OpenRouter integration
"""

import streamlit as st
import requests
import time
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import AppConfig, RAG_OPTIMIZED_MODELS, get_model_info
from src.rag_engine import get_rag_engine
from src.ai_client import OpenRouterClient, RAGAssistant

# Page configuration
st.set_page_config(
    page_title="🤖 RAG Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e94560 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Cards */
    .stExpander {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(233, 69, 96, 0.3);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #e94560, #0f3460);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(233, 69, 96, 0.4);
    }
    
    /* Text areas */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(233, 69, 96, 0.3);
        border-radius: 10px;
        color: white;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: rgba(15, 52, 96, 0.8);
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(0, 255, 0, 0.1);
        border-left: 4px solid #00ff00;
    }
    
    .stError {
        background-color: rgba(255, 0, 0, 0.1);
        border-left: 4px solid #ff0000;
    }
    
    /* Model cards */
    .model-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(233, 69, 96, 0.2);
    }
    
    /* Chat messages */
    .user-message {
        background: linear-gradient(90deg, #e94560, #0f3460);
        border-radius: 15px 15px 5px 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .assistant-message {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px 15px 15px 5px;
        padding: 15px;
        margin: 10px 0;
        border-left: 3px solid #e94560;
    }
    
    /* Stats cards */
    .stat-card {
        background: rgba(233, 69, 96, 0.1);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(233, 69, 96, 0.3);
    }
    
    .stat-number {
        font-size: 2.5em;
        font-weight: bold;
        color: #e94560;
    }
    
    .stat-label {
        color: #aaa;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state"""
    if 'config' not in st.session_state:
        st.session_state.config = AppConfig.load()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = None
    
    if 'ai_client' not in st.session_state:
        st.session_state.ai_client = None

def get_rag():
    """Get or initialize RAG engine"""
    if st.session_state.rag_engine is None:
        with st.spinner("🔄 Inicjalizacja bazy wiedzy..."):
            st.session_state.rag_engine = get_rag_engine()
    return st.session_state.rag_engine

def get_ai_client():
    """Get or initialize AI client"""
    config = st.session_state.config
    if config.openrouter_api_key:
        if st.session_state.ai_client is None:
            st.session_state.ai_client = OpenRouterClient(config.openrouter_api_key)
        return st.session_state.ai_client
    return None

def render_sidebar():
    """Render sidebar with configuration"""
    with st.sidebar:
        st.markdown("## ⚙️ Konfiguracja")
        
        config = st.session_state.config
        
        # API Key input
        api_key = st.text_input(
            "🔑 OpenRouter API Key",
            value=config.openrouter_api_key,
            type="password",
            help="Uzyskaj klucz na https://openrouter.ai/keys"
        )
        
        if api_key != config.openrouter_api_key:
            config.openrouter_api_key = api_key
            st.session_state.ai_client = None  # Reset client
            config.save()
        
        st.markdown("---")
        
        # Model selection with categories
        st.markdown("### 🤖 Wybór modelu AI")
        
        # Group models by tier
        tiers = {
            "🆓 Darmowe": [k for k, v in RAG_OPTIMIZED_MODELS.items() if v['tier'] == 'free'],
            "⚡ Szybkie": [k for k, v in RAG_OPTIMIZED_MODELS.items() if v['tier'] == 'fast'],
            "💎 Premium": [k for k, v in RAG_OPTIMIZED_MODELS.items() if v['tier'] == 'premium'],
            "🔓 Open Source": [k for k, v in RAG_OPTIMIZED_MODELS.items() if v['tier'] == 'open'],
            "💰 Budżetowe": [k for k, v in RAG_OPTIMIZED_MODELS.items() if v['tier'] == 'budget'],
        }
        
        # Flatten for selectbox
        all_models = list(RAG_OPTIMIZED_MODELS.keys())
        
        def format_model(model_id):
            info = RAG_OPTIMIZED_MODELS.get(model_id, {})
            return f"{info.get('name', model_id)} ({info.get('context', '?')})"
        
        selected_model = st.selectbox(
            "Model",
            options=all_models,
            index=all_models.index(config.default_model) if config.default_model in all_models else 0,
            format_func=format_model
        )
        
        if selected_model != config.default_model:
            config.default_model = selected_model
            config.save()
        
        # Show model info
        model_info = RAG_OPTIMIZED_MODELS.get(selected_model, {})
        st.markdown(f"""
        <div class="model-card">
            <b>{model_info.get('name', selected_model)}</b><br>
            <small>
                📊 Kontekst: {model_info.get('context', 'N/A')}<br>
                💵 Koszt: {model_info.get('cost_per_1m_tokens', 'N/A')}<br>
                📝 {model_info.get('description', '')}
            </small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Advanced settings
        with st.expander("⚙️ Zaawansowane"):
            config.temperature = st.slider(
                "Temperatura (kreatywność)",
                0.0, 1.0, config.temperature, 0.1
            )
            
            config.top_k_results = st.slider(
                "Liczba dokumentów RAG",
                1, 10, config.top_k_results
            )
            
            config.max_tokens = st.slider(
                "Max tokenów odpowiedzi",
                500, 8000, config.max_tokens, 500
            )
        
        st.markdown("---")
        
        # Connection status
        st.markdown("### 📊 Status")
        
        # RAG status
        try:
            rag = get_rag()
            stats = rag.get_stats()
            st.success(f"✅ RAG: {stats['total_documents']} dokumentów")
        except Exception as e:
            st.error(f"❌ RAG: {str(e)[:50]}")
        
        # API status
        if config.openrouter_api_key:
            st.success("✅ API Key: skonfigurowany")
        else:
            st.warning("⚠️ API Key: nie ustawiony")

def render_main_chat():
    """Render main chat interface"""
    st.markdown("# 🤖 RAG Knowledge Assistant")
    st.markdown("*Inteligentny asystent z dostępem do Twojej bazy wiedzy*")
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_area(
            "💬 Zadaj pytanie w języku naturalnym:",
            height=100,
            placeholder="Np. 'Jakie są najlepsze praktyki Docker?' lub 'Opisz architekturę backend'",
            key="user_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_only = st.checkbox("🔍 Tylko RAG", help="Pokaż tylko wyniki wyszukiwania bez AI")
        stream_response = st.checkbox("📡 Streaming", value=True, help="Strumieniowanie odpowiedzi")
    
    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
    
    with col_btn1:
        ask_button = st.button("🚀 Zapytaj", type="primary", use_container_width=True)
    
    with col_btn2:
        clear_button = st.button("🗑️ Wyczyść", use_container_width=True)
    
    with col_btn3:
        if st.button("📊 Statystyki", use_container_width=True):
            show_stats()
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    # Process question
    if ask_button and user_input.strip():
        process_question(user_input.strip(), search_only, stream_response)
    
    # Display chat history
    render_chat_history()

def process_question(question: str, search_only: bool, stream: bool):
    """Process user question"""
    config = st.session_state.config
    rag = get_rag()
    
    # Add user message to history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': question,
        'timestamp': datetime.now().isoformat()
    })
    
    if search_only:
        # RAG-only mode
        with st.spinner("🔍 Przeszukuję bazę wiedzy..."):
            results = rag.search(question, top_k=config.top_k_results)
            
            if results:
                response = "📚 **Znalezione dokumenty:**\n\n"
                for i, r in enumerate(results, 1):
                    response += f"**{i}. {r.filename}** (trafność: {r.relevance_score:.2%})\n"
                    response += f"```\n{r.content_preview}\n```\n\n"
            else:
                response = "❌ Nie znaleziono pasujących dokumentów."
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().isoformat(),
                'model': 'RAG Search'
            })
    else:
        # AI + RAG mode
        if not config.openrouter_api_key:
            st.error("❌ Wprowadź OpenRouter API Key w panelu bocznym!")
            return
        
        ai_client = get_ai_client()
        assistant = RAGAssistant(ai_client, rag)
        
        if stream:
            # Streaming response
            response_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("🤖 Generuję odpowiedź..."):
                for chunk in assistant.stream_ask(
                    question,
                    model=config.default_model,
                    top_k=config.top_k_results,
                    temperature=config.temperature,
                    max_tokens=config.max_tokens
                ):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.empty()
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': full_response,
                'timestamp': datetime.now().isoformat(),
                'model': config.default_model
            })
        else:
            # Non-streaming response
            with st.spinner("🤖 Generuję odpowiedź..."):
                response = assistant.ask(
                    question,
                    model=config.default_model,
                    top_k=config.top_k_results,
                    temperature=config.temperature,
                    max_tokens=config.max_tokens
                )
                
                if response.success:
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response.content,
                        'timestamp': datetime.now().isoformat(),
                        'model': config.default_model,
                        'usage': response.usage
                    })
                else:
                    st.error(f"❌ Błąd: {response.error}")
    
    st.rerun()

def render_chat_history():
    """Render chat history"""
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align: center; padding: 50px; color: #888;">
            <h3>👋 Witaj w RAG Knowledge Assistant!</h3>
            <p>Zadaj pytanie, aby rozpocząć rozmowę.</p>
            <p><small>System przeszuka bazę wiedzy i wygeneruje inteligentną odpowiedź.</small></p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("---")
    st.markdown("### 💬 Historia rozmowy")
    
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div class="user-message">
                <b>👤 Ty:</b><br>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            model_name = msg.get('model', 'AI')
            st.markdown(f"""
            <div class="assistant-message">
                <b>🤖 {model_name}:</b>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(msg['content'])

def show_stats():
    """Show knowledge base statistics"""
    rag = get_rag()
    stats = rag.get_stats()
    
    st.markdown("### 📊 Statystyki bazy wiedzy")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_documents']}</div>
            <div class="stat-label">Dokumentów</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        chars = stats['total_characters']
        chars_display = f"{chars/1000:.1f}K" if chars > 1000 else str(chars)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{chars_display}</div>
            <div class="stat-label">Znaków</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['vocabulary_size']}</div>
            <div class="stat-label">Słów w indeksie</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        types_count = len(stats['file_types'])
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{types_count}</div>
            <div class="stat-label">Typów plików</div>
        </div>
        """, unsafe_allow_html=True)
    
    # File types breakdown
    st.markdown("#### 📁 Typy plików")
    for ft, count in stats['file_types'].items():
        st.progress(count / stats['total_documents'], text=f"{ft}: {count} plików")

def main():
    """Main application"""
    init_session_state()
    render_sidebar()
    render_main_chat()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8em;">
        🤖 RAG Knowledge Assistant v2.0 | 
        Powered by OpenRouter | 
        Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

