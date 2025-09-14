"""
Simple test for FAISS knowledge base integration
"""
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_faiss_import():
    """Test basic FAISS import and loading"""
    print("=== Testing FAISS Import ===")
    
    try:
        import faiss
        print("✅ FAISS imported successfully")
        
        # Test loading index files
        uni_index_path = "KnowledgeBase/faiss_universities_index.index"
        visa_index_path = "KnowledgeBase/faiss_visas_index.index"
        
        if os.path.exists(uni_index_path):
            uni_index = faiss.read_index(uni_index_path)
            print(f"✅ University index loaded: {uni_index.ntotal} vectors")
        else:
            print("❌ University index not found")
            
        if os.path.exists(visa_index_path):
            visa_index = faiss.read_index(visa_index_path)
            print(f"✅ Visa index loaded: {visa_index.ntotal} vectors")
        else:
            print("❌ Visa index not found")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sentence_transformer():
    """Test sentence transformer import"""
    print("\n=== Testing Sentence Transformer ===")
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ SentenceTransformer imported successfully")
        
        # Test model loading (without actually loading)
        print("✅ SentenceTransformer module is available")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_basic_search():
    """Test basic FAISS search functionality"""
    print("\n=== Testing Basic FAISS Search ===")
    
    try:
        import faiss
        import numpy as np
        
        # Load university index
        uni_index = faiss.read_index("KnowledgeBase/faiss_universities_index.index")
        
        # Create a random query vector
        query_vector = np.random.random((1, 384)).astype('float32')
        
        # Perform search
        distances, indices = uni_index.search(query_vector, k=3)
        
        print(f"✅ Search successful: {len(indices[0])} results")
        print(f"   Indices: {indices[0]}")
        print(f"   Distances: {distances[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run basic tests"""
    print("🚀 Starting Basic FAISS Tests\n")
    
    tests = [
        ("FAISS Import", test_faiss_import),
        ("Sentence Transformer", test_sentence_transformer),
        ("Basic Search", test_basic_search),
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
        print("🎉 All basic tests passed!")
    else:
        print("⚠️ Some tests failed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
