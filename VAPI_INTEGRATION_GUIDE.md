# Vapi Integration Guide for Aven FAQ Voice Assistant

## 🎯 **Overview**

This guide shows how to integrate Vapi with your existing FAQ search system to create a voice-enabled AI assistant.

## 🏗️ **Architecture**

```
User Voice → Vapi → Speech-to-Text → Your API → Pinecone Search → AI Answer → Text-to-Speech → User
```

## 📋 **Prerequisites**

1. ✅ FAQ embeddings generated and uploaded to Pinecone
2. ✅ Next.js API endpoint created (`/api/search`)
3. ✅ Vapi account (sign up at [vapi.ai](https://vapi.ai))

## 🚀 **Step 1: Install Required Dependencies**

```bash
npm install @pinecone-database/pinecone openai
```

## 🔧 **Step 2: Complete Your API Endpoint**

Update `src/app/api/search/route.ts` with the full implementation:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { Pinecone } from '@pinecone-database/pinecone';
import OpenAI from 'openai';

const pinecone = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY!,
});

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY!,
});

export async function POST(request: NextRequest) {
  try {
    const { query } = await request.json();

    if (!query) {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      );
    }

    // 1. Embed the user's query
    const embeddingResponse = await openai.embeddings.create({
      model: 'text-embedding-3-small',
      input: query,
    });

    const queryEmbedding = embeddingResponse.data[0].embedding;

    // 2. Search Pinecone for similar questions
    const index = pinecone.index('aven-faq');
    const searchResponse = await index.query({
      vector: queryEmbedding,
      topK: 3,
      includeMetadata: true,
    });

    if (!searchResponse.matches || searchResponse.matches.length === 0) {
      return NextResponse.json({
        answer: "I'm sorry, I couldn't find a relevant answer to your question. Please try rephrasing or contact Aven support directly.",
        confidence: 0,
        sources: []
      });
    }

    // 3. Prepare context from top matches
    const context = searchResponse.matches
      .map(match => {
        const metadata = match.metadata as any;
        return `Question: ${metadata.question}\nAnswer: ${metadata.answer}`;
      })
      .join('\n\n');

    // 4. Generate AI answer using the context
    const completion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'system',
          content: `You are a helpful Aven customer support assistant. Use the following FAQ context to answer the user's question. If the context doesn't contain relevant information, say you don't have enough information and suggest contacting Aven support.

FAQ Context:
${context}

Guidelines:
- Be concise and helpful
- Use a friendly, professional tone
- If you're not sure, suggest contacting Aven support
- Keep answers under 150 words for voice responses`
        },
        {
          role: 'user',
          content: query
        }
      ],
      max_tokens: 200,
      temperature: 0.7,
    });

    const answer = completion.choices[0].message.content;

    return NextResponse.json({
      answer,
      confidence: searchResponse.matches[0].score,
      sources: searchResponse.matches.map(match => ({
        question: (match.metadata as any).question,
        section: (match.metadata as any).section,
        score: match.score
      })),
      query
    });

  } catch (error) {
    console.error('Search API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## 🎤 **Step 3: Vapi Configuration**

### **3.1 Create Vapi Assistant**

1. Go to [Vapi Dashboard](https://console.vapi.ai/)
2. Click "Create Assistant"
3. Choose "Custom Assistant"

### **3.2 Configure Assistant Settings**

```json
{
  "name": "Aven FAQ Assistant",
  "description": "Voice assistant for Aven customer support questions",
  "model": "gpt-4",
  "voice": "jennifer",
  "language": "en-US"
}
```

### **3.3 Set Up Function Calling**

Add this function to your Vapi assistant:

```javascript
{
  "name": "search_aven_faq",
  "description": "Search Aven FAQ database for customer support questions",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The user's question about Aven services"
      }
    },
    "required": ["query"]
  }
}
```

### **3.4 Configure Function URL**

Set your function URL to:
```
https://your-domain.com/api/search
```

## 🎯 **Step 4: Vapi Assistant Prompt**

Use this system prompt in your Vapi assistant:

```
You are a helpful Aven customer support assistant. Your job is to help customers with questions about Aven's services.

When a customer asks a question:
1. Use the search_aven_faq function to find relevant information
2. Provide a helpful, concise answer based on the search results
3. If you don't have enough information, suggest contacting Aven support
4. Keep responses under 150 words for better voice experience

Be friendly, professional, and helpful. Always try to provide accurate information from the FAQ database.
```

## 📱 **Step 5: Update Your React Component**

Update your HeadstarterAssistant component to include Vapi integration:

```tsx
'use client';

import React, { useEffect, useState } from 'react';
import { useVapi } from '@vapi-ai/react';

const HeadstarterAssistant: React.FC = () => {
  const [isListening, setIsListening] = useState(false);
  const [lastMessage, setLastMessage] = useState('');
  
  const { start, stop, isActive, transcript, messages } = useVapi({
    assistantId: 'your-vapi-assistant-id',
    apiKey: process.env.NEXT_PUBLIC_VAPI_API_KEY,
  });

  const handleVoiceCall = async () => {
    if (isActive) {
      await stop();
      setIsListening(false);
    } else {
      await start();
      setIsListening(true);
    }
  };

  // Update status based on Vapi state
  useEffect(() => {
    if (isActive) {
      setStatus('connected');
    } else {
      setStatus('ready');
    }
  }, [isActive]);

  // Update last message
  useEffect(() => {
    if (messages.length > 0) {
      setLastMessage(messages[messages.length - 1].content);
    }
  }, [messages]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center overflow-hidden relative">
      {/* ... existing background particles ... */}

      <div className="relative z-10 w-96 max-w-[90vw]">
        <div className="bg-slate-900/90 border border-cyan-400/20 rounded-3xl p-12 text-center backdrop-blur-xl shadow-2xl shadow-black/50 relative overflow-hidden">
          {/* ... existing card content ... */}

          {/* Voice Status */}
          {isListening && (
            <div className="mb-4 p-3 bg-cyan-400/10 rounded-lg border border-cyan-400/20">
              <div className="text-cyan-400 text-sm font-medium mb-2">
                🎤 Listening...
              </div>
              {transcript && (
                <div className="text-white/80 text-xs">
                  "{transcript}"
                </div>
              )}
            </div>
          )}

          {/* Last Response */}
          {lastMessage && (
            <div className="mb-4 p-3 bg-green-400/10 rounded-lg border border-green-400/20">
              <div className="text-green-400 text-sm font-medium mb-2">
                💬 Response
              </div>
              <div className="text-white/80 text-xs">
                {lastMessage}
              </div>
            </div>
          )}

          {/* Voice Button */}
          <button
            onClick={handleVoiceCall}
            className={`w-full py-4 px-6 bg-gradient-to-br from-cyan-400 to-cyan-500 border-none rounded-2xl text-slate-900 text-lg font-bold cursor-pointer transition-all duration-300 relative overflow-hidden shadow-lg shadow-cyan-400/30 hover:shadow-xl hover:shadow-cyan-400/40 hover:-translate-y-0.5 active:translate-y-0 active:shadow-md active:shadow-cyan-400/30 ${
              isListening ? 'animate-pulse' : ''
            }`}
          >
            {isListening ? '🎤 Stop Listening' : '🎤 Ask Aven Assistant'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default HeadstarterAssistant;
```

## 🔑 **Step 6: Environment Variables**

Add to your `.env.local`:

```env
NEXT_PUBLIC_VAPI_API_KEY=your-vapi-api-key
PINECONE_API_KEY=your-pinecone-api-key
OPENAI_API_KEY=your-openai-api-key
```

## 🧪 **Step 7: Testing**

### **Test Your API Endpoint:**

```bash
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I make a payment?"}'
```

### **Test Vapi Integration:**

1. Deploy your app to a public URL (Vercel, Netlify, etc.)
2. Update the function URL in Vapi dashboard
3. Test the voice assistant through Vapi console

## 🎉 **What You'll Have**

✅ **Voice Input** - Users can ask questions by speaking  
✅ **Speech-to-Text** - Vapi converts speech to text  
✅ **FAQ Search** - Your API searches Pinecone for relevant answers  
✅ **AI Response** - GPT generates contextual answers  
✅ **Text-to-Speech** - Vapi speaks the response back to the user  

## 💡 **Pro Tips**

1. **Deploy to Production** - Vapi needs a public URL for webhooks
2. **Test Voice Quality** - Try different Vapi voices for best experience
3. **Monitor Usage** - Track API calls and costs
4. **Add Error Handling** - Handle network issues gracefully

## 🚀 **Next Steps**

1. Install dependencies: `npm install @pinecone-database/pinecone openai @vapi-ai/react`
2. Complete the API endpoint implementation
3. Set up your Vapi assistant
4. Update your React component
5. Test the voice integration

Let me know when you're ready to implement any specific part! 🎤 