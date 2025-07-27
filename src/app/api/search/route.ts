import { NextRequest, NextResponse } from 'next/server';
import { Pinecone } from '@pinecone-database/pinecone';
import OpenAI from 'openai';

// Initialize clients
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

    // 5. Prepare sources for reference
    const sources = searchResponse.matches.map(match => ({
      question: (match.metadata as any).question,
      section: (match.metadata as any).section,
      score: match.score
    }));

    return NextResponse.json({
      answer,
      confidence: searchResponse.matches[0].score,
      sources,
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