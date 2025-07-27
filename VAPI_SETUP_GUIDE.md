# Vapi Setup Guide for Aven FAQ Voice Assistant

## 🎯 **Quick Setup Steps**

### **1. Get Your Vapi API Key**

1. Go to [Vapi Console](https://console.vapi.ai/)
2. Sign up or log in
3. Go to **API Keys** section
4. Create a new API key
5. Copy the **Public Key** (starts with `pk_`)

### **2. Create Your Vapi Assistant**

1. In Vapi Console, click **"Create Assistant"**
2. Choose **"Custom Assistant"**
3. Configure with these settings:

```json
{
  "name": "Aven FAQ Assistant",
  "description": "Voice assistant for Aven customer support questions",
  "model": "gpt-4",
  "voice": "jennifer",
  "language": "en-US"
}
```

### **3. Set Up Function Calling**

Add this function to your assistant:

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

### **4. Configure Function URL**

Set your function URL to:
```
https://your-domain.com/api/search
```

**Note:** You'll need to deploy your app to a public URL (Vercel, Netlify, etc.) for this to work.

### **5. Set Environment Variables**

Create or update your `.env.local` file:

```env
# Vapi Configuration
NEXT_PUBLIC_VAPI_API_KEY=pk_your-vapi-public-key-here
NEXT_PUBLIC_VAPI_ASSISTANT_ID=your-assistant-id-here

# Your existing keys
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
```

### **6. Get Your Assistant ID**

1. In Vapi Console, go to your assistant
2. Copy the **Assistant ID** from the URL or settings
3. Add it to your environment variables

## 🧪 **Testing Your Setup**

### **Local Testing (Limited)**
- The voice functionality requires HTTPS and a public URL
- You can test the UI and button interactions locally
- Voice calls will work once deployed

### **Deploy to Test Voice**
1. Deploy your app to Vercel/Netlify
2. Update the function URL in Vapi Console
3. Test voice calls through your deployed app

## 🎤 **How It Works**

1. **User clicks "Start Voice Call"**
2. **Vapi connects** and starts listening
3. **User speaks** their question
4. **Vapi converts** speech to text
5. **Your API** searches FAQ database
6. **AI generates** contextual answer
7. **Vapi speaks** the response back

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **"Public key not found"**
   - Check your `NEXT_PUBLIC_VAPI_API_KEY` environment variable
   - Make sure it starts with `pk_`

2. **"Assistant not found"**
   - Verify your `NEXT_PUBLIC_VAPI_ASSISTANT_ID`
   - Check that the assistant exists in your Vapi account

3. **"Function call failed"**
   - Ensure your app is deployed to a public URL
   - Check that the function URL in Vapi Console is correct
   - Verify your API endpoint is working

4. **"No voice input"**
   - Check browser permissions for microphone
   - Ensure you're on HTTPS (required for voice)

## 🚀 **Next Steps**

Once you have your Vapi credentials:

1. **Add them to your environment variables**
2. **Deploy your app** to a public URL
3. **Update the function URL** in Vapi Console
4. **Test voice calls** through your deployed app

## 💡 **Pro Tips**

- **Test with simple questions** first
- **Monitor Vapi Console** for call logs and errors
- **Use different voices** to find the best fit
- **Adjust function calling** parameters as needed

Let me know when you have your Vapi credentials and I'll help you test the integration! 🎤 