#!/usr/bin/env python3
"""
RAG Engine - Core retrieval and search functionality
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import hashlib

logger = logging.getLogger(__name__)

# Try to import dependencies
try:
    import PyPDF2
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    from scipy.sparse import csr_matrix
except ImportError as e:
    logger.error(f"Missing dependencies: {e}")
    logger.error("Install with: pip install PyPDF2 scikit-learn numpy scipy")
    raise

@dataclass
class SearchResult:
    """Single search result"""
    filename: str
    content_preview: str
    full_content: str
    relevance_score: float
    file_type: str
    char_count: int
    document_id: str

class RAGEngine:
    """
    Retrieval-Augmented Generation Engine
    Handles document loading, indexing, and semantic search
    """
    
    def __init__(self, knowledge_dir: str = ".cursor/knowledge", index_file: str = "rag_index.json"):
        self.knowledge_dir = Path(knowledge_dir)
        self.index_file = Path(index_file)
        self.documents: List[Dict] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self._initialized = False
        
        logger.info(f"RAG Engine initialized with knowledge_dir: {knowledge_dir}")
    
    def _hash_content(self, content: str) -> str:
        """Generate hash for content deduplication"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def extract_text_from_pdf(self, pdf_path: Path, max_chars: int = 50000) -> str:
        """Extract text from PDF file with size limit"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_parts = []
                current_chars = 0
                
                for page in pdf_reader.pages:
                    if current_chars >= max_chars:
                        break
                    page_text = page.extract_text() or ""
                    text_parts.append(page_text)
                    current_chars += len(page_text)
                
                return "\n".join(text_parts).strip()[:max_chars]
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    def extract_text_from_file(self, file_path: Path, max_chars: int = 100000) -> str:
        """Extract text from various file types"""
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif suffix in ['.md', '.txt', '.json', '.py', '.js', '.ts']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()[:max_chars]
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        return f.read()[:max_chars]
                except Exception as e:
                    logger.error(f"Error reading {file_path}: {e}")
                    return ""
        return ""
    
    def load_documents(self) -> int:
        """Load all documents from knowledge directory"""
        if not self.knowledge_dir.exists():
            logger.error(f"Knowledge directory not found: {self.knowledge_dir}")
            return 0
        
        logger.info(f"Loading documents from {self.knowledge_dir}")
        
        # Supported file types
        extensions = ['*.pdf', '*.md', '*.txt', '*.json']
        all_files = []
        for ext in extensions:
            all_files.extend(list(self.knowledge_dir.glob(ext)))
        
        logger.info(f"Found {len(all_files)} files")
        
        self.documents = []
        for file_path in all_files:
            text = self.extract_text_from_file(file_path)
            
            if text and len(text) > 50:
                doc_id = self._hash_content(text)
                document = {
                    'id': doc_id,
                    'path': str(file_path),
                    'filename': file_path.name,
                    'content': text,
                    'type': file_path.suffix[1:] if file_path.suffix else 'unknown',
                    'char_count': len(text)
                }
                self.documents.append(document)
                logger.debug(f"Loaded: {file_path.name} ({len(text)} chars)")
        
        total_chars = sum(doc['char_count'] for doc in self.documents)
        logger.info(f"Loaded {len(self.documents)} documents ({total_chars:,} total characters)")
        
        return len(self.documents)
    
    def create_vectors(self) -> None:
        """Create TF-IDF vectors from documents"""
        if not self.documents:
            raise ValueError("No documents loaded. Call load_documents() first.")
        
        logger.info("Creating TF-IDF vectors...")
        
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        
        doc_texts = [doc['content'] for doc in self.documents]
        self.tfidf_matrix = self.vectorizer.fit_transform(doc_texts)
        
        logger.info(f"TF-IDF matrix shape: {self.tfidf_matrix.shape}")
        logger.info(f"Vocabulary size: {len(self.vectorizer.vocabulary_)}")
    
    def save_index(self) -> None:
        """Save index to disk for faster loading"""
        logger.info(f"Saving index to {self.index_file}")
        
        tfidf_data = {
            'data': self.tfidf_matrix.data.tolist(),
            'indices': self.tfidf_matrix.indices.tolist(),
            'indptr': self.tfidf_matrix.indptr.tolist(),
            'shape': list(self.tfidf_matrix.shape)
        }
        
        vocabulary = {str(k): int(v) for k, v in self.vectorizer.vocabulary_.items()}
        
        data = {
            'documents': self.documents,
            'tfidf_data': tfidf_data,
            'vocabulary': vocabulary,
            'version': '2.0'
        }
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        
        logger.info("Index saved successfully")
    
    def load_index(self) -> bool:
        """Load index from disk"""
        if not self.index_file.exists():
            return False
        
        logger.info(f"Loading index from {self.index_file}")
        
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.documents = data['documents']
            
            # Reconstruct TF-IDF matrix
            tfidf_data = data['tfidf_data']
            self.tfidf_matrix = csr_matrix(
                (tfidf_data['data'], tfidf_data['indices'], tfidf_data['indptr']),
                shape=tuple(tfidf_data['shape'])
            )
            
            # Reconstruct vectorizer - need to fit it with vocabulary
            vocabulary = data['vocabulary']
            self.vectorizer = TfidfVectorizer(
                vocabulary=vocabulary,
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Fit the vectorizer on dummy data to initialize it properly
            # Then set the vocabulary and idf weights
            doc_texts = [doc['content'] for doc in self.documents]
            self.vectorizer.fit(doc_texts)
            
            logger.info(f"Loaded {len(self.documents)} documents from index")
            return True
            
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def initialize(self, force_rebuild: bool = False) -> None:
        """Initialize the RAG engine"""
        if self._initialized and not force_rebuild:
            logger.info("RAG engine already initialized")
            return
        
        if not force_rebuild and self.load_index():
            logger.info("RAG engine loaded from existing index")
        else:
            logger.info("Building new RAG index...")
            self.load_documents()
            if self.documents:
                self.create_vectors()
                self.save_index()
            else:
                logger.warning("No documents found!")
        
        self._initialized = True
        logger.info("RAG engine ready!")
    
    def search(self, query: str, top_k: int = 5, min_score: float = 0.05) -> List[SearchResult]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            top_k: Maximum number of results
            min_score: Minimum relevance score (0-1)
            
        Returns:
            List of SearchResult objects
        """
        if not self._initialized:
            self.initialize()
        
        if self.vectorizer is None or self.tfidf_matrix is None:
            logger.error("RAG engine not properly initialized")
            return []
        
        # Transform query to vector
        query_vector = self.vectorizer.transform([query])
        
        # Calculate cosine similarities
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        
        # Get top results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= min_score:
                doc = self.documents[idx]
                content = doc['content']
                preview = content[:500] + "..." if len(content) > 500 else content
                
                results.append(SearchResult(
                    filename=doc['filename'],
                    content_preview=preview,
                    full_content=content,
                    relevance_score=score,
                    file_type=doc['type'],
                    char_count=doc['char_count'],
                    document_id=doc['id']
                ))
        
        logger.info(f"Search '{query[:50]}...' returned {len(results)} results")
        return results
    
    def get_context_for_query(self, query: str, top_k: int = 5, max_context_chars: int = 8000) -> str:
        """
        Get formatted context string for AI model
        
        Args:
            query: Search query
            top_k: Number of documents to include
            max_context_chars: Maximum total context length
            
        Returns:
            Formatted context string
        """
        results = self.search(query, top_k=top_k)
        
        if not results:
            return "No relevant information found in the knowledge base."
        
        context_parts = []
        total_chars = 0
        
        for i, result in enumerate(results, 1):
            # Calculate available space
            available = max_context_chars - total_chars
            if available <= 0:
                break
            
            # Format result
            content = result.full_content[:available]
            part = f"""
--- Document {i}: {result.filename} (relevance: {result.relevance_score:.2f}) ---
{content}
"""
            context_parts.append(part)
            total_chars += len(part)
        
        return "\n".join(context_parts)
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        if not self._initialized:
            self.initialize()
        
        file_types = {}
        for doc in self.documents:
            ft = doc['type'].upper()
            file_types[ft] = file_types.get(ft, 0) + 1
        
        return {
            'total_documents': len(self.documents),
            'total_characters': sum(doc['char_count'] for doc in self.documents),
            'file_types': file_types,
            'vocabulary_size': len(self.vectorizer.vocabulary_) if self.vectorizer else 0,
            'tfidf_shape': list(self.tfidf_matrix.shape) if self.tfidf_matrix is not None else [0, 0]
        }
    
    def list_files(self) -> List[Dict]:
        """List all indexed files"""
        if not self._initialized:
            self.initialize()
        
        return [
            {
                'filename': doc['filename'],
                'type': doc['type'],
                'char_count': doc['char_count'],
                'id': doc['id']
            }
            for doc in self.documents
        ]


# Global singleton instance
_engine_instance: Optional[RAGEngine] = None

def get_rag_engine() -> RAGEngine:
    """Get or create the global RAG engine instance"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = RAGEngine()
        _engine_instance.initialize()
    return _engine_instance

def search_knowledge(query: str, top_k: int = 5) -> List[SearchResult]:
    """Convenience function for searching"""
    engine = get_rag_engine()
    return engine.search(query, top_k=top_k)

def get_context(query: str, top_k: int = 5) -> str:
    """Convenience function for getting AI context"""
    engine = get_rag_engine()
    return engine.get_context_for_query(query, top_k=top_k)

