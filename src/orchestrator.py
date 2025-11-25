#!/usr/bin/env python3
"""
🎯 Knowledge Orchestrator - Central coordination layer for RAG + LLM

This module provides an orchestration layer that:
- Decides how to use the RAG engine based on user queries
- Manages context retrieval and LLM interactions
- Returns structured results with answer, sources, and debug metadata
- Is designed for future extensibility (additional tools, multi-step reasoning)
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class OrchestratorResult:
    """
    Structured result from the Orchestrator.
    
    Attributes:
        answer: The generated response text
        sources: List of source documents used (filename, score, snippet, type)
        model: The AI model used for generation
        usage: Token usage statistics from the LLM
        steps: List of orchestration steps taken (for debugging/transparency)
        success: Whether the orchestration completed successfully
        error: Error message if orchestration failed
    """
    answer: str
    sources: List[Dict[str, Any]]
    model: str
    usage: Dict[str, Any]
    steps: List[Dict[str, Any]] = field(default_factory=list)
    success: bool = True
    error: Optional[str] = None


@dataclass
class OrchestrationStep:
    """
    A single step in the orchestration process.
    
    Attributes:
        step_type: Type of step (e.g., 'rag_search', 'llm_call', 'context_build')
        description: Human-readable description of what happened
        duration_ms: Time taken for this step in milliseconds
        metadata: Additional step-specific data
    """
    step_type: str
    description: str
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "type": self.step_type,
            "description": self.description,
            "duration_ms": round(self.duration_ms, 2),
            "metadata": self.metadata
        }


class KnowledgeOrchestrator:
    """
    Orchestrates conversation flow between user, RAG engine, and LLM.
    
    This is the central coordination layer that:
    1. Receives user messages and chat history
    2. Decides which tools to use (currently: RAG search)
    3. Builds appropriate context for the LLM
    4. Calls the LLM and returns structured results
    
    Design for extensibility:
    - Add new tools by creating _run_<tool>_tool() methods
    - Modify orchestration strategy in handle_message()
    - Steps list provides transparency for debugging
    
    Example usage:
        orchestrator = KnowledgeOrchestrator(rag_engine, ai_client, config)
        result = orchestrator.handle_message("What is RAG?", chat_history=[])
        print(result.answer)
        print(result.sources)
    """
    
    # System prompt template for RAG-augmented responses
    SYSTEM_PROMPT_TEMPLATE = """You are an intelligent knowledge assistant. Answer based on the provided context from the knowledge base.

Rules:
- Answer in the user's language (Polish for Polish questions, English for English)
- Be concise but comprehensive
- Use Markdown formatting for readability
- Cite sources when possible (mention the filename)
- If context doesn't contain the answer, say so honestly

Context from knowledge base:
{context}"""

    def __init__(self, rag_engine, ai_client, config):
        """
        Initialize the Knowledge Orchestrator.
        
        Args:
            rag_engine: RAGEngine instance for semantic search
            ai_client: OpenRouterClient instance for LLM calls
            config: AppConfig instance with model settings
        """
        self.rag = rag_engine
        self.ai_client = ai_client
        self.config = config
        
        logger.info("🎯 KnowledgeOrchestrator initialized")
    
    def handle_message(
        self, 
        user_message: str, 
        chat_history: Optional[List[Dict[str, str]]] = None,
        model: Optional[str] = None
    ) -> OrchestratorResult:
        """
        Main orchestration method - processes a user message and returns a response.
        
        This method:
        1. Runs RAG search to find relevant context
        2. Builds a system prompt with the context
        3. Calls the LLM to generate a response
        4. Returns structured result with answer, sources, and metadata
        
        Args:
            user_message: The user's question or message
            chat_history: Optional list of previous messages (for context)
            model: Optional model override (uses config.default_model if not provided)
            
        Returns:
            OrchestratorResult with answer, sources, model info, usage stats, and steps
        """
        import time
        
        steps: List[Dict[str, Any]] = []
        sources: List[Dict[str, Any]] = []
        context = "No context available."
        
        # Use provided model or fall back to config default
        selected_model = model or self.config.default_model
        
        # Step 1: RAG Search
        try:
            rag_result = self._run_rag_tool(user_message)
            steps.append(rag_result["step"])
            sources = rag_result["sources"]
            context = rag_result["context"]
        except Exception as e:
            logger.error(f"❌ RAG search failed: {e}")
            steps.append(OrchestrationStep(
                step_type="rag_search",
                description=f"RAG search failed: {str(e)}",
                metadata={"error": str(e)}
            ).to_dict())
        
        # Step 2: Build LLM messages
        start_time = time.time()
        
        system_prompt = self.SYSTEM_PROMPT_TEMPLATE.format(context=context)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        build_time = (time.time() - start_time) * 1000
        steps.append(OrchestrationStep(
            step_type="context_build",
            description=f"Built system prompt with {len(context)} chars of context",
            duration_ms=build_time,
            metadata={
                "context_length": len(context),
                "sources_count": len(sources),
                "model": selected_model
            }
        ).to_dict())
        
        # Step 3: Call LLM
        try:
            llm_result = self._run_llm_tool(
                messages=messages,
                model=selected_model
            )
            steps.append(llm_result["step"])
            
            if llm_result["success"]:
                return OrchestratorResult(
                    answer=llm_result["content"],
                    sources=sources,
                    model=llm_result["model"],
                    usage=llm_result["usage"],
                    steps=steps,
                    success=True
                )
            else:
                return OrchestratorResult(
                    answer=f"❌ **Error:** {llm_result['error']}",
                    sources=sources,
                    model=selected_model,
                    usage={},
                    steps=steps,
                    success=False,
                    error=llm_result["error"]
                )
                
        except Exception as e:
            logger.error(f"❌ LLM call failed: {e}")
            steps.append(OrchestrationStep(
                step_type="llm_call",
                description=f"LLM call failed: {str(e)}",
                metadata={"error": str(e)}
            ).to_dict())
            
            return OrchestratorResult(
                answer=f"❌ **Error:** {str(e)}",
                sources=sources,
                model=selected_model,
                usage={},
                steps=steps,
                success=False,
                error=str(e)
            )
    
    def _run_rag_tool(self, query: str) -> Dict[str, Any]:
        """
        Execute RAG search tool.
        
        This is a dedicated helper method for RAG operations,
        making it easy to extend or modify RAG behavior.
        
        Args:
            query: Search query
            
        Returns:
            Dict with 'step', 'sources', and 'context' keys
        """
        import time
        start_time = time.time()
        
        top_k = self.config.top_k_results
        min_score = self.config.min_relevance_score
        
        # Execute search
        search_results = self.rag.search(
            query=query,
            top_k=top_k,
            min_score=min_score
        )
        
        # Build sources list
        sources = []
        if search_results:
            sources = [
                {
                    "filename": r.filename,
                    "score": r.relevance_score,
                    "snippet": r.content_preview[:400] + "..." if len(r.content_preview) > 400 else r.content_preview,
                    "type": r.file_type
                }
                for r in search_results
            ]
            context = self.rag.get_context_for_query(query, top_k=top_k)
        else:
            context = "No relevant information found in the knowledge base."
        
        duration_ms = (time.time() - start_time) * 1000
        
        step = OrchestrationStep(
            step_type="rag_search",
            description=f"Found {len(search_results)} relevant chunks" if search_results else "No relevant chunks found",
            duration_ms=duration_ms,
            metadata={
                "query": query[:100] + "..." if len(query) > 100 else query,
                "top_k": top_k,
                "min_score": min_score,
                "results_count": len(search_results) if search_results else 0,
                "top_score": round(search_results[0].relevance_score, 3) if search_results else 0
            }
        ).to_dict()
        
        return {
            "step": step,
            "sources": sources,
            "context": context
        }
    
    def _run_llm_tool(
        self, 
        messages: List[Dict[str, str]], 
        model: str
    ) -> Dict[str, Any]:
        """
        Execute LLM call tool.
        
        This is a dedicated helper method for LLM operations,
        making it easy to extend or modify LLM behavior.
        
        Args:
            messages: List of message dicts for the LLM
            model: Model identifier to use
            
        Returns:
            Dict with 'step', 'success', 'content', 'model', 'usage', and optionally 'error'
        """
        import time
        start_time = time.time()
        
        response = self.ai_client.chat_completion(
            messages=messages,
            model=model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            stream=False
        )
        
        duration_ms = (time.time() - start_time) * 1000
        
        if response.success:
            step = OrchestrationStep(
                step_type="llm_call",
                description=f"Generated response using {response.model}",
                duration_ms=duration_ms,
                metadata={
                    "model": response.model,
                    "usage": response.usage,
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens
                }
            ).to_dict()
            
            return {
                "step": step,
                "success": True,
                "content": response.content,
                "model": response.model,
                "usage": response.usage
            }
        else:
            step = OrchestrationStep(
                step_type="llm_call",
                description=f"LLM call failed: {response.error}",
                duration_ms=duration_ms,
                metadata={
                    "model": model,
                    "error": response.error
                }
            ).to_dict()
            
            return {
                "step": step,
                "success": False,
                "content": "",
                "model": model,
                "usage": {},
                "error": response.error
            }
    
    def get_orchestrator_info(self) -> Dict[str, Any]:
        """
        Get information about the orchestrator configuration.
        
        Returns:
            Dict with orchestrator settings and capabilities
        """
        return {
            "version": "1.0.0",
            "capabilities": ["rag_search", "llm_call"],
            "config": {
                "default_model": self.config.default_model,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                "top_k_results": self.config.top_k_results,
                "min_relevance_score": self.config.min_relevance_score
            },
            "rag_stats": self.rag.get_stats() if self.rag else {}
        }

