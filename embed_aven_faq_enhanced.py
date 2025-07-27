import json
import os
import re
from typing import List, Dict, Any, Optional
from openai import OpenAI
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def parse_faq_from_text(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse FAQ data from the text file format.
    
    Args:
        file_path (str): Path to the text file containing FAQ data
        
    Returns:
        List[Dict[str, Any]]: List of FAQ entries
    """
    faq_entries = []
    current_section = ""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split by sections
        sections = re.split(r'Section: (.+?)\n-+\n', content)[1:]  # Skip first empty element
        
        for i in range(0, len(sections), 2):
            if i + 1 < len(sections):
                section_name = sections[i].strip()
                section_content = sections[i + 1]
                
                # Extract Q&A pairs from section
                qa_pairs = re.findall(r'Question \d+: (.+?)\nAnswer \d+: (.+?)(?=\nQuestion \d+:|$)', 
                                    section_content, re.DOTALL)
                
                for question, answer in qa_pairs:
                    faq_entries.append({
                        "section": section_name,
                        "question": question.strip(),
                        "answer": answer.strip(),
                        "source_url": "https://www.aven.com/support"
                    })
        
        print(f"✅ Parsed {len(faq_entries)} FAQ entries from text file {file_path}")
        return faq_entries
        
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        return []
    except Exception as e:
        print(f"❌ Error parsing text file {file_path}: {e}")
        return []

def load_faq_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load FAQ data from JSON or text file.
    
    Args:
        file_path (str): Path to the file containing FAQ data
        
    Returns:
        List[Dict[str, Any]]: List of FAQ entries with section, question, answer, and source_url
    """
    if file_path.endswith('.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            print(f"✅ Loaded {len(data)} FAQ entries from JSON file {file_path}")
            return data
        except FileNotFoundError:
            print(f"❌ Error: File {file_path} not found")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in {file_path}: {e}")
            return []
    elif file_path.endswith('.txt'):
        return parse_faq_from_text(file_path)
    else:
        print(f"❌ Error: Unsupported file format. Please use .json or .txt files")
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
    total_batches = (len(questions) + batch_size - 1) // batch_size
    
    print(f"🔄 Processing {len(questions)} questions in {total_batches} batches...")
    
    for i in range(0, len(questions), batch_size):
        batch = questions[i:i + batch_size]
        batch_num = i // batch_size + 1
        
        try:
            response = client.embeddings.create(
                model=model,
                input=batch
            )
            
            batch_embeddings = [embedding.embedding for embedding in response.data]
            embeddings.extend(batch_embeddings)
            
            print(f"✅ Embedded batch {batch_num}/{total_batches} ({len(batch)} questions)")
            
            # Add a small delay to respect rate limits
            time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Error embedding batch {batch_num}: {e}")
            # Add empty embeddings for failed batch
            embeddings.extend([[0.0] * 1536] * len(batch))  # text-embedding-3-small has 1536 dimensions
    
    return embeddings

def create_pinecone_vectors(faq_data: List[Dict[str, Any]], embeddings: List[List[float]], 
                          id_prefix: str = "aven_faq") -> List[Dict[str, Any]]:
    """
    Create Pinecone-ready vectors with metadata.
    
    Args:
        faq_data (List[Dict[str, Any]]): Original FAQ data
        embeddings (List[List[float]]): Embedding vectors
        id_prefix (str): Prefix for vector IDs
        
    Returns:
        List[Dict[str, Any]]: Pinecone-ready vectors with id, values, and metadata
    """
    vectors = []
    
    for i, (faq_entry, embedding) in enumerate(zip(faq_data, embeddings)):
        vector = {
            "id": f"{id_prefix}_{i:04d}",  # Create unique ID with zero-padding
            "values": embedding,
            "metadata": {
                "section": faq_entry["section"],
                "question": faq_entry["question"],
                "answer": faq_entry["answer"],
                "source_url": faq_entry["source_url"],
                "type": "faq",
                "company": "aven",
                "embedding_model": "text-embedding-3-small"
            }
        }
        vectors.append(vector)
    
    return vectors

def validate_vectors(vectors: List[Dict[str, Any]]) -> bool:
    """
    Validate the created vectors for Pinecone compatibility.
    
    Args:
        vectors (List[Dict[str, Any]]): List of vectors to validate
        
    Returns:
        bool: True if all vectors are valid, False otherwise
    """
    if not vectors:
        print("❌ No vectors to validate")
        return False
    
    required_fields = ["id", "values", "metadata"]
    required_metadata = ["section", "question", "answer", "source_url"]
    
    for i, vector in enumerate(vectors):
        # Check required fields
        for field in required_fields:
            if field not in vector:
                print(f"❌ Vector {i} missing required field: {field}")
                return False
        
        # Check metadata fields
        for field in required_metadata:
            if field not in vector["metadata"]:
                print(f"❌ Vector {i} missing required metadata field: {field}")
                return False
        
        # Check vector dimensions
        if len(vector["values"]) != 1536:
            print(f"❌ Vector {i} has incorrect dimensions: {len(vector['values'])} (expected 1536)")
            return False
    
    print(f"✅ Validated {len(vectors)} vectors successfully")
    return True

def main():
    """
    Main function to process FAQ data and create Pinecone-ready vectors.
    """
    # Configuration
    faq_files = [
        "aven_support_faq_correct.json",
        "aven_support_faq_correct.txt"
    ]
    output_file = "aven_faq_vectors.json"
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("  or create a .env file with: OPENAI_API_KEY=your-api-key-here")
        return
    
    # Try to load FAQ data from available files
    faq_data = []
    for file_path in faq_files:
        if os.path.exists(file_path):
            print(f"📖 Loading FAQ data from {file_path}...")
            faq_data = load_faq_data(file_path)
            if faq_data:
                break
    
    if not faq_data:
        print("❌ No FAQ data loaded. Please ensure one of these files exists:")
        for file_path in faq_files:
            print(f"   • {file_path}")
        return
    
    # Extract questions
    questions = [entry["question"] for entry in faq_data]
    print(f"📝 Extracted {len(questions)} questions for embedding")
    
    # Show sample questions
    print("\n📋 Sample questions:")
    for i, question in enumerate(questions[:3]):
        print(f"   {i+1}. {question[:60]}...")
    if len(questions) > 3:
        print(f"   ... and {len(questions) - 3} more")
    
    # Create embeddings
    print(f"\n🤖 Creating embeddings with OpenAI text-embedding-3-small...")
    client = OpenAI(api_key=api_key)
    embeddings = create_embeddings(questions, client)
    
    if len(embeddings) != len(questions):
        print(f"❌ Warning: Number of embeddings ({len(embeddings)}) doesn't match number of questions ({len(questions)})")
        return
    
    # Create Pinecone-ready vectors
    print("🔧 Creating Pinecone-ready vectors...")
    vectors = create_pinecone_vectors(faq_data, embeddings)
    
    # Validate vectors
    if not validate_vectors(vectors):
        print("❌ Vector validation failed")
        return
    
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
        print(f"   • Metadata fields: {list(sample['metadata'].keys())}")
    
    print(f"\n🎉 Ready to upload to Pinecone! Use the vectors from {output_file}")
    print(f"💡 You can now use these vectors with Pinecone's upsert() method")

if __name__ == "__main__":
    main() 