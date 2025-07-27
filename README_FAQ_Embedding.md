# Aven FAQ Embedding Pipeline

This project provides a complete pipeline to embed Aven Support FAQ questions using OpenAI's text-embedding-3-small model and prepare them for Pinecone vector database.

## 📁 Files Overview

- **`embed_aven_faq.py`** - Basic embedding script
- **`embed_aven_faq_enhanced.py`** - Enhanced version with better error handling and text file support
- **`pinecone_upload_example.py`** - Example script for uploading to Pinecone
- **`requirements_embedding.txt`** - Python dependencies
- **`aven_support_faq_correct.json`** - Source FAQ data (JSON format)
- **`aven_support_faq_correct.txt`** - Source FAQ data (Text format)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_embedding.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in your project root:

```env
OPENAI_API_KEY=your-openai-api-key-here
PINECONE_API_KEY=your-pinecone-api-key-here
```

Or set them in your terminal:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
export PINECONE_API_KEY="your-pinecone-api-key-here"
```

### 3. Generate Embeddings

```bash
python embed_aven_faq_enhanced.py
```

This will:
- Load FAQ data from either JSON or text file
- Create embeddings using OpenAI's text-embedding-3-small model
- Generate Pinecone-ready vectors
- Save results to `aven_faq_vectors.json`

### 4. Upload to Pinecone (Optional)

```bash
python pinecone_upload_example.py
```

## 📊 Output Format

The generated vectors follow this structure:

```json
[
  {
    "id": "aven_faq_0000",
    "values": [0.123, -0.456, ...], // 1536-dimensional vector
    "metadata": {
      "section": "Trending Articles",
      "question": "Is the rate variable?",
      "answer": "The Aven Card is a variable rate credit card...",
      "source_url": "https://www.aven.com/support",
      "type": "faq",
      "company": "aven",
      "embedding_model": "text-embedding-3-small"
    }
  }
]
```

## 🔧 Script Details

### `embed_aven_faq_enhanced.py`

**Features:**
- ✅ Supports both JSON and text file formats
- ✅ Batch processing to handle rate limits
- ✅ Comprehensive error handling
- ✅ Vector validation
- ✅ Progress tracking
- ✅ Detailed logging

**Usage:**
```bash
python embed_aven_faq_enhanced.py
```

**Output:**
- `aven_faq_vectors.json` - Pinecone-ready vectors

### `pinecone_upload_example.py`

**Features:**
- ✅ Automatic index creation
- ✅ Batch upload support
- ✅ Index statistics
- ✅ Search example structure

**Usage:**
```bash
python pinecone_upload_example.py
```

## 📈 Performance

- **Embedding Model:** OpenAI text-embedding-3-small (1536 dimensions)
- **Batch Size:** 100 questions per batch
- **Rate Limiting:** 0.1 second delay between batches
- **Processing Time:** ~1-2 minutes for ~100 FAQ entries

## 🔍 Example Usage

### Basic Embedding

```python
from embed_aven_faq_enhanced import load_faq_data, create_embeddings, create_pinecone_vectors
from openai import OpenAI

# Load FAQ data
faq_data = load_faq_data("aven_support_faq_correct.json")

# Create embeddings
client = OpenAI(api_key="your-api-key")
questions = [entry["question"] for entry in faq_data]
embeddings = create_embeddings(questions, client)

# Create Pinecone vectors
vectors = create_pinecone_vectors(faq_data, embeddings)
```

### Pinecone Integration

```python
from pinecone import Pinecone
import json

# Load vectors
with open("aven_faq_vectors.json", "r") as f:
    vectors = json.load(f)

# Upload to Pinecone
pc = Pinecone(api_key="your-pinecone-key")
index = pc.Index("aven-faq")

# Upsert vectors
index.upsert(vectors=vectors)
```

## 🛠️ Customization

### Change Embedding Model

```python
# In embed_aven_faq_enhanced.py, modify the model parameter:
embeddings = create_embeddings(questions, client, model="text-embedding-3-large")
```

### Modify Vector Structure

```python
# In create_pinecone_vectors function, add custom metadata:
vector = {
    "id": f"{id_prefix}_{i:04d}",
    "values": embedding,
    "metadata": {
        "section": faq_entry["section"],
        "question": faq_entry["question"],
        "answer": faq_entry["answer"],
        "source_url": faq_entry["source_url"],
        "type": "faq",
        "company": "aven",
        "embedding_model": "text-embedding-3-small",
        "custom_field": "custom_value"  # Add your custom fields
    }
}
```

### Change Batch Size

```python
# In create_embeddings function, modify batch_size:
batch_size = 50  # Smaller batches for slower connections
```

## 🔒 Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Consider using a `.env` file (included in `.gitignore`)
- Monitor API usage to avoid unexpected costs

## 📋 Requirements

- Python 3.7+
- OpenAI API key
- Pinecone API key (for upload functionality)
- Internet connection for API calls

## 🐛 Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not set"**
   - Ensure your API key is set in environment variables
   - Check that the `.env` file exists and is properly formatted

2. **"File not found"**
   - Ensure `aven_support_faq_correct.json` or `aven_support_faq_correct.txt` exists
   - Check file paths and permissions

3. **Rate limiting errors**
   - The script includes built-in rate limiting
   - Increase the `time.sleep()` delay if needed

4. **Pinecone connection issues**
   - Verify your Pinecone API key
   - Check your internet connection
   - Ensure the index name is unique

### Debug Mode

Add debug logging by modifying the script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your API keys and permissions
3. Ensure all dependencies are installed
4. Check the OpenAI and Pinecone documentation

## 📄 License

This project is provided as-is for educational and development purposes. 