#!/usr/bin/env python3
"""
🧠 RAG Engine - Semantic Search with Embeddings
Uses sentence-transformers + ChromaDB for high-quality retrieval
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import hashlib

# Configure logging with rich if available
try:
    from rich.logging import RichHandler
    from rich.console import Console
    from rich import print as rprint
    console = Console()
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, console=console)]
    )
    HAS_RICH = True
except ImportError:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    HAS_RICH = False

logger = logging.getLogger(__name__)

# Try to import dependencies
EMBEDDING_AVAILABLE = False
CHROMA_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING_AVAILABLE = True
    logger.info("✅ sentence-transformers available")
except ImportError:
    logger.warning("⚠️ sentence-transformers not available, using TF-IDF fallback")

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
    logger.info("✅ ChromaDB available")
except ImportError:
    logger.warning("⚠️ ChromaDB not available, using in-memory storage")

# Fallback imports
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
    logger.warning("⚠️ PyPDF2 not available, PDF support disabled")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    TFIDF_AVAILABLE = True
except ImportError:
    TFIDF_AVAILABLE = False
    logger.warning("⚠️ scikit-learn not available")


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
    chunk_id: Optional[str] = None


class TextChunker:
    """Intelligent text chunking with overlap"""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Split text into overlapping chunks for better retrieval
        
        Args:
            text: Full document text
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of chunk dictionaries
        """
        if not text or len(text) < 50:
            return []
        
        chunks = []
        start = 0
        chunk_idx = 0
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # Try to find a natural break point (sentence or paragraph)
            if end < len(text):
                # Look for paragraph break
                para_break = text.rfind('\n\n', start, end)
                if para_break > start + self.chunk_size // 2:
                    end = para_break
                else:
                    # Look for sentence break
                    for sep in ['. ', '! ', '? ', '\n']:
                        sent_break = text.rfind(sep, start, end)
                        if sent_break > start + self.chunk_size // 2:
                            end = sent_break + len(sep)
                            break
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunk = {
                    'text': chunk_text,
                    'start': start,
                    'end': end,
                    'chunk_idx': chunk_idx,
                    'char_count': len(chunk_text)
                }
                
                if metadata:
                    chunk.update(metadata)
                
                chunks.append(chunk)
                chunk_idx += 1
            
            # Move start position with overlap
            start = end - self.overlap
            
            # Ensure we make progress
            if start <= 0 and chunk_idx > 0:
                break
        
        return chunks


