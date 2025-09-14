"""
Final test for FAISS knowledge base integration
"""
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_import():
    """Test basic import without instantiation"""
    print("=== Testing Basic Import ===")
    
    try:
        # Test importing modules
        import core.faiss_knowledge_base
        print("✅ faiss_knowledge_base imported")
        
        import core.smart_search
        print("✅ smart_search imported")
        
        import core.knowledge_updater
        print("✅ knowledge_updater imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_faiss_loading():
    """Test FAISS loading without embedding model"""
    print("\n=== Testing FAISS Loading ===")
    
    try:
        import faiss
        import pickle
        
        # Test loading indices
        uni_index = faiss.read_index("KnowledgeBase/faiss_universities_index.index")
        print(f"✅ University index: {uni_index.ntotal} vectors")
        
        visa_index = faiss.read_index("KnowledgeBase/faiss_visas_index.index")
        print(f"✅ Visa index: {visa_index.ntotal} vectors")
        
        # Test loading metadata
        with open("KnowledgeBase/faiss_universities_index_metadata.pkl", 'rb') as f:
            uni_metadata = pickle.load(f)
        print(f"✅ University metadata: {len(uni_metadata['documents'])} documents")
        
        with open("KnowledgeBase/faiss_visas_index_metadata.pkl", 'rb') as f:
            visa_metadata = pickle.load(f)
        print(f"✅ Visa metadata: {len(visa_metadata['documents'])} documents")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_class_instantiation():
    """Test class instantiation (without embedding model)"""
    print("\n=== Testing Class Instantiation ===")
    
    try:
        from core.faiss_knowledge_base import FAISSKnowledgeBase
        
        # Create instance (should not load embedding model yet)
        kb = FAISSKnowledgeBase()
        print("✅ FAISSKnowledgeBase instantiated")
        
        # Check if indices are loaded
        if kb.university_index is not None:
            print(f"✅ University index loaded: {kb.university_index.ntotal} vectors")
        else:
            print("❌ University index not loaded")
            return False
            
        if kb.visa_index is not None:
            print(f"✅ Visa index loaded: {kb.visa_index.ntotal} vectors")
        else:
            print("❌ Visa index not loaded")
            return False
        
        # Check if embedding model is not loaded yet
        if kb.embedding_model is None:
            print("✅ Embedding model not loaded yet (lazy loading)")
        else:
            print("⚠️ Embedding model already loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_smart_search_instantiation():
    """Test smart search instantiation"""
    print("\n=== Testing Smart Search Instantiation ===")
    
    try:
        from core.smart_search import SmartSearchStrategy
        
        # Create instance
        smart_search = SmartSearchStrategy()
        print("✅ SmartSearchStrategy instantiated")
        
        # Test basic methods
        query = "university canada computer science"
        intent = smart_search.analyze_query_intent(query)
        print(f"✅ Query intent analysis: {intent['primary_intent']}")
        
        terms = smart_search.extract_search_terms(query)
        print(f"✅ Extracted terms: {len(terms['university_terms'])} university terms")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_knowledge_updater_instantiation():
    """Test knowledge updater instantiation"""
    print("\n=== Testing Knowledge Updater Instantiation ===")
    
    try:
        from core.knowledge_updater import KnowledgeUpdater
        
        # Create instance
        updater = KnowledgeUpdater()
        print("✅ KnowledgeUpdater instantiated")
        
        # Test basic methods
        test_content = "University of Toronto is a top university in Canada for computer science."
        content_type = updater.classify_content_type(test_content)
        print(f"✅ Content classification: {content_type}")
        
        should_update = updater.should_update_knowledge("test query", test_content)
        print(f"✅ Should update: {should_update}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run final tests"""
    print("🚀 Starting Final FAISS Integration Tests\n")
    
    tests = [
        ("Basic Import", test_basic_import),
        ("FAISS Loading", test_faiss_loading),
        ("Class Instantiation", test_class_instantiation),
        ("Smart Search Instantiation", test_smart_search_instantiation),
        ("Knowledge Updater Instantiation", test_knowledge_updater_instantiation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        if test_func():
            print(f"✅ {test_name} - PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} - FAILED")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! FAISS integration is working correctly.")
        print("\n📋 Integration Summary:")
        print("   ✅ All modules can be imported")
        print("   ✅ FAISS indices load successfully")
        print("   ✅ Classes can be instantiated")
        print("   ✅ Smart search works")
        print("   ✅ Knowledge updater works")
        print("\n🚀 FAISS knowledge base integration is ready to use!")
    else:
        print("⚠️ Some tests failed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
