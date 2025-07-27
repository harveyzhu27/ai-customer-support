'use client';

import { useState } from 'react';

export default function TestAPIPage() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const testQueries = [
    "How do I make a payment?",
    "What is the interest rate?",
    "Can I pay with a check?",
    "How long does it take to get my card?"
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResponse(null);

    try {
      const res = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();

      if (res.ok) {
        setResponse(data);
      } else {
        setError(data.error || 'API request failed');
      }
    } catch (err) {
      setError('Network error: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickTest = async (testQuery: string) => {
    setQuery(testQuery);
    setLoading(true);
    setError('');
    setResponse(null);

    try {
      const res = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: testQuery }),
      });

      const data = await res.json();

      if (res.ok) {
        setResponse(data);
      } else {
        setError(data.error || 'API request failed');
      }
    } catch (err) {
      setError('Network error: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">🧪 API Test Page</h1>
        
        {/* Quick Test Buttons */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-white mb-4">Quick Tests:</h2>
          <div className="flex flex-wrap gap-2">
            {testQueries.map((testQuery, index) => (
              <button
                key={index}
                onClick={() => handleQuickTest(testQuery)}
                disabled={loading}
                className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 disabled:bg-gray-600 text-white rounded-lg text-sm transition-colors"
              >
                {testQuery.substring(0, 20)}...
              </button>
            ))}
          </div>
        </div>

        {/* Custom Query Form */}
        <div className="bg-white/10 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-white mb-4">Custom Query:</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="query" className="block text-white text-sm font-medium mb-2">
                Your Question:
              </label>
              <input
                type="text"
                id="query"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask a question about Aven..."
                className="w-full px-4 py-2 bg-white/20 border border-white/30 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-cyan-400"
                disabled={loading}
              />
            </div>
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="px-6 py-2 bg-cyan-500 hover:bg-cyan-600 disabled:bg-gray-600 text-white rounded-lg transition-colors"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-4 mb-4">
            <div className="text-blue-400">⏳ Searching for answers...</div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4 mb-4">
            <div className="text-red-400">❌ Error: {error}</div>
          </div>
        )}

        {/* Response */}
        {response && (
          <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-green-400 mb-4">✅ Response:</h3>
            
            <div className="space-y-4">
              <div>
                <h4 className="text-white font-medium mb-2">Query:</h4>
                <p className="text-white/80">{response.query}</p>
              </div>
              
              <div>
                <h4 className="text-white font-medium mb-2">Answer:</h4>
                <p className="text-white/80">{response.answer}</p>
              </div>
              
              <div>
                <h4 className="text-white font-medium mb-2">Confidence:</h4>
                <p className="text-white/80">{(response.confidence * 100).toFixed(1)}%</p>
              </div>
              
              {response.sources && response.sources.length > 0 && (
                <div>
                  <h4 className="text-white font-medium mb-2">Sources:</h4>
                  <div className="space-y-2">
                    {response.sources.map((source: any, index: number) => (
                      <div key={index} className="bg-white/5 rounded p-3">
                        <p className="text-white/80 text-sm">
                          <strong>Question:</strong> {source.question}
                        </p>
                        <p className="text-white/60 text-xs">
                          <strong>Section:</strong> {source.section} | <strong>Score:</strong> {(source.score * 100).toFixed(1)}%
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 