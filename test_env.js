// Simple test to check environment variables
const fs = require('fs');
const path = require('path');

console.log('🔍 Testing Environment Variables...\n');

// Read .env.local file
const envPath = path.join(process.cwd(), '.env.local');
if (fs.existsSync(envPath)) {
  console.log('✅ .env.local file found');
  
  const envContent = fs.readFileSync(envPath, 'utf8');
  console.log('\n📄 File contents:');
  console.log(envContent);
  
  // Parse environment variables
  const envVars = {};
  envContent.split('\n').forEach(line => {
    const match = line.match(/^([^#][^=]+)=(.*)$/);
    if (match) {
      envVars[match[1]] = match[2];
    }
  });
  
  console.log('\n🔑 Parsed variables:');
  console.log('NEXT_PUBLIC_VAPI_API_KEY:', envVars.NEXT_PUBLIC_VAPI_API_KEY ? 
    envVars.NEXT_PUBLIC_VAPI_API_KEY.substring(0, 10) + '...' : 'NOT FOUND');
  console.log('NEXT_PUBLIC_VAPI_ASSISTANT_ID:', envVars.NEXT_PUBLIC_VAPI_ASSISTANT_ID ? 
    envVars.NEXT_PUBLIC_VAPI_ASSISTANT_ID.substring(0, 10) + '...' : 'NOT FOUND');
    
} else {
  console.log('❌ .env.local file not found');
} 