"""
FAISS Knowledge Base Manager
Handles FAISS vector database operations for university and visa information
"""
import os
import pickle
import numpy as np
import faiss
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FAISSKnowledgeBase:
    """FAISS Knowledge Base Manager for university and visa information"""
    
    def __init__(self, knowledge_base_path: str = "KnowledgeBase"):
        """
        Initialize FAISS Knowledge Base
        
        Args:
            knowledge_base_path: Path to the KnowledgeBase directory
        """
        self.knowledge_base_path = knowledge_base_path
        self.university_index = None
        self.visa_index = None
        self.university_metadata = None
        self.visa_metadata = None
        self.embedding_model = None
        
        # Initialize the knowledge base (lazy loading)
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load FAISS indices and metadata"""
        try:
            # Load university index and metadata
            university_index_path = os.path.join(self.knowledge_base_path, "faiss_universities_index.index")
            university_metadata_path = os.path.join(self.knowledge_base_path, "faiss_universities_index_metadata.pkl")
            
            if os.path.exists(university_index_path) and os.path.exists(university_metadata_path):
                self.university_index = faiss.read_index(university_index_path)
                with open(university_metadata_path, 'rb') as f:
                    self.university_metadata = pickle.load(f)
                logger.info(f"✅ Loaded university index with {self.university_index.ntotal} vectors")
            else:
                logger.warning("⚠️ University index files not found")
            
            # Load visa index and metadata
            visa_index_path = os.path.join(self.knowledge_base_path, "faiss_visas_index.index")
            visa_metadata_path = os.path.join(self.knowledge_base_path, "faiss_visas_index_metadata.pkl")
            
            if os.path.exists(visa_index_path) and os.path.exists(visa_metadata_path):
                self.visa_index = faiss.read_index(visa_index_path)
                with open(visa_metadata_path, 'rb') as f:
                    self.visa_metadata = pickle.load(f)
                logger.info(f"✅ Loaded visa index with {self.visa_index.ntotal} vectors")
            else:
                logger.warning("⚠️ Visa index files not found")
            
            # Initialize embedding model
            self._initialize_embedding_model()
            
        except Exception as e:
            logger.error(f"❌ Error loading knowledge base: {e}")
            raise
    
    def _initialize_embedding_model(self):
        """Initialize the embedding model (lazy loading)"""
        if self.embedding_model is not None:
            return  # Already initialized
            
        try:
            # Use the same model that was used to create the indices
            if self.university_metadata and 'embedding_model' in self.university_metadata:
                model_name = self.university_metadata['embedding_model']
            else:
                # Default model
                model_name = "sentence-transformers/all-MiniLM-L6-v2"
            
            self.embedding_model = SentenceTransformer(model_name)
            logger.info(f"✅ Initialized embedding model: {model_name}")
            
        except Exception as e:
            logger.error(f"❌ Error initializing embedding model: {e}")
            # Fallback to default model
            try:
                self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            except Exception as e2:
                logger.error(f"❌ Failed to load fallback model: {e2}")
                self.embedding_model = None
    
    def search_universities(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for universities based on query
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of university information dictionaries
        """
        if not self.university_index or not self.university_metadata:
            logger.warning("⚠️ University index not available")
            return []
        
        try:
            # Initialize embedding model if needed
            self._initialize_embedding_model()
            if self.embedding_model is None:
                logger.error("❌ Embedding model not available")
                return []
            
            # Encode query
            query_embedding = self.embedding_model.encode([query])
            query_embedding = query_embedding.astype('float32')
            
            # Search
            distances, indices = self.university_index.search(query_embedding, k)
            
            # Retrieve results
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.university_metadata['documents']):
                    result = {
                        'rank': i + 1,
                        'distance': float(distance),
                        'content': self.university_metadata['documents'][idx],
                        'metadata': self.university_metadata['metadata'][idx] if 'metadata' in self.university_metadata else {}
                    }
                    results.append(result)
            
            logger.info(f"🔍 Found {len(results)} university results for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error searching universities: {e}")
            return []
    
    def search_visas(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for visa information based on query
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of visa information dictionaries
        """
        if not self.visa_index or not self.visa_metadata:
            logger.warning("⚠️ Visa index not available")
            return []
        
        try:
            # Initialize embedding model if needed
            self._initialize_embedding_model()
            if self.embedding_model is None:
                logger.error("❌ Embedding model not available")
                return []
            
            # Encode query
            query_embedding = self.embedding_model.encode([query])
            query_embedding = query_embedding.astype('float32')
            
            # Search
            distances, indices = self.visa_index.search(query_embedding, k)
            
            # Retrieve results
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.visa_metadata['documents']):
                    result = {
                        'rank': i + 1,
                        'distance': float(distance),
                        'content': self.visa_metadata['documents'][idx],
                        'metadata': self.visa_metadata['metadata'][idx] if 'metadata' in self.visa_metadata else {}
                    }
                    results.append(result)
            
            logger.info(f"🔍 Found {len(results)} visa results for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error searching visas: {e}")
            return []
    
    def smart_search(self, query: str, search_type: str = "auto", k: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Smart search that determines the best search strategy
        
        Args:
            query: Search query
            search_type: "auto", "universities", "visas", or "both"
            k: Number of results per category
            
        Returns:
            Dictionary with search results
        """
        results = {
            'universities': [],
            'visas': [],
            'search_type': search_type,
            'query': query
        }
        
        try:
            # Determine search strategy
            if search_type == "auto":
                # Auto-detect based on query content
                query_lower = query.lower()
                university_keywords = ['university', 'college', 'school', 'education', 'study', 'degree', 'program', 'course', 'tuition', 'scholarship']
                visa_keywords = ['visa', 'immigration', 'work permit', 'residence', 'citizenship', 'passport', 'entry', 'stay', 'permit']
                
                has_university_keywords = any(keyword in query_lower for keyword in university_keywords)
                has_visa_keywords = any(keyword in query_lower for keyword in visa_keywords)
                
                if has_university_keywords and not has_visa_keywords:
                    search_type = "universities"
                elif has_visa_keywords and not has_university_keywords:
                    search_type = "visas"
                else:
                    search_type = "both"
            
            # Perform searches
            if search_type in ["universities", "both"]:
                results['universities'] = self.search_universities(query, k)
            
            if search_type in ["visas", "both"]:
                results['visas'] = self.search_visas(query, k)
            
            results['search_type'] = search_type
            logger.info(f"🎯 Smart search completed: {search_type} for '{query[:30]}...'")
            
        except Exception as e:
            logger.error(f"❌ Error in smart search: {e}")
        
        return results
    
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get summary of the knowledge base"""
        summary = {
            'universities': {
                'available': self.university_index is not None,
                'vector_count': self.university_index.ntotal if self.university_index else 0,
                'dimension': self.university_index.d if self.university_index else 0
            },
            'visas': {
                'available': self.visa_index is not None,
                'vector_count': self.visa_index.ntotal if self.visa_index else 0,
                'dimension': self.visa_index.d if self.visa_index else 0
            },
            'embedding_model': str(self.embedding_model) if self.embedding_model else None
        }
        return summary
    
    def is_available(self) -> bool:
        """Check if knowledge base is available"""
        return (self.university_index is not None or self.visa_index is not None) and self.embedding_model is not None

# Global knowledge base instance (lazy initialization)
faiss_kb = None

def get_faiss_kb():
    """Get FAISS knowledge base instance (lazy initialization)"""
    global faiss_kb
    if faiss_kb is None:
        faiss_kb = FAISSKnowledgeBase()
    return faiss_kb
