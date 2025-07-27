// Test script for the API endpoint
const testAPI = async () => {
  const testQueries = [
    "How do I make a payment?",
    "What is the interest rate?",
    "Can I pay with a check?",
    "How long does it take to get my card?"
  ];

  console.log('🧪 Testing API Endpoint...\n');

  for (const query of testQueries) {
    try {
      console.log(`📝 Testing query: "${query}"`);
      
      const response = await fetch('http://localhost:3000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Response received:');
        console.log(`   Answer: ${data.answer?.substring(0, 100)}...`);
        console.log(`   Confidence: ${data.confidence}`);
        console.log(`   Sources: ${data.sources?.length || 0} found`);
      } else {
        const error = await response.text();
        console.log('❌ Error:', error);
      }
      
      console.log('---\n');
      
      // Wait a bit between requests
      await new Promise(resolve => setTimeout(resolve, 1000));
      
    } catch (error) {
      console.log('❌ Network error:', error.message);
      console.log('---\n');
    }
  }
};

// Run the test
testAPI(); 