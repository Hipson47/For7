#!/usr/bin/env python3
"""
AI Client - OpenRouter API integration
"""

import logging
import requests
from typing import Optional, Generator, Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

@dataclass
class AIResponse:
    """AI model response"""
    content: str
    model: str
    usage: Dict
    success: bool
    error: Optional[str] = None

class OpenRouterClient:
    """
    OpenRouter API client for AI model access
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = OPENROUTER_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost:8501",
            "X-Title": "RAG Knowledge Assistant"
        })
    
    def _make_request(self, endpoint: str, data: Dict, stream: bool = False) -> requests.Response:
        """Make API request"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.post(url, json=data, stream=stream, timeout=60)
            return response
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Try a faster model or shorter query.")
        except requests.exceptions.ConnectionError:
            raise Exception("Connection error. Check your internet connection.")
    
    def chat_completion(
        self,
        messages: List[Dict],
        model: str = "anthropic/claude-3.5-sonnet",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        stream: bool = False
    ) -> AIResponse:
        """
        Generate chat completion
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model identifier
            temperature: Creativity (0-1)
            max_tokens: Maximum response length
            stream: Whether to stream response
            
        Returns:
            AIResponse object
        """
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        try:
            response = self._make_request("chat/completions", data, stream=stream)
            
            if response.status_code == 200:
                result = response.json()
                return AIResponse(
                    content=result['choices'][0]['message']['content'],
                    model=result.get('model', model),
                    usage=result.get('usage', {}),
                    success=True
                )
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                logger.error(error_msg)
                return AIResponse(
                    content="",
                    model=model,
                    usage={},
                    success=False,
                    error=error_msg
                )
                
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return AIResponse(
                content="",
                model=model,
                usage={},
                success=False,
                error=str(e)
            )
    
    def stream_chat_completion(
        self,
        messages: List[Dict],
        model: str = "anthropic/claude-3.5-sonnet",
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> Generator[str, None, None]:
        """
        Stream chat completion response
        
        Yields:
            Content chunks as they arrive
        """
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        try:
            response = self._make_request("chat/completions", data, stream=True)
            
            if response.status_code != 200:
                yield f"Error: {response.status_code} - {response.text}"
                return
            
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        json_str = line_text[6:]
                        if json_str == '[DONE]':
                            break
                        try:
                            import json
                            chunk = json.loads(json_str)
                            delta = chunk.get('choices', [{}])[0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            response = self.chat_completion(
                messages=[{"role": "user", "content": "Say 'OK'"}],
                model="meta-llama/llama-3.1-8b-instruct",
                max_tokens=10
            )
            return response.success
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_available_models(self) -> List[Dict]:
        """Get list of available models from OpenRouter"""
        try:
            response = self.session.get(f"{self.base_url}/models", timeout=10)
            if response.status_code == 200:
                return response.json().get('data', [])
            return []
        except Exception as e:
            logger.error(f"Failed to get models: {e}")
            return []


class RAGAssistant:
    """
    RAG-powered AI Assistant
    Combines RAG search with AI generation
    """
    
    def __init__(self, ai_client: OpenRouterClient, rag_engine):
        self.ai_client = ai_client
        self.rag_engine = rag_engine
    
    def _build_system_prompt(self, context: str) -> str:
        """Build system prompt with RAG context"""
        return f"""Jesteś Inteligentnym Asystentem Wiedzy, który pomaga użytkownikom na podstawie bogatej bazy wiedzy technicznej.

## Twoje zadania:
1. Analizuj zapytania użytkowników w języku naturalnym
2. Wykorzystuj dostarczony kontekst z bazy wiedzy RAG
3. Generuj pomocne, dokładne odpowiedzi
4. Jeśli kontekst nie zawiera odpowiedzi, powiedz o tym uczciwie
5. Odpowiadaj w języku użytkownika (po polsku na polskie pytania)

## Kontekst zawiera informacje z następujących dziedzin:
- Backend engineering i architektura systemów
- Docker i konteneryzacja
- AI, machine learning i prompt engineering
- Google Cloud Platform
- Best practices programistyczne
- Cursor IDE i narzędzia deweloperskie

## Zasady odpowiedzi:
- Bądź przyjazny i pomocny
- Bądź dokładny i oparty na faktach z kontekstu
- Bądź zwięzły ale kompletny
- Używaj formatowania Markdown dla czytelności
- Cytuj źródła gdy to możliwe (nazwa pliku)

## Kontekst z bazy wiedzy:
{context}

---
Odpowiedz na pytanie użytkownika korzystając z powyższego kontekstu."""
    
    def ask(
        self,
        question: str,
        model: str = "anthropic/claude-3.5-sonnet",
        top_k: int = 5,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> AIResponse:
        """
        Ask a question using RAG
        
        Args:
            question: User's question
            model: AI model to use
            top_k: Number of documents to retrieve
            temperature: AI creativity
            max_tokens: Max response length
            
        Returns:
            AIResponse with the answer
        """
        # Get relevant context from RAG
        context = self.rag_engine.get_context_for_query(question, top_k=top_k)
        
        # Build messages
        messages = [
            {"role": "system", "content": self._build_system_prompt(context)},
            {"role": "user", "content": question}
        ]
        
        # Get AI response
        return self.ai_client.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def stream_ask(
        self,
        question: str,
        model: str = "anthropic/claude-3.5-sonnet",
        top_k: int = 5,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> Generator[str, None, None]:
        """
        Ask a question with streaming response
        
        Yields:
            Response chunks as they arrive
        """
        # Get relevant context from RAG
        context = self.rag_engine.get_context_for_query(question, top_k=top_k)
        
        # Build messages
        messages = [
            {"role": "system", "content": self._build_system_prompt(context)},
            {"role": "user", "content": question}
        ]
        
        # Stream AI response
        yield from self.ai_client.stream_chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

