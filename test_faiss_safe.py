"""
Safe test for FAISS knowledge base integration
"""
import os
import sys
import pickle

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_metadata_loading():
    """Test metadata loading"""
    print("=== Testing Metadata Loading ===")
    
    try:
        # Load university metadata
        with open("KnowledgeBase/faiss_universities_index_metadata.pkl", 'rb') as f:
            uni_metadata = pickle.load(f)
        
        print(f"✅ University metadata loaded")
        print(f"   Documents: {len(uni_metadata.get('documents', []))}")
        print(f"   Metadata: {len(uni_metadata.get('metadata', []))}")
        print(f"   Embedding model: {uni_metadata.get('embedding_model', 'unknown')}")
        
        # Load visa metadata
        with open("KnowledgeBase/faiss_visas_index_metadata.pkl", 'rb') as f:
            visa_metadata = pickle.load(f)
        
        print(f"✅ Visa metadata loaded")
        print(f"   Documents: {len(visa_metadata.get('documents', []))}")
        print(f"   Metadata: {len(visa_metadata.get('metadata', []))}")
        print(f"   Embedding model: {visa_metadata.get('embedding_model', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sample_content():
    """Test sample content from metadata"""
    print("\n=== Testing Sample Content ===")
    
    try:
        # Load university metadata
        with open("KnowledgeBase/faiss_universities_index_metadata.pkl", 'rb') as f:
            uni_metadata = pickle.load(f)
        
        # Show sample university content
        documents = uni_metadata.get('documents', [])
        if documents:
            print(f"✅ Sample university content:")
            print(f"   {documents[0][:200]}...")
        
        # Load visa metadata
        with open("KnowledgeBase/faiss_visas_index_metadata.pkl", 'rb') as f:
            visa_metadata = pickle.load(f)
        
        # Show sample visa content
        documents = visa_metadata.get('documents', [])
        if documents:
            print(f"✅ Sample visa content:")
            print(f"   {documents[0][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_faiss_knowledge_base_class():
    """Test FAISSKnowledgeBase class without full initialization"""
    print("\n=== Testing FAISSKnowledgeBase Class ===")
    
    try:
        # Import the class
        from core.faiss_knowledge_base import FAISSKnowledgeBase
        print("✅ FAISSKnowledgeBase class imported successfully")
        
        # Test class methods exist
        methods = ['search_universities', 'search_visas', 'smart_search', 'is_available']
        for method in methods:
            if hasattr(FAISSKnowledgeBase, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_smart_search_class():
    """Test SmartSearchStrategy class"""
    print("\n=== Testing SmartSearchStrategy Class ===")
    
    try:
        # Import the class
        from core.smart_search import SmartSearchStrategy
        print("✅ SmartSearchStrategy class imported successfully")
        
        # Test class methods exist
        methods = ['analyze_query_intent', 'extract_search_terms', 'smart_search']
        for method in methods:
            if hasattr(SmartSearchStrategy, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_knowledge_updater_class():
    """Test KnowledgeUpdater class"""
    print("\n=== Testing KnowledgeUpdater Class ===")
    
    try:
        # Import the class
        from core.knowledge_updater import KnowledgeUpdater
        print("✅ KnowledgeUpdater class imported successfully")
        
        # Test class methods exist
        methods = ['should_update_knowledge', 'extract_knowledge_chunks', 'update_knowledge_base']
        for method in methods:
            if hasattr(KnowledgeUpdater, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run safe tests"""
    print("🚀 Starting Safe FAISS Tests\n")
    
    tests = [
        ("Metadata Loading", test_metadata_loading),
        ("Sample Content", test_sample_content),
        ("FAISSKnowledgeBase Class", test_faiss_knowledge_base_class),
        ("SmartSearchStrategy Class", test_smart_search_class),
        ("KnowledgeUpdater Class", test_knowledge_updater_class),
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
        print("🎉 All safe tests passed! FAISS integration classes are ready.")
    else:
        print("⚠️ Some tests failed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
