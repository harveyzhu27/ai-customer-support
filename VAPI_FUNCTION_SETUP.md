# Vapi Function Setup Guide

## 🎯 **Configure Function Calling in Vapi Console**

### **Step 1: Go to Your Assistant**
1. In Vapi Console, go to your **"Aven FAQ Assistant"**
2. Click on **"Edit Assistant"**

### **Step 2: Add Function**
1. Scroll down to **"Functions"** section
2. Click **"Add Function"**
3. Use these settings:

```json
{
  "name": "search_aven_faq",
  "description": "Search Aven FAQ database for customer support questions",
  "url": "https://your-domain.com/api/search",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
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

### **Step 3: Set Function URL**
**Important:** You need to deploy your app to a public URL first!

**Option A: Deploy to Vercel (Recommended)**
1. Push your code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Import your repository
4. Deploy
5. Use the Vercel URL: `https://your-app.vercel.app/api/search`

**Option B: Use ngrok for local testing**
1. Install ngrok: `npm install -g ngrok`
2. Run: `ngrok http 3002`
3. Use the ngrok URL: `https://your-ngrok-url.ngrok.io/api/search`

### **Step 4: Test Function**
1. Save your assistant
2. Go to **"Test"** tab
3. Try a voice call to test the function

## 🚀 **Quick Deploy to Vercel**

If you want to deploy quickly:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Follow the prompts
# Use your GitHub account
# Choose your repository
# Deploy!
```

## 🧪 **Local Testing with ngrok**

```bash
# Install ngrok
npm install -g ngrok

# Start your dev server
npm run dev

# In another terminal, start ngrok
ngrok http 3002

# Copy the HTTPS URL and use it in Vapi Console
```

## ✅ **What Happens Next**

1. **User speaks** → Vapi converts to text
2. **Vapi calls your function** → Sends query to `/api/search`
3. **Your API searches** → Finds relevant FAQ answers
4. **AI generates response** → Contextual answer
5. **Vapi speaks back** → Text-to-speech response

## 🔧 **Troubleshooting**

**"Function call failed"**
- Check the URL is accessible
- Verify your API endpoint works
- Check browser console for errors

**"No response from function"**
- Ensure your API returns proper JSON
- Check CORS settings
- Verify function parameters match

Let me know when you've set up the function URL and we can test the voice calls! 🎤 