"""
Smart Search Strategy Module
Implements intelligent search strategies for the FAISS knowledge base
"""
import re
from typing import Dict, List, Any, Optional, Tuple
from .faiss_knowledge_base import faiss_kb

class SmartSearchStrategy:
    """Smart search strategy for knowledge base queries"""
    
    def __init__(self):
        self.knowledge_base = faiss_kb
        
        # Define search patterns and keywords
        self.university_keywords = [
            'university', 'college', 'school', 'education', 'study', 'degree',
            'program', 'course', 'tuition', 'scholarship', 'admission',
            'requirements', 'application', 'campus', 'faculty', 'department',
            'undergraduate', 'graduate', 'phd', 'masters', 'bachelor'
        ]
        
        self.visa_keywords = [
            'visa', 'immigration', 'work permit', 'residence', 'citizenship',
            'passport', 'entry', 'stay', 'permit', 'green card', 'pr',
            'permanent residence', 'temporary', 'student visa', 'work visa',
            'tourist visa', 'visitor', 'sponsor', 'sponsorship'
        ]
        
        self.country_keywords = [
            'canada', 'australia', 'new zealand', 'uk', 'united kingdom',
            'germany', 'france', 'spain', 'italy', 'netherlands', 'sweden',
            'norway', 'denmark', 'finland', 'switzerland', 'austria',
            'ireland', 'portugal', 'belgium', 'luxembourg'
        ]
    
    def analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """
        Analyze user query to determine search intent
        
        Args:
            query: User's search query
            
        Returns:
            Dictionary containing intent analysis
        """
        query_lower = query.lower()
        
        # Check for university-related intent
        university_score = sum(1 for keyword in self.university_keywords if keyword in query_lower)
        
        # Check for visa-related intent
        visa_score = sum(1 for keyword in self.visa_keywords if keyword in query_lower)
        
        # Check for country-specific intent
        country_score = sum(1 for keyword in self.country_keywords if keyword in query_lower)
        
        # Determine primary intent
        if university_score > visa_score and university_score > 0:
            primary_intent = "universities"
        elif visa_score > university_score and visa_score > 0:
            primary_intent = "visas"
        elif country_score > 0:
            primary_intent = "both"  # Country queries often need both
        else:
            primary_intent = "auto"
        
        return {
            "primary_intent": primary_intent,
            "university_score": university_score,
            "visa_score": visa_score,
            "country_score": country_score,
            "confidence": max(university_score, visa_score, country_score) / len(query.split())
        }
    
    def extract_search_terms(self, query: str) -> Dict[str, List[str]]:
        """
        Extract relevant search terms from query
        
        Args:
            query: User's search query
            
        Returns:
            Dictionary containing extracted terms
        """
        query_lower = query.lower()
        
        # Extract university-related terms
        university_terms = [term for term in self.university_keywords if term in query_lower]
        
        # Extract visa-related terms
        visa_terms = [term for term in self.visa_keywords if term in query_lower]
        
        # Extract country terms
        country_terms = [term for term in self.country_keywords if term in query_lower]
        
        # Extract other important terms (nouns, adjectives)
        other_terms = self._extract_important_terms(query)
        
        return {
            "university_terms": university_terms,
            "visa_terms": visa_terms,
            "country_terms": country_terms,
            "other_terms": other_terms
        }
    
    def _extract_important_terms(self, query: str) -> List[str]:
        """Extract important terms from query using simple NLP"""
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'must', 'shall', 'i', 'you', 'he',
            'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        # Simple word extraction
        words = re.findall(r'\b\w+\b', query.lower())
        important_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return important_words[:10]  # Limit to top 10 terms
    
    def generate_search_queries(self, original_query: str) -> List[str]:
        """
        Generate multiple search queries for better results
        
        Args:
            original_query: Original user query
            
        Returns:
            List of search queries
        """
        queries = [original_query]
        
        # Extract terms
        terms = self.extract_search_terms(original_query)
        
        # Generate country-specific queries
        if terms["country_terms"]:
            for country in terms["country_terms"]:
                if terms["university_terms"]:
                    queries.append(f"{country} {', '.join(terms['university_terms'][:3])}")
                if terms["visa_terms"]:
                    queries.append(f"{country} {', '.join(terms['visa_terms'][:3])}")
        
        # Generate field-specific queries
        if terms["other_terms"]:
            for term in terms["other_terms"][:3]:
                if terms["university_terms"]:
                    queries.append(f"{term} {', '.join(terms['university_terms'][:2])}")
                if terms["visa_terms"]:
                    queries.append(f"{term} {', '.join(terms['visa_terms'][:2])}")
        
        # Remove duplicates and limit
        unique_queries = list(dict.fromkeys(queries))[:5]
        return unique_queries
    
    def smart_search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Perform smart search with multiple strategies
        
        Args:
            query: User's search query
            max_results: Maximum number of results per category
            
        Returns:
            Dictionary containing search results and metadata
        """
        try:
            # Analyze query intent
            intent_analysis = self.analyze_query_intent(query)
            
            # Generate multiple search queries
            search_queries = self.generate_search_queries(query)
            
            # Perform searches
            all_results = {
                "universities": [],
                "visas": [],
                "metadata": {
                    "original_query": query,
                    "intent_analysis": intent_analysis,
                    "search_queries": search_queries,
                    "total_queries": len(search_queries)
                }
            }
            
            # Search with each query
            for search_query in search_queries:
                # Determine search type based on intent
                search_type = intent_analysis["primary_intent"]
                
                # Perform search
                results = self.knowledge_base.smart_search(search_query, search_type, max_results)
                
                # Merge results
                if results.get("universities"):
                    all_results["universities"].extend(results["universities"])
                
                if results.get("visas"):
                    all_results["visas"].extend(results["visas"])
            
            # Remove duplicates and rank results
            all_results["universities"] = self._deduplicate_and_rank(all_results["universities"])
            all_results["visas"] = self._deduplicate_and_rank(all_results["visas"])
            
            # Limit results
            all_results["universities"] = all_results["universities"][:max_results]
            all_results["visas"] = all_results["visas"][:max_results]
            
            return all_results
            
        except Exception as e:
            return {
                "error": f"Smart search failed: {str(e)}",
                "universities": [],
                "visas": [],
                "metadata": {"original_query": query}
            }
    
    def _deduplicate_and_rank(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicates and rank results by relevance
        
        Args:
            results: List of search results
            
        Returns:
            Deduplicated and ranked results
        """
        if not results:
            return []
        
        # Remove duplicates based on content
        seen_contents = set()
        unique_results = []
        
        for result in results:
            content = result.get("content", "")
            if content not in seen_contents:
                seen_contents.add(content)
                unique_results.append(result)
        
        # Sort by distance (lower is better)
        unique_results.sort(key=lambda x: x.get("distance", float('inf')))
        
        return unique_results
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """
        Generate search suggestions based on query
        
        Args:
            query: User's search query
            
        Returns:
            List of search suggestions
        """
        suggestions = []
        query_lower = query.lower()
        
        # Add country-specific suggestions
        if any(country in query_lower for country in self.country_keywords):
            if "university" in query_lower or "study" in query_lower:
                suggestions.extend([
                    f"{query} admission requirements",
                    f"{query} tuition fees",
                    f"{query} scholarship opportunities"
                ])
            if "visa" in query_lower or "work" in query_lower:
                suggestions.extend([
                    f"{query} work permit requirements",
                    f"{query} immigration process",
                    f"{query} permanent residence"
                ])
        
        # Add general suggestions
        if "university" in query_lower:
            suggestions.extend([
                "top universities for international students",
                "university application deadlines",
                "university ranking and reputation"
            ])
        
        if "visa" in query_lower:
            suggestions.extend([
                "visa application process",
                "visa requirements and documents",
                "visa processing time"
            ])
        
        return suggestions[:5]  # Limit to 5 suggestions

# Global smart search instance
smart_search = SmartSearchStrategy()
