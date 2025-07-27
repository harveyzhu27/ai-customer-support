import json
import os
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_vectors(file_path: str) -> List[Dict[str, Any]]:
    """
    Load vectors from the generated JSON file.
    
    Args:
        file_path (str): Path to the vectors JSON file
        
    Returns:
        List[Dict[str, Any]]: List of vectors ready for Pinecone
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            vectors = json.load(file)
        print(f"✅ Loaded {len(vectors)} vectors from {file_path}")
        return vectors
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {file_path}: {e}")
        return []

def create_pinecone_index(pc: Pinecone, index_name: str, dimension: int = 1536):
    """
    Create a Pinecone index if it doesn't exist.
    
    Args:
        pc (Pinecone): Pinecone client
        index_name (str): Name of the index to create
        dimension (int): Dimension of the vectors
    """
    try:
        # Check if index already exists
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if index_name in existing_indexes:
            print(f"✅ Index '{index_name}' already exists")
            return
        
        # Create new index
        print(f"🔧 Creating Pinecone index '{index_name}'...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        print(f"✅ Successfully created index '{index_name}'")
        
    except Exception as e:
        print(f"❌ Error creating index: {e}")

def upload_vectors_to_pinecone(vectors: List[Dict[str, Any]], index_name: str = "aven-faq"):
    """
    Upload vectors to Pinecone index.
    
    Args:
        vectors (List[Dict[str, Any]]): List of vectors to upload
        index_name (str): Name of the Pinecone index
    """
    # Check for Pinecone API key
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("❌ Error: PINECONE_API_KEY environment variable not set")
        print("Please set your Pinecone API key:")
        print("  export PINECONE_API_KEY='your-api-key-here'")
        print("  or create a .env file with: PINECONE_API_KEY=your-api-key-here")
        return
    
    try:
        # Initialize Pinecone client
        pc = Pinecone(api_key=api_key)
        
        # Create index if it doesn't exist
        create_pinecone_index(pc, index_name)
        
        # Get the index
        index = pc.Index(index_name)
        
        # Wait for index to be ready
        print("⏳ Waiting for index to be ready...")
        while not index.describe_index_stats():
            import time
            time.sleep(1)
        
        # Upload vectors in batches
        batch_size = 100
        total_batches = (len(vectors) + batch_size - 1) // batch_size
        
        print(f"📤 Uploading {len(vectors)} vectors in {total_batches} batches...")
        
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            try:
                # Prepare batch for upsert
                upsert_batch = []
                for vector in batch:
                    upsert_batch.append({
                        "id": vector["id"],
                        "values": vector["values"],
                        "metadata": vector["metadata"]
                    })
                
                # Upsert batch
                index.upsert(vectors=upsert_batch)
                print(f"✅ Uploaded batch {batch_num}/{total_batches} ({len(batch)} vectors)")
                
            except Exception as e:
                print(f"❌ Error uploading batch {batch_num}: {e}")
        
        # Get index stats
        stats = index.describe_index_stats()
        print(f"\n📊 Index Statistics:")
        print(f"   • Total vectors: {stats.total_vector_count}")
        print(f"   • Index dimension: {stats.dimension}")
        print(f"   • Index metric: {stats.metric}")
        
        print(f"\n🎉 Successfully uploaded all vectors to Pinecone index '{index_name}'")
        
    except Exception as e:
        print(f"❌ Error connecting to Pinecone: {e}")

def search_example(index_name: str = "aven-faq"):
    """
    Example search function to test the uploaded vectors.
    
    Args:
        index_name (str): Name of the Pinecone index
    """
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("❌ Error: PINECONE_API_KEY environment variable not set")
        return
    
    try:
        pc = Pinecone(api_key=api_key)
        index = pc.Index(index_name)
        
        # Example search queries
        test_queries = [
            "How do I make a payment?",
            "What is the interest rate?",
            "Can I pay with a check?",
            "How long does it take to get my card?"
        ]
        
        print(f"\n🔍 Testing search functionality...")
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            print("-" * 50)
            
            # Note: You would need to embed the query first
            # This is just an example structure
            print("(Note: Query embedding would be required for actual search)")
            print("Top results would appear here...")
            
    except Exception as e:
        print(f"❌ Error during search: {e}")

def main():
    """
    Main function to upload vectors to Pinecone.
    """
    vectors_file = "aven_faq_vectors.json"
    
    # Load vectors
    print("📖 Loading vectors...")
    vectors = load_vectors(vectors_file)
    
    if not vectors:
        print("❌ No vectors loaded. Please run the embedding script first.")
        return
    
    # Upload to Pinecone
    print("🚀 Uploading to Pinecone...")
    upload_vectors_to_pinecone(vectors)
    
    # Show search example
    print("\n💡 Search Example:")
    search_example()

if __name__ == "__main__":
    main() 