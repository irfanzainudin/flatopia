"""
Test script for FAISS knowledge base integration
"""
import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.faiss_knowledge_base import faiss_kb
from core.smart_search import smart_search
from core.knowledge_updater import knowledge_updater
from core.flatopia_chat_manager import flatopia_chat_manager

def test_faiss_loading():
    """Test FAISS knowledge base loading"""
    print("=== Testing FAISS Knowledge Base Loading ===")
    
    try:
        # Test knowledge base availability
        if faiss_kb.is_available():
            print("✅ FAISS knowledge base is available")
            
            # Get summary
            summary = faiss_kb.get_knowledge_summary()
            print(f"📊 Knowledge Base Summary:")
            print(f"   Universities: {summary['universities']['vector_count']} vectors")
            print(f"   Visas: {summary['visas']['vector_count']} vectors")
            print(f"   Embedding Model: {summary['embedding_model']}")
            
        else:
            print("❌ FAISS knowledge base is not available")
            return False
            
    except Exception as e:
        print(f"❌ Error testing FAISS loading: {e}")
        return False
    
    return True

def test_university_search():
    """Test university search functionality"""
    print("\n=== Testing University Search ===")
    
    try:
        # Test university search
        query = "computer science university canada"
        results = faiss_kb.search_universities(query, k=3)
        
        if results:
            print(f"✅ Found {len(results)} university results for '{query}'")
            for i, result in enumerate(results, 1):
                print(f"   {i}. Distance: {result['distance']:.4f}")
                print(f"      Content: {result['content'][:100]}...")
        else:
            print(f"❌ No university results found for '{query}'")
            return False
            
    except Exception as e:
        print(f"❌ Error testing university search: {e}")
        return False
    
    return True

def test_visa_search():
    """Test visa search functionality"""
    print("\n=== Testing Visa Search ===")
    
    try:
        # Test visa search
        query = "work permit canada requirements"
        results = faiss_kb.search_visas(query, k=3)
        
        if results:
            print(f"✅ Found {len(results)} visa results for '{query}'")
            for i, result in enumerate(results, 1):
                print(f"   {i}. Distance: {result['distance']:.4f}")
                print(f"      Content: {result['content'][:100]}...")
        else:
            print(f"❌ No visa results found for '{query}'")
            return False
            
    except Exception as e:
        print(f"❌ Error testing visa search: {e}")
        return False
    
    return True

def test_smart_search():
    """Test smart search functionality"""
    print("\n=== Testing Smart Search ===")
    
    try:
        # Test smart search
        query = "best universities for engineering in australia"
        results = smart_search.smart_search(query, max_results=3)
        
        if results.get("universities") or results.get("visas"):
            print(f"✅ Smart search found results for '{query}'")
            print(f"   Intent: {results.get('metadata', {}).get('intent_analysis', {}).get('primary_intent', 'unknown')}")
            print(f"   Universities: {len(results.get('universities', []))}")
            print(f"   Visas: {len(results.get('visas', []))}")
        else:
            print(f"❌ Smart search found no results for '{query}'")
            return False
            
    except Exception as e:
        print(f"❌ Error testing smart search: {e}")
        return False
    
    return True

def test_knowledge_updater():
    """Test knowledge updater functionality"""
    print("\n=== Testing Knowledge Updater ===")
    
    try:
        # Test knowledge updater
        test_query = "What are the requirements for studying in Germany?"
        test_response = """
        To study in Germany, you need to meet several requirements:
        1. Academic qualifications equivalent to German Abitur
        2. German language proficiency (TestDaF or DSH)
        3. Proof of financial resources (€10,332 per year)
        4. Health insurance coverage
        5. Valid passport and student visa
        """
        
        # Test if content should be updated
        should_update = knowledge_updater.should_update_knowledge(test_query, test_response)
        print(f"✅ Should update knowledge: {should_update}")
        
        # Test content classification
        content_type = knowledge_updater.classify_content_type(test_response)
        print(f"✅ Content type: {content_type}")
        
        # Test chunk extraction
        chunks = knowledge_updater.extract_knowledge_chunks(test_response, content_type)
        print(f"✅ Extracted {len(chunks)} chunks")
        
        # Get update statistics
        stats = knowledge_updater.get_update_statistics()
        print(f"✅ Update statistics: {stats}")
        
    except Exception as e:
        print(f"❌ Error testing knowledge updater: {e}")
        return False
    
    return True

async def test_chat_integration():
    """Test chat integration with knowledge base"""
    print("\n=== Testing Chat Integration ===")
    
    try:
        # Test chat with knowledge base integration
        test_queries = [
            "Tell me about universities in Canada",
            "What are the visa requirements for Australia?",
            "I want to study computer science in Germany"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: '{query}'")
            
            # Get chat response
            response = await flatopia_chat_manager.chat(query)
            
            if response.get("answer"):
                print(f"✅ Chat response received")
                print(f"   Stage: {response.get('conversation_stage', 'unknown')}")
                print(f"   Response length: {len(response['answer'])} characters")
            else:
                print(f"❌ No chat response received")
                return False
        
        # Test knowledge base status
        kb_status = flatopia_chat_manager.get_knowledge_base_status()
        print(f"\n📊 Knowledge Base Status:")
        print(f"   Smart search available: {kb_status.get('smart_search_available', False)}")
        print(f"   Knowledge updater available: {kb_status.get('knowledge_updater_available', False)}")
        
    except Exception as e:
        print(f"❌ Error testing chat integration: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting FAISS Knowledge Base Integration Tests\n")
    
    tests = [
        ("FAISS Loading", test_faiss_loading),
        ("University Search", test_university_search),
        ("Visa Search", test_visa_search),
        ("Smart Search", test_smart_search),
        ("Knowledge Updater", test_knowledge_updater),
    ]
    
    passed = 0
    total = len(tests)
    
    # Run synchronous tests
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        if test_func():
            print(f"✅ {test_name} - PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} - FAILED")
    
    # Run async test
    print(f"\n{'='*50}")
    try:
        if asyncio.run(test_chat_integration()):
            print("✅ Chat Integration - PASSED")
            passed += 1
        else:
            print("❌ Chat Integration - FAILED")
    except Exception as e:
        print(f"❌ Chat Integration - FAILED: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total + 1} tests passed")
    
    if passed == total + 1:
        print("🎉 All tests passed! FAISS integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total + 1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
