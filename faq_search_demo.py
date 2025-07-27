import json
import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()

class FAQSearchEngine:
    def __init__(self, vectors_file: str = "aven_faq_vectors.json"):
        """
        Initialize the FAQ search engine.
        
        Args:
            vectors_file (str): Path to the vectors JSON file
        """
        self.vectors_file = vectors_file
        self.vectors = []
        self.questions = []
        self.answers = []
        self.sections = []
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)
        
        # Load vectors
        self.load_vectors()
    
    def load_vectors(self):
        """Load vectors from the JSON file."""
        try:
            with open(self.vectors_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            self.vectors = [item['values'] for item in data]
            self.questions = [item['metadata']['question'] for item in data]
            self.answers = [item['metadata']['answer'] for item in data]
            self.sections = [item['metadata']['section'] for item in data]
            
            print(f"✅ Loaded {len(self.vectors)} FAQ vectors")
            
        except FileNotFoundError:
            print(f"❌ Error: {self.vectors_file} not found")
            print("Please run the embedding script first: python embed_aven_faq_enhanced.py")
            raise
        except Exception as e:
            print(f"❌ Error loading vectors: {e}")
            raise
    
    def embed_query(self, query: str) -> List[float]:
        """
        Embed a search query using OpenAI.
        
        Args:
            query (str): The search query
            
        Returns:
            List[float]: The query embedding
        """
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=[query]
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"❌ Error embedding query: {e}")
            raise
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar FAQ entries.
        
        Args:
            query (str): The search query
            top_k (int): Number of top results to return
            
        Returns:
            List[Dict[str, Any]]: List of search results with scores
        """
        # Embed the query
        query_embedding = self.embed_query(query)
        
        # Calculate similarities
        similarities = []
        for vector in self.vectors:
            similarity = cosine_similarity([query_embedding], [vector])[0][0]
            similarities.append(similarity)
        
        # Get top-k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                'rank': len(results) + 1,
                'question': self.questions[idx],
                'answer': self.answers[idx],
                'section': self.sections[idx],
                'similarity_score': float(similarities[idx]),
                'similarity_percentage': f"{similarities[idx] * 100:.1f}%"
            })
        
        return results
    
    def interactive_search(self):
        """Run an interactive search session."""
        print("🔍 Aven FAQ Search Engine")
        print("=" * 50)
        print("Type your questions about Aven. Type 'quit' to exit.")
        print()
        
        while True:
            try:
                query = input("❓ Your question: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not query:
                    continue
                
                print(f"\n🔍 Searching for: '{query}'")
                print("-" * 50)
                
                results = self.search(query, top_k=3)
                
                if results:
                    for result in results:
                        print(f"\n📋 Rank {result['rank']} ({result['similarity_percentage']} match)")
                        print(f"📂 Section: {result['section']}")
                        print(f"❓ Question: {result['question']}")
                        print(f"💡 Answer: {result['answer'][:200]}...")
                        print("-" * 30)
                else:
                    print("❌ No results found.")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Please try again.")

def main():
    """Main function to run the search demo."""
    try:
        # Initialize search engine
        search_engine = FAQSearchEngine()
        
        # Run interactive search
        search_engine.interactive_search()
        
    except Exception as e:
        print(f"❌ Failed to initialize search engine: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Run the embedding script: python embed_aven_faq_enhanced.py")
        print("   2. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
        print("   3. Installed dependencies: pip install -r requirements_embedding.txt")

if __name__ == "__main__":
    main() 