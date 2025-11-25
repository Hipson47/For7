#!/usr/bin/env python3
"""
RAG API Server - HTTP endpoints for RAG functionality
"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/server.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
Path('logs').mkdir(exist_ok=True)

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
except ImportError:
    logger.error("Flask not installed. Run: pip install flask flask-cors")
    sys.exit(1)

from .rag_engine import get_rag_engine, SearchResult

app = Flask(__name__)
CORS(app)

# Initialize RAG engine
rag_engine = None

def init_rag():
    """Initialize RAG engine"""
    global rag_engine
    if rag_engine is None:
        logger.info("Initializing RAG engine...")
        rag_engine = get_rag_engine()
        logger.info(f"RAG engine ready with {len(rag_engine.documents)} documents")
    return rag_engine

@app.before_request
def ensure_rag_initialized():
    """Ensure RAG is initialized before handling requests"""
    init_rag()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'RAG Knowledge Base Server',
        'version': '2.0.0'
    })

@app.route('/search', methods=['POST'])
def search():
    """
    Search the knowledge base
    
    Request body:
        {
            "query": "search query",
            "top_k": 5,
            "min_score": 0.05
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body required'}), 400
        
        query = data.get('query', '').strip()
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        top_k = data.get('top_k', 5)
        min_score = data.get('min_score', 0.05)
        
        logger.info(f"Search request: '{query[:50]}...' (top_k={top_k})")
        
        results = rag_engine.search(query, top_k=top_k, min_score=min_score)
        
        # Convert SearchResult objects to dicts
        results_data = [
            {
                'filename': r.filename,
                'content_preview': r.content_preview,
                'relevance_score': r.relevance_score,
                'file_type': r.file_type,
                'char_count': r.char_count,
                'document_id': r.document_id
            }
            for r in results
        ]
        
        return jsonify({
            'results': results_data,
            'query': query,
            'count': len(results_data)
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/context', methods=['POST'])
def get_context():
    """
    Get formatted context for AI model
    
    Request body:
        {
            "query": "search query",
            "top_k": 5,
            "max_chars": 8000
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body required'}), 400
        
        query = data.get('query', '').strip()
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        top_k = data.get('top_k', 5)
        max_chars = data.get('max_chars', 8000)
        
        context = rag_engine.get_context_for_query(query, top_k=top_k, max_context_chars=max_chars)
        
        return jsonify({
            'context': context,
            'query': query
        })
        
    except Exception as e:
        logger.error(f"Context error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/files', methods=['GET'])
def list_files():
    """List all indexed files"""
    try:
        files = rag_engine.list_files()
        return jsonify({
            'files': files,
            'count': len(files)
        })
    except Exception as e:
        logger.error(f"Files list error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get knowledge base statistics"""
    try:
        stats = rag_engine.get_stats()
        return jsonify({
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Stats error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/rebuild', methods=['POST'])
def rebuild_index():
    """Rebuild the RAG index"""
    try:
        logger.info("Rebuilding RAG index...")
        rag_engine.initialize(force_rebuild=True)
        return jsonify({
            'status': 'success',
            'documents': len(rag_engine.documents)
        })
    except Exception as e:
        logger.error(f"Rebuild error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET  /health   - Health check',
            'POST /search   - Search knowledge base',
            'POST /context  - Get AI context',
            'GET  /files    - List indexed files',
            'GET  /stats    - Get statistics',
            'POST /rebuild  - Rebuild index'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}", exc_info=True)
    return jsonify({
        'error': 'Internal server error',
        'details': str(error)
    }), 500

def run_server(host: str = '127.0.0.1', port: int = 5001, debug: bool = False):
    """Run the server"""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           🤖 RAG Knowledge Base Server v2.0                  ║
╠══════════════════════════════════════════════════════════════╣
║  Server: http://{host}:{port}                               ║
║                                                              ║
║  Endpoints:                                                  ║
║    GET  /health   - Health check                             ║
║    POST /search   - Search knowledge base                    ║
║    POST /context  - Get AI context                           ║
║    GET  /files    - List indexed files                       ║
║    GET  /stats    - Get statistics                           ║
║    POST /rebuild  - Rebuild index                            ║
║                                                              ║
║  Press Ctrl+C to stop                                        ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    init_rag()
    app.run(host=host, port=port, debug=debug, threaded=True)

if __name__ == '__main__':
    run_server()