class RAGEngine:
    """
    Retrieval-Augmented Generation Engine
    Uses semantic embeddings for high-quality search
    """
    
    def __init__(
        self, 
        knowledge_dir: str = ".cursor/knowledge", 
        db_path: str = "./chroma_db",
        collection_name: str = "knowledge_base"
    ):
        self.knowledge_dir = Path(knowledge_dir)
        self.db_path = db_path
        self.collection_name = collection_name
        
        self.chunker = TextChunker(chunk_size=1000, overlap=200)
        self.documents: List[Dict] = []
        self._initialized = False
        
        # Initialize embedding model
        self.embedding_model = None
        if EMBEDDING_AVAILABLE:
            try:
                logger.info("🔄 Loading embedding model...")
                # Use a fast, multilingual model
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ Embedding model loaded: all-MiniLM-L6-v2")
            except Exception as e:
                logger.error(f"❌ Failed to load embedding model: {e}")
        
        # Initialize ChromaDB
        self.chroma_client = None
        self.collection = None
        if CHROMA_AVAILABLE:
            try:
                self.chroma_client = chromadb.PersistentClient(path=self.db_path)
                logger.info(f"✅ ChromaDB initialized at {self.db_path}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize ChromaDB: {e}")
        
        # Fallback to TF-IDF if needed
        self.vectorizer = None
        self.tfidf_matrix = None
        
        logger.info(f"📁 Knowledge directory: {self.knowledge_dir}")
    
    def _hash_content(self, content: str) -> str:
        """Generate hash for content deduplication"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def extract_text_from_pdf(self, pdf_path: Path, max_chars: int = 100000) -> str:
        """Extract text from PDF file"""
        if PyPDF2 is None:
            logger.warning(f"Cannot read PDF {pdf_path}: PyPDF2 not installed")
            return ""
        
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
            logger.error(f"❌ Error reading PDF {pdf_path}: {e}")
            return ""
    
    def extract_text_from_file(self, file_path: Path, max_chars: int = 100000) -> str:
        """Extract text from various file types"""
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            return self.extract_text_from_pdf(file_path, max_chars)
        elif suffix in ['.md', '.txt', '.json', '.py', '.js', '.ts', '.yaml', '.yml']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()[:max_chars]
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        return f.read()[:max_chars]
                except Exception as e:
                    logger.error(f"❌ Error reading {file_path}: {e}")
                    return ""
        return ""
    
    def load_documents(self) -> int:
        """Load all documents from knowledge directory"""
        if not self.knowledge_dir.exists():
            logger.error(f"❌ Knowledge directory not found: {self.knowledge_dir}")
            return 0
        
        logger.info(f"📂 Loading documents from {self.knowledge_dir}")
        
        # Supported file types
        extensions = ['*.pdf', '*.md', '*.txt', '*.json']
        all_files = []
        for ext in extensions:
            all_files.extend(list(self.knowledge_dir.glob(ext)))
            all_files.extend(list(self.knowledge_dir.glob(f"**/{ext}")))  # Recursive
        
        # Remove duplicates
        all_files = list(set(all_files))
        logger.info(f"📄 Found {len(all_files)} files")
        
        self.documents = []
        all_chunks = []
        
        for file_path in all_files:
            text = self.extract_text_from_file(file_path)
            
            if text and len(text) > 50:
                doc_id = self._hash_content(str(file_path))
                
                # Create document metadata
                doc_metadata = {
                    'doc_id': doc_id,
                    'path': str(file_path),
                    'filename': file_path.name,
                    'type': file_path.suffix[1:] if file_path.suffix else 'unknown'
                }
                
                # Store full document
                document = {
                    **doc_metadata,
                    'content': text,
                    'char_count': len(text)
                }
                self.documents.append(document)
                
                # Chunk the document
                chunks = self.chunker.chunk_text(text, doc_metadata)
                all_chunks.extend(chunks)
                
                logger.debug(f"✅ Loaded: {file_path.name} ({len(text)} chars, {len(chunks)} chunks)")
        
        total_chars = sum(doc['char_count'] for doc in self.documents)
        logger.info(f"📚 Loaded {len(self.documents)} documents ({total_chars:,} chars, {len(all_chunks)} chunks)")
        
        # Index chunks
        if all_chunks:
            self._index_chunks(all_chunks)
        
        return len(self.documents)
    
    def _index_chunks(self, chunks: List[Dict]) -> None:
        """Index chunks using ChromaDB or TF-IDF fallback"""
        
        if self.chroma_client and self.embedding_model:
            # Use ChromaDB with embeddings
            logger.info("🔄 Indexing with ChromaDB + embeddings...")
            
            try:
                # Delete existing collection if it exists
                try:
                    self.chroma_client.delete_collection(self.collection_name)
                except:
                    pass
                
                # Create new collection
                self.collection = self.chroma_client.create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
                
                # Prepare data for ChromaDB
                ids = []
                documents = []
                metadatas = []
                
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{chunk.get('doc_id', 'doc')}_{chunk.get('chunk_idx', i)}"
                    ids.append(chunk_id)
                    documents.append(chunk['text'])
                    metadatas.append({
                        'filename': chunk.get('filename', 'unknown'),
                        'doc_id': chunk.get('doc_id', ''),
                        'chunk_idx': chunk.get('chunk_idx', i),
                        'char_count': chunk.get('char_count', 0),
                        'type': chunk.get('type', 'unknown')
                    })
                
                # Generate embeddings
                logger.info(f"🧮 Generating embeddings for {len(documents)} chunks...")
                embeddings = self.embedding_model.encode(documents, show_progress_bar=True)
                
                # Add to collection in batches
                batch_size = 100
                for i in range(0, len(ids), batch_size):
                    end = min(i + batch_size, len(ids))
                    self.collection.add(
                        ids=ids[i:end],
                        documents=documents[i:end],
                        embeddings=embeddings[i:end].tolist(),
                        metadatas=metadatas[i:end]
                    )
                
                logger.info(f"✅ Indexed {len(ids)} chunks in ChromaDB")
                return
                
            except Exception as e:
                logger.error(f"❌ ChromaDB indexing failed: {e}")
                logger.info("⚠️ Falling back to TF-IDF...")
        
        # Fallback to TF-IDF
        if TFIDF_AVAILABLE:
            logger.info("🔄 Indexing with TF-IDF (fallback)...")
            
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95
            )
            
            chunk_texts = [c['text'] for c in chunks]
            self.tfidf_matrix = self.vectorizer.fit_transform(chunk_texts)
            self._chunks = chunks  # Store for retrieval
            
            logger.info(f"✅ TF-IDF matrix: {self.tfidf_matrix.shape}")
        else:
            logger.error("❌ No indexing method available!")
    
    def initialize(self, force_rebuild: bool = False) -> None:
        """Initialize the RAG engine"""
        if self._initialized and not force_rebuild:
            logger.info("✅ RAG engine already initialized")
            return
        
        # Check if ChromaDB collection exists
        if self.chroma_client and not force_rebuild:
            try:
                self.collection = self.chroma_client.get_collection(self.collection_name)
                count = self.collection.count()
                if count > 0:
                    logger.info(f"✅ Loaded existing ChromaDB collection ({count} chunks)")
                    # Load document metadata
                    self._load_document_metadata()
                    self._initialized = True
                    return
            except:
                pass
        
        logger.info("🔄 Building new RAG index...")
        self.load_documents()
        self._initialized = True
        logger.info("✅ RAG engine ready!")
    
    def _load_document_metadata(self) -> None:
        """Load document metadata from files"""
        if not self.knowledge_dir.exists():
            return
        
        extensions = ['*.pdf', '*.md', '*.txt', '*.json']
        all_files = []
        for ext in extensions:
            all_files.extend(list(self.knowledge_dir.glob(ext)))
            all_files.extend(list(self.knowledge_dir.glob(f"**/{ext}")))
        
        all_files = list(set(all_files))
        
        self.documents = []
        for file_path in all_files:
            text = self.extract_text_from_file(file_path)
            if text and len(text) > 50:
                doc_id = self._hash_content(str(file_path))
                self.documents.append({
                    'doc_id': doc_id,
                    'path': str(file_path),
                    'filename': file_path.name,
                    'content': text,
                    'type': file_path.suffix[1:] if file_path.suffix else 'unknown',
                    'char_count': len(text)
                })
    
    def search(self, query: str, top_k: int = 5, min_score: float = 0.1) -> List[SearchResult]:
        """
        Search for relevant chunks using semantic search
        
        Args:
            query: Search query
            top_k: Maximum number of results
            min_score: Minimum relevance score
            
        Returns:
            List of SearchResult objects
        """
        if not self._initialized:
            self.initialize()
        
        results = []
        
        # Try ChromaDB first
        if self.collection and self.embedding_model:
            try:
                # Generate query embedding
                query_embedding = self.embedding_model.encode([query])[0]
                
                # Search ChromaDB
                search_results = self.collection.query(
                    query_embeddings=[query_embedding.tolist()],
                    n_results=top_k,
                    include=['documents', 'metadatas', 'distances']
                )
                
                if search_results and search_results['documents']:
                    for i, doc in enumerate(search_results['documents'][0]):
                        metadata = search_results['metadatas'][0][i]
                        distance = search_results['distances'][0][i]
                        
                        # Convert distance to similarity score (cosine distance -> similarity)
                        score = 1 - distance
                        
                        if score >= min_score:
                            results.append(SearchResult(
                                filename=metadata.get('filename', 'unknown'),
                                content_preview=doc[:500] + "..." if len(doc) > 500 else doc,
                                full_content=doc,
                                relevance_score=float(score),
                                file_type=metadata.get('type', 'unknown'),
                                char_count=metadata.get('char_count', len(doc)),
                                document_id=metadata.get('doc_id', ''),
                                chunk_id=search_results['ids'][0][i] if search_results['ids'] else None
                            ))
                
                logger.info(f"🔍 Search '{query[:40]}...' → {len(results)} results (ChromaDB)")
                return results
                
            except Exception as e:
                logger.error(f"❌ ChromaDB search failed: {e}")
        
        # Fallback to TF-IDF
        if self.vectorizer and self.tfidf_matrix is not None:
            try:
                query_vector = self.vectorizer.transform([query])
                similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
                
                top_indices = np.argsort(similarities)[-top_k:][::-1]
                
                for idx in top_indices:
                    score = float(similarities[idx])
                    if score >= min_score:
                        chunk = self._chunks[idx]
                        content = chunk['text']
                        
                        results.append(SearchResult(
                            filename=chunk.get('filename', 'unknown'),
                            content_preview=content[:500] + "..." if len(content) > 500 else content,
                            full_content=content,
                            relevance_score=score,
                            file_type=chunk.get('type', 'unknown'),
                            char_count=chunk.get('char_count', len(content)),
                            document_id=chunk.get('doc_id', ''),
                            chunk_id=f"{chunk.get('doc_id', '')}_{chunk.get('chunk_idx', idx)}"
                        ))
                
                logger.info(f"🔍 Search '{query[:40]}...' → {len(results)} results (TF-IDF)")
                
            except Exception as e:
                logger.error(f"❌ TF-IDF search failed: {e}")
        
        return results
    
    def get_context_for_query(self, query: str, top_k: int = 5, max_context_chars: int = 8000) -> str:
        """
        Get formatted context string for AI model
        
        Args:
            query: Search query
            top_k: Number of chunks to include
            max_context_chars: Maximum total context length
            
        Returns:
            Formatted context string
        """
        results = self.search(query, top_k=top_k)
        
        if not results:
            return "No relevant information found in the knowledge base."
        
        context_parts = []
        total_chars = 0
        seen_docs = set()
        
        for i, result in enumerate(results, 1):
            available = max_context_chars - total_chars
            if available <= 0:
                break
            
            # Deduplicate by document
            doc_key = f"{result.filename}_{result.document_id}"
            if doc_key in seen_docs:
                continue
            seen_docs.add(doc_key)
            
            content = result.full_content[:available]
            part = f"""
📄 Source {i}: {result.filename} (relevance: {result.relevance_score:.2%})
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
            ft = doc.get('type', 'unknown').upper()
            file_types[ft] = file_types.get(ft, 0) + 1
        
        chunk_count = 0
        if self.collection:
            try:
                chunk_count = self.collection.count()
            except:
                pass
        elif hasattr(self, '_chunks'):
            chunk_count = len(self._chunks)
        
        return {
            'total_documents': len(self.documents),
            'total_characters': sum(doc.get('char_count', 0) for doc in self.documents),
            'total_chunks': chunk_count,
            'file_types': file_types,
            'embedding_model': 'all-MiniLM-L6-v2' if self.embedding_model else 'TF-IDF',
            'storage': 'ChromaDB' if self.collection else 'In-Memory'
        }
    
    def list_files(self) -> List[Dict]:
        """List all indexed files"""
        if not self._initialized:
            self.initialize()
        
        return [
            {
                'filename': doc.get('filename', 'unknown'),
                'type': doc.get('type', 'unknown'),
                'char_count': doc.get('char_count', 0),
                'id': doc.get('doc_id', '')
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
