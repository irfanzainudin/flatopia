"""
Knowledge Base Updater
Handles updating the FAISS knowledge base with new information from LLM responses
"""
import os
import pickle
import numpy as np
import faiss
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class KnowledgeUpdater:
    """Handles updating the FAISS knowledge base with new information"""
    
    def __init__(self, knowledge_base_path: str = "KnowledgeBase"):
        """
        Initialize Knowledge Updater
        
        Args:
            knowledge_base_path: Path to the KnowledgeBase directory
        """
        self.knowledge_base_path = knowledge_base_path
        self.embedding_model = None
        # Don't initialize embedding model immediately
    
    def _initialize_embedding_model(self):
        """Initialize the embedding model (lazy loading)"""
        if self.embedding_model is not None:
            return  # Already initialized
            
        try:
            self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            logger.info("✅ Initialized embedding model for knowledge updates")
        except Exception as e:
            logger.error(f"❌ Error initializing embedding model: {e}")
            self.embedding_model = None
    
    def should_update_knowledge(self, user_query: str, llm_response: str) -> bool:
        """
        Determine if knowledge base should be updated based on query and response
        
        Args:
            user_query: User's query
            llm_response: LLM's response
            
        Returns:
            Boolean indicating whether to update knowledge base
        """
        # Check if response contains factual information worth storing
        factual_indicators = [
            "university", "college", "school", "program", "tuition", "scholarship",
            "visa", "immigration", "work permit", "residence", "requirements",
            "admission", "application", "deadline", "cost", "ranking"
        ]
        
        response_lower = llm_response.lower()
        has_factual_info = any(indicator in response_lower for indicator in factual_indicators)
        
        # Check if response is substantial (not just conversational)
        is_substantial = len(llm_response.split()) > 20
        
        # Check if response contains specific details (numbers, names, etc.)
        has_specifics = any(char.isdigit() for char in llm_response) or \
                       any(word.istitle() for word in llm_response.split())
        
        return has_factual_info and is_substantial and has_specifics
    
    def extract_knowledge_chunks(self, content: str, chunk_type: str = "general") -> List[Dict[str, Any]]:
        """
        Extract knowledge chunks from content
        
        Args:
            content: Content to extract knowledge from
            chunk_type: Type of knowledge ("university", "visa", "general")
            
        Returns:
            List of knowledge chunks
        """
        chunks = []
        
        # Split content into sentences
        sentences = content.split('. ')
        
        # Group sentences into chunks
        chunk_size = 3  # 3 sentences per chunk
        for i in range(0, len(sentences), chunk_size):
            chunk_sentences = sentences[i:i + chunk_size]
            chunk_text = '. '.join(chunk_sentences).strip()
            
            if len(chunk_text) > 50:  # Only include substantial chunks
                chunk = {
                    "content": chunk_text,
                    "metadata": {
                        "type": chunk_type,
                        "created_at": datetime.now().isoformat(),
                        "source": "llm_response",
                        "chunk_id": f"{chunk_type}_{i}_{hash(chunk_text) % 10000}"
                    }
                }
                chunks.append(chunk)
        
        return chunks
    
    def classify_content_type(self, content: str) -> str:
        """
        Classify content type based on keywords
        
        Args:
            content: Content to classify
            
        Returns:
            Content type ("university", "visa", "general")
        """
        content_lower = content.lower()
        
        university_keywords = [
            'university', 'college', 'school', 'education', 'program', 'course',
            'tuition', 'scholarship', 'admission', 'campus', 'faculty'
        ]
        
        visa_keywords = [
            'visa', 'immigration', 'work permit', 'residence', 'citizenship',
            'passport', 'entry', 'stay', 'permit', 'application'
        ]
        
        university_score = sum(1 for keyword in university_keywords if keyword in content_lower)
        visa_score = sum(1 for keyword in visa_keywords if keyword in content_lower)
        
        if university_score > visa_score and university_score > 0:
            return "university"
        elif visa_score > university_score and visa_score > 0:
            return "visa"
        else:
            return "general"
    
    def update_knowledge_base(self, user_query: str, llm_response: str) -> Dict[str, Any]:
        """
        Update knowledge base with new information
        
        Args:
            user_query: User's query
            llm_response: LLM's response
            
        Returns:
            Dictionary containing update results
        """
        try:
            # Initialize embedding model if needed
            self._initialize_embedding_model()
            if self.embedding_model is None:
                return {
                    "success": False,
                    "reason": "Embedding model not available",
                    "updated_chunks": 0
                }
            
            # Check if should update
            if not self.should_update_knowledge(user_query, llm_response):
                return {
                    "success": False,
                    "reason": "Content not suitable for knowledge base update",
                    "updated_chunks": 0
                }
            
            # Classify content type
            content_type = self.classify_content_type(llm_response)
            
            # Extract knowledge chunks
            chunks = self.extract_knowledge_chunks(llm_response, content_type)
            
            if not chunks:
                return {
                    "success": False,
                    "reason": "No suitable chunks extracted",
                    "updated_chunks": 0
                }
            
            # Update appropriate index
            if content_type == "university":
                updated = self._update_university_index(chunks)
            elif content_type == "visa":
                updated = self._update_visa_index(chunks)
            else:
                # For general content, try to update both if relevant
                uni_updated = self._update_university_index(chunks)
                visa_updated = self._update_visa_index(chunks)
                updated = uni_updated + visa_updated
            
            return {
                "success": True,
                "content_type": content_type,
                "updated_chunks": len(chunks),
                "chunks_added": updated
            }
            
        except Exception as e:
            logger.error(f"❌ Error updating knowledge base: {e}")
            return {
                "success": False,
                "error": str(e),
                "updated_chunks": 0
            }
    
    def _update_university_index(self, chunks: List[Dict[str, Any]]) -> int:
        """
        Update university index with new chunks
        
        Args:
            chunks: List of knowledge chunks
            
        Returns:
            Number of chunks added
        """
        try:
            # Load existing index and metadata
            index_path = os.path.join(self.knowledge_base_path, "faiss_universities_index.index")
            metadata_path = os.path.join(self.knowledge_base_path, "faiss_universities_index_metadata.pkl")
            
            if not os.path.exists(index_path) or not os.path.exists(metadata_path):
                logger.warning("⚠️ University index not found, skipping update")
                return 0
            
            # Load existing data
            index = faiss.read_index(index_path)
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
            
            # Prepare new chunks
            new_contents = [chunk["content"] for chunk in chunks]
            new_metadatas = [chunk["metadata"] for chunk in chunks]
            
            # Generate embeddings
            new_embeddings = self.embedding_model.encode(new_contents)
            new_embeddings = new_embeddings.astype('float32')
            
            # Add to index
            index.add(new_embeddings)
            
            # Update metadata
            metadata['documents'].extend(new_contents)
            metadata['metadata'].extend(new_metadatas)
            
            # Save updated index and metadata
            faiss.write_index(index, index_path)
            with open(metadata_path, 'wb') as f:
                pickle.dump(metadata, f)
            
            logger.info(f"✅ Updated university index with {len(chunks)} new chunks")
            return len(chunks)
            
        except Exception as e:
            logger.error(f"❌ Error updating university index: {e}")
            return 0
    
    def _update_visa_index(self, chunks: List[Dict[str, Any]]) -> int:
        """
        Update visa index with new chunks
        
        Args:
            chunks: List of knowledge chunks
            
        Returns:
            Number of chunks added
        """
        try:
            # Load existing index and metadata
            index_path = os.path.join(self.knowledge_base_path, "faiss_visas_index.index")
            metadata_path = os.path.join(self.knowledge_base_path, "faiss_visas_index_metadata.pkl")
            
            if not os.path.exists(index_path) or not os.path.exists(metadata_path):
                logger.warning("⚠️ Visa index not found, skipping update")
                return 0
            
            # Load existing data
            index = faiss.read_index(index_path)
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
            
            # Prepare new chunks
            new_contents = [chunk["content"] for chunk in chunks]
            new_metadatas = [chunk["metadata"] for chunk in chunks]
            
            # Generate embeddings
            new_embeddings = self.embedding_model.encode(new_contents)
            new_embeddings = new_embeddings.astype('float32')
            
            # Add to index
            index.add(new_embeddings)
            
            # Update metadata
            metadata['documents'].extend(new_contents)
            metadata['metadata'].extend(new_metadatas)
            
            # Save updated index and metadata
            faiss.write_index(index, index_path)
            with open(metadata_path, 'wb') as f:
                pickle.dump(metadata, f)
            
            logger.info(f"✅ Updated visa index with {len(chunks)} new chunks")
            return len(chunks)
            
        except Exception as e:
            logger.error(f"❌ Error updating visa index: {e}")
            return 0
    
    def get_update_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about knowledge base updates
        
        Returns:
            Dictionary containing update statistics
        """
        try:
            stats = {
                "university_index": {"available": False, "size": 0},
                "visa_index": {"available": False, "size": 0},
                "last_updated": None
            }
            
            # Check university index
            uni_index_path = os.path.join(self.knowledge_base_path, "faiss_universities_index.index")
            if os.path.exists(uni_index_path):
                index = faiss.read_index(uni_index_path)
                stats["university_index"] = {
                    "available": True,
                    "size": index.ntotal
                }
            
            # Check visa index
            visa_index_path = os.path.join(self.knowledge_base_path, "faiss_visas_index.index")
            if os.path.exists(visa_index_path):
                index = faiss.read_index(visa_index_path)
                stats["visa_index"] = {
                    "available": True,
                    "size": index.ntotal
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting update statistics: {e}")
            return {"error": str(e)}

# Global knowledge updater instance
knowledge_updater = KnowledgeUpdater()
