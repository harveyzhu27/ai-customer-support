// Simple test to verify Vapi Web SDK integration
console.log('🧪 Testing Vapi Web SDK Integration...');

// Check if Vapi Web SDK is available
try {
  const Vapi = require('@vapi-ai/web').default;
  console.log('✅ Vapi Web SDK imported successfully');
  
  // Load environment variables from .env.local
  const fs = require('fs');
  const path = require('path');
  
  const envPath = path.join(process.cwd(), '.env.local');
  if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    const envVars = {};
    
    envContent.split('\n').forEach(line => {
      const match = line.match(/^([^#][^=]+)=(.*)$/);
      if (match) {
        envVars[match[1]] = match[2];
      }
    });
    
    const apiKey = envVars.NEXT_PUBLIC_VAPI_API_KEY;
    const assistantId = envVars.NEXT_PUBLIC_VAPI_ASSISTANT_ID;
    
    if (apiKey && apiKey !== 'pk_your-vapi-public-key-here') {
      console.log('✅ Vapi API Key configured:', apiKey.substring(0, 10) + '...');
    } else {
      console.log('⚠️  Vapi API Key not configured');
    }
    
    if (assistantId && assistantId !== 'your-assistant-id-here') {
      console.log('✅ Vapi Assistant ID configured:', assistantId.substring(0, 10) + '...');
    } else {
      console.log('⚠️  Vapi Assistant ID not configured');
    }
  } else {
    console.log('⚠️  .env.local file not found');
  }
  
  console.log('\n🎯 Ready to test voice calls!');
  console.log('1. Make sure your app is running (npm run dev)');
  console.log('2. Click the "Start Voice Call" button');
  console.log('3. Allow microphone permissions');
  console.log('4. Speak your question');
  
} catch (error) {
  console.error('❌ Error testing Vapi integration:', error);
} 