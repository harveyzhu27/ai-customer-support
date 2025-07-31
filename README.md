# AI Customer Support App

A **full-stack AI customer support platform** that combines **real-time voice AI**, **semantic search**, and **context-aware responses** to deliver intelligent and interactive support experiences.  
Built with **Next.js 15**, **TypeScript**, **Vapi AI**, **OpenAI**, and **Pinecone**, the app integrates voice calls, embeddings-based search, and modern UI for seamless support interactions.

---

## 🚀 Features

### 1. Real-Time Voice AI
- **Voice calls in the browser** using **Vapi AI Web SDK**
- **Live transcription** for both user and assistant dialogue
- **Voice synthesis** for AI responses
- **Connection management** with visual feedback and error handling

### 2. Semantic Search API
- **Vector search** using **OpenAI embeddings** + **Pinecone vector database**
- **Context-aware responses** with **GPT-3.5-turbo**
- **Confidence scoring** and **source attribution** for answers
- **Next.js API routes** for query processing and data retrieval

### 3. Data Ingestion & Processing
- **Web scraping** (Selenium + BeautifulSoup) for FAQ and support data
- **Vector embeddings** stored in Pinecone for fast similarity search
- **Metadata management** for source tracking and contextual responses

---

## 🛠️ Tech Stack

**Frontend**  
- Next.js 15 + React 19 + TypeScript  
- Tailwind CSS + Shadcn UI + Lucide React  
- Framer Motion for animations  

**Backend & AI**  
- Next.js API Routes for serverless endpoints  
- OpenAI API for NLP and response generation  
- Pinecone vector database for semantic search  
- Vapi AI for real-time voice calls and transcription  

**Other Tools**  
- Node.js runtime  
- ESLint + Prettier for clean code  
- Turbopack for fast development builds  

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-customer-support-app.git
cd ai-customer-support-app

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Add API keys for OpenAI, Vapi, and Pinecone

# Start the development server
npm run dev
