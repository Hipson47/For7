#!/usr/bin/env python3
"""
Configuration management for RAG Knowledge Assistant
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

# Default configuration values
DEFAULT_CONFIG = {
    "openrouter_api_key": "",
    "rag_server_url": "http://127.0.0.1:5001",
    "default_model": "anthropic/claude-3.5-sonnet",
    "temperature": 0.7,
    "max_tokens": 4000,
    "top_k_results": 5,
    "min_relevance_score": 0.1,
    "theme": "dark",
    "language": "pl"
}

# Best models for RAG from OpenRouter (researched 2024-2025)
# Models with large context windows and good instruction following
RAG_OPTIMIZED_MODELS = {
    # Premium tier - best for complex RAG
    "anthropic/claude-3.5-sonnet": {
        "name": "Claude 3.5 Sonnet",
        "provider": "Anthropic",
        "context": "200K",
        "tier": "premium",
        "description": "Best for complex analysis and long context",
        "cost_per_1m_tokens": "$3.00 / $15.00"
    },
    "anthropic/claude-3-haiku": {
        "name": "Claude 3 Haiku",
        "provider": "Anthropic",
        "context": "200K",
        "tier": "fast",
        "description": "Fast and efficient for simple queries",
        "cost_per_1m_tokens": "$0.25 / $1.25"
    },
    "openai/gpt-4o": {
        "name": "GPT-4o",
        "provider": "OpenAI",
        "context": "128K",
        "tier": "premium",
        "description": "Versatile and intelligent",
        "cost_per_1m_tokens": "$2.50 / $10.00"
    },
    "openai/gpt-4o-mini": {
        "name": "GPT-4o Mini",
        "provider": "OpenAI",
        "context": "128K",
        "tier": "fast",
        "description": "Cost-effective for most tasks",
        "cost_per_1m_tokens": "$0.15 / $0.60"
    },
    # Google tier
    "google/gemini-2.0-flash-exp:free": {
        "name": "Gemini 2.0 Flash (Free)",
        "provider": "Google",
        "context": "1M",
        "tier": "free",
        "description": "Free tier, massive context window",
        "cost_per_1m_tokens": "Free"
    },
    "google/gemini-pro-1.5": {
        "name": "Gemini Pro 1.5",
        "provider": "Google",
        "context": "2M",
        "tier": "premium",
        "description": "Largest context window available",
        "cost_per_1m_tokens": "$1.25 / $5.00"
    },
    # Open source tier
    "meta-llama/llama-3.1-70b-instruct": {
        "name": "Llama 3.1 70B",
        "provider": "Meta",
        "context": "128K",
        "tier": "open",
        "description": "Strong open-source model",
        "cost_per_1m_tokens": "$0.35 / $0.40"
    },
    "meta-llama/llama-3.1-8b-instruct": {
        "name": "Llama 3.1 8B",
        "provider": "Meta",
        "context": "128K",
        "tier": "fast",
        "description": "Fast open-source model",
        "cost_per_1m_tokens": "$0.06 / $0.06"
    },
    # Specialized models
    "mistralai/mistral-large": {
        "name": "Mistral Large",
        "provider": "Mistral",
        "context": "128K",
        "tier": "premium",
        "description": "European AI, strong reasoning",
        "cost_per_1m_tokens": "$2.00 / $6.00"
    },
    "qwen/qwen-2.5-72b-instruct": {
        "name": "Qwen 2.5 72B",
        "provider": "Alibaba",
        "context": "128K",
        "tier": "premium",
        "description": "Strong multilingual model",
        "cost_per_1m_tokens": "$0.35 / $0.40"
    },
    # Budget tier
    "deepseek/deepseek-chat": {
        "name": "DeepSeek Chat",
        "provider": "DeepSeek",
        "context": "64K",
        "tier": "budget",
        "description": "Very cost-effective",
        "cost_per_1m_tokens": "$0.14 / $0.28"
    },
    # xAI Grok models
    "x-ai/grok-4.1-fast": {
        "name": "Grok 4.1 Fast",
        "provider": "xAI",
        "context": "2M",
        "tier": "premium",
        "description": "xAI's best agentic model, 2M context, real-time data",
        "cost_per_1m_tokens": "$3.00 / $15.00"
    },
    "x-ai/grok-3-mini-beta": {
        "name": "Grok 3 Mini",
        "provider": "xAI",
        "context": "128K",
        "tier": "fast",
        "description": "Fast reasoning model from xAI",
        "cost_per_1m_tokens": "$0.30 / $0.50"
    }
}

@dataclass
class AppConfig:
    """Application configuration"""
    openrouter_api_key: str = ""
    rag_server_url: str = "http://127.0.0.1:5001"
    default_model: str = "anthropic/claude-3.5-sonnet"
    temperature: float = 0.7
    max_tokens: int = 4000
    top_k_results: int = 5
    min_relevance_score: float = 0.1
    theme: str = "dark"
    language: str = "pl"
    
    @classmethod
    def get_config_path(cls) -> Path:
        """Get configuration file path"""
        config_dir = Path.home() / ".rag_assistant"
        config_dir.mkdir(exist_ok=True)
        return config_dir / "config.json"
    
    @classmethod
    def load(cls) -> "AppConfig":
        """Load configuration from file"""
        config_path = cls.get_config_path()
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Configuration loaded from {config_path}")
                    return cls(**{k: v for k, v in data.items() if k in DEFAULT_CONFIG})
            except Exception as e:
                logger.warning(f"Error loading config: {e}, using defaults")
        
        # Try environment variables
        env_api_key = os.getenv('OPENROUTER_API_KEY', '')
        
        return cls(openrouter_api_key=env_api_key)
    
    def save(self) -> None:
        """Save configuration to file"""
        config_path = self.get_config_path()
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self), f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration saved to {config_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def is_configured(self) -> bool:
        """Check if essential configuration is set"""
        return bool(self.openrouter_api_key)

def get_models_by_tier(tier: str = None) -> Dict:
    """Get models filtered by tier"""
    if tier is None:
        return RAG_OPTIMIZED_MODELS
    
    return {
        k: v for k, v in RAG_OPTIMIZED_MODELS.items() 
        if v.get('tier') == tier
    }

def get_model_info(model_id: str) -> Optional[Dict]:
    """Get information about a specific model"""
    return RAG_OPTIMIZED_MODELS.get(model_id)

