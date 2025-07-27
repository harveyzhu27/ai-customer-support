import json
import os
from typing import List, Dict, Any
from openai import OpenAI
import time

def load_faq_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load FAQ data from JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing FAQ data
        
    Returns:
        List[Dict[str, Any]]: List of FAQ entries with section, question, answer, and source_url
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"✅ Loaded {len(data)} FAQ entries from {file_path}")
        return data
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {file_path}: {e}")
        return []

def create_embeddings(questions: List[str], client: OpenAI, model: str = "text-embedding-3-small") -> List[List[float]]:
    """
    Create embeddings for a list of questions using OpenAI's embedding model.
    
    Args:
        questions (List[str]): List of questions to embed
        client (OpenAI): OpenAI client instance
        model (str): Embedding model to use
        
    Returns:
        List[List[float]]: List of embedding vectors
    """
    embeddings = []
    
    # Process in batches to avoid rate limits
    batch_size = 100
    for i in range(0, len(questions), batch_size):
        batch = questions[i:i + batch_size]
        
        try:
            response = client.embeddings.create(
                model=model,
                input=batch
            )
            
            batch_embeddings = [embedding.embedding for embedding in response.data]
            embeddings.extend(batch_embeddings)
            
            print(f"✅ Embedded batch {i//batch_size + 1}/{(len(questions) + batch_size - 1)//batch_size}")
            
            # Add a small delay to respect rate limits
            time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Error embedding batch {i//batch_size + 1}: {e}")
            # Add empty embeddings for failed batch
            embeddings.extend([[0.0] * 1536] * len(batch))  # text-embedding-3-small has 1536 dimensions
    
    return embeddings

def create_pinecone_vectors(faq_data: List[Dict[str, Any]], embeddings: List[List[float]]) -> List[Dict[str, Any]]:
    """
    Create Pinecone-ready vectors with metadata.
    
    Args:
        faq_data (List[Dict[str, Any]]): Original FAQ data
        embeddings (List[List[float]]): Embedding vectors
        
    Returns:
        List[Dict[str, Any]]: Pinecone-ready vectors with id, values, and metadata
    """
    vectors = []
    
    for i, (faq_entry, embedding) in enumerate(zip(faq_data, embeddings)):
        vector = {
            "id": f"aven_faq_{i:04d}",  # Create unique ID with zero-padding
            "values": embedding,
            "metadata": {
                "section": faq_entry["section"],
                "question": faq_entry["question"],
                "answer": faq_entry["answer"],
                "source_url": faq_entry["source_url"],
                "type": "faq",
                "company": "aven"
            }
        }
        vectors.append(vector)
    
    return vectors

def main():
    """
    Main function to process FAQ data and create Pinecone-ready vectors.
    """
    # Configuration
    faq_file = "aven_support_faq_correct.json"
    output_file = "aven_faq_vectors.json"
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Load FAQ data
    print("📖 Loading FAQ data...")
    faq_data = load_faq_data(faq_file)
    
    if not faq_data:
        print("❌ No FAQ data loaded. Exiting.")
        return
    
    # Extract questions
    questions = [entry["question"] for entry in faq_data]
    print(f"📝 Extracted {len(questions)} questions for embedding")
    
    # Create embeddings
    print("🤖 Creating embeddings with OpenAI text-embedding-3-small...")
    embeddings = create_embeddings(questions, client)
    
    if len(embeddings) != len(questions):
        print(f"❌ Warning: Number of embeddings ({len(embeddings)}) doesn't match number of questions ({len(questions)})")
        return
    
    # Create Pinecone-ready vectors
    print("🔧 Creating Pinecone-ready vectors...")
    vectors = create_pinecone_vectors(faq_data, embeddings)
    
    # Save vectors to file
    print(f"💾 Saving {len(vectors)} vectors to {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(vectors, file, indent=2, ensure_ascii=False)
        print(f"✅ Successfully saved vectors to {output_file}")
    except Exception as e:
        print(f"❌ Error saving vectors: {e}")
        return
    
    # Print summary
    print("\n📊 Summary:")
    print(f"   • Total FAQ entries: {len(faq_data)}")
    print(f"   • Questions embedded: {len(questions)}")
    print(f"   • Vectors created: {len(vectors)}")
    print(f"   • Embedding dimensions: {len(embeddings[0]) if embeddings else 0}")
    
    # Show sample vector structure
    if vectors:
        print(f"\n📋 Sample vector structure:")
        sample = vectors[0]
        print(f"   • ID: {sample['id']}")
        print(f"   • Section: {sample['metadata']['section']}")
        print(f"   • Question: {sample['metadata']['question'][:50]}...")
        print(f"   • Vector dimensions: {len(sample['values'])}")
    
    print(f"\n🎉 Ready to upload to Pinecone! Use the vectors from {output_file}")

if __name__ == "__main__":
    main() 