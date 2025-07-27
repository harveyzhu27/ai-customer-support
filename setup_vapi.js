#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🎤 Vapi Setup Helper\n');

// Check if .env.local exists
const envPath = path.join(process.cwd(), '.env.local');
const templatePath = path.join(process.cwd(), 'env.template');

if (!fs.existsSync(envPath)) {
  console.log('📝 Creating .env.local file...');
  
  if (fs.existsSync(templatePath)) {
    fs.copyFileSync(templatePath, envPath);
    console.log('✅ Created .env.local from template');
  } else {
    // Create basic .env.local
    const envContent = `# Vapi Configuration
# Replace these with your actual Vapi credentials
NEXT_PUBLIC_VAPI_API_KEY=pk_your-vapi-public-key-here
NEXT_PUBLIC_VAPI_ASSISTANT_ID=your-assistant-id-here

# Your existing API keys (if you have them)
# OPENAI_API_KEY=your-openai-api-key
# PINECONE_API_KEY=your-pinecone-api-key
`;
    fs.writeFileSync(envPath, envContent);
    console.log('✅ Created .env.local file');
  }
} else {
  console.log('✅ .env.local already exists');
}

console.log('\n📋 Next Steps:');
console.log('1. Go to https://console.vapi.ai/');
console.log('2. Get your Public API Key (starts with pk_)');
console.log('3. Create an Assistant and get the Assistant ID');
console.log('4. Update .env.local with your actual values');
console.log('5. Restart your development server');
console.log('\n🎯 Your app will then have full voice functionality!'); 