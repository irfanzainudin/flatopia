"""
Minimal test for FAISS knowledge base integration
"""
import os
import sys
import pickle

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_file_structure():
    """Test that all required files exist"""
    print("=== Testing File Structure ===")
    
    required_files = [
        "KnowledgeBase/faiss_universities_index.index",
        "KnowledgeBase/faiss_universities_index_metadata.pkl",
        "KnowledgeBase/faiss_visas_index.index",
        "KnowledgeBase/faiss_visas_index_metadata.pkl",
        "core/faiss_knowledge_base.py",
        "core/smart_search.py",
        "core/knowledge_updater.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_metadata_structure():
    """Test metadata structure"""
    print("\n=== Testing Metadata Structure ===")
    
    try:
        # Test university metadata
        with open("KnowledgeBase/faiss_universities_index_metadata.pkl", 'rb') as f:
            uni_metadata = pickle.load(f)
        
        required_keys = ['documents', 'metadata', 'embedding_model']
        for key in required_keys:
            if key in uni_metadata:
                print(f"✅ University metadata has '{key}'")
            else:
                print(f"❌ University metadata missing '{key}'")
                return False
        
        # Test visa metadata
        with open("KnowledgeBase/faiss_visas_index_metadata.pkl", 'rb') as f:
            visa_metadata = pickle.load(f)
        
        for key in required_keys:
            if key in visa_metadata:
                print(f"✅ Visa metadata has '{key}'")
            else:
                print(f"❌ Visa metadata missing '{key}'")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_faiss_index_integrity():
    """Test FAISS index integrity"""
    print("\n=== Testing FAISS Index Integrity ===")
    
    try:
        import faiss
        import numpy as np
        
        # Test university index
        uni_index = faiss.read_index("KnowledgeBase/faiss_universities_index.index")
        print(f"✅ University index: {uni_index.ntotal} vectors, {uni_index.d} dimensions")
        
        # Test visa index
        visa_index = faiss.read_index("KnowledgeBase/faiss_visas_index.index")
        print(f"✅ Visa index: {visa_index.ntotal} vectors, {visa_index.d} dimensions")
        
        # Test search functionality
        query_vector = np.random.random((1, uni_index.d)).astype('float32')
        distances, indices = uni_index.search(query_vector, k=1)
        print(f"✅ University search test: {len(indices[0])} results")
        
        query_vector = np.random.random((1, visa_index.d)).astype('float32')
        distances, indices = visa_index.search(query_vector, k=1)
        print(f"✅ Visa search test: {len(indices[0])} results")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_import_modules():
    """Test importing modules without instantiation"""
    print("\n=== Testing Module Imports ===")
    
    try:
        # Test importing without instantiation
        import core.faiss_knowledge_base
        print("✅ faiss_knowledge_base module imported")
        
        import core.smart_search
        print("✅ smart_search module imported")
        
        import core.knowledge_updater
        print("✅ knowledge_updater module imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run minimal tests"""
    print("🚀 Starting Minimal FAISS Tests\n")
    
    tests = [
        ("File Structure", test_file_structure),
        ("Metadata Structure", test_metadata_structure),
        ("FAISS Index Integrity", test_faiss_index_integrity),
        ("Module Imports", test_import_modules),
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
        print("🎉 All minimal tests passed! FAISS integration is ready.")
        print("\n📋 Integration Summary:")
        print("   ✅ FAISS indices loaded successfully")
        print("   ✅ Metadata structure is correct")
        print("   ✅ Search functionality works")
        print("   ✅ All modules can be imported")
        print("\n🚀 Ready to use FAISS knowledge base integration!")
    else:
        print("⚠️ Some tests failed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
