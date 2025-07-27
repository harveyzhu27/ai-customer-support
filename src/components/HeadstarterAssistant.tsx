'use client';

import React, { useEffect, useState } from 'react';

interface Particle {
  id: number;
  left: string;
  top: string;
  delay: string;
  duration: string;
}

const AvenAssistant: React.FC = () => {
  const [particles, setParticles] = useState<Particle[]>([]);
  const [isButtonClicked, setIsButtonClicked] = useState(false);
  const [userTranscript, setUserTranscript] = useState('');
  const [assistantTranscript, setAssistantTranscript] = useState('');
  const [isCallActive, setIsCallActive] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected'>('disconnected');
  const [vapiInitialized, setVapiInitialized] = useState(false);
  
  // Client-side Vapi integration using Web SDK
  useEffect(() => {
    // Only run on client side
    if (typeof window === 'undefined') return;
    
    // Debug: Check environment variables
    console.log('🔍 Environment Variables Check:');
    console.log('NEXT_PUBLIC_VAPI_API_KEY:', process.env.NEXT_PUBLIC_VAPI_API_KEY ? '✅ Set' : '❌ Not set');
    console.log('NEXT_PUBLIC_VAPI_ASSISTANT_ID:', process.env.NEXT_PUBLIC_VAPI_ASSISTANT_ID ? '✅ Set' : '❌ Not set');
    
    const initVapi = async () => {
      try {
        // Import Vapi Web SDK
        const Vapi = (await import('@vapi-ai/web')).default;
        
        // Check if API key is available
        const apiKey = process.env.NEXT_PUBLIC_VAPI_API_KEY || '';
        if (!apiKey) {
          throw new Error('Vapi API key is not configured. Please check your .env.local file.');
        }
        
        // Initialize Vapi with your configuration
        const vapi = new Vapi(apiKey);
        
        // Set up event listeners based on official documentation
        vapi.on('call-start', () => {
          setConnectionStatus('connected');
          setIsCallActive(true);
          setUserTranscript('');
          setAssistantTranscript('');
          console.log('🎤 Call started');
        });
        
        vapi.on('call-end', () => {
          setConnectionStatus('disconnected');
          setIsCallActive(false);
          console.log('📞 Call ended');
        });
        
        vapi.on('speech-start', () => {
          setIsSpeaking(true);
        });
        
        vapi.on('speech-end', () => {
          setIsSpeaking(false);
        });
        
        // Handle messages and transcripts
        vapi.on('message', (message: { type: string; role: string; transcript: string }) => {
          console.log('📨 Message received:', message);
          
          if (message.type === 'transcript') {
            if (message.role === 'user') {
              setUserTranscript(message.transcript);
            } else if (message.role === 'assistant') {
              setAssistantTranscript(message.transcript);
            }
          }
        });
        
        vapi.on('error', (error: unknown) => {
          console.error('Vapi error:', error);
          setConnectionStatus('disconnected');
          setIsCallActive(false);
        });
        
        // Store Vapi instance globally for use in handleCall
        (window as { vapi?: typeof vapi }).vapi = vapi;
        setVapiInitialized(true);
        
        console.log('✅ Vapi Web SDK initialized successfully');
        
      } catch (error) {
        console.error('Failed to initialize Vapi:', error);
      }
    };
    
    initVapi();
  }, []);

  useEffect(() => {
    // Create floating particles
    const particleCount = 50;
    const newParticles: Particle[] = [];
    
    for (let i = 0; i < particleCount; i++) {
      newParticles.push({
        id: i,
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        delay: `${Math.random() * 6}s`,
        duration: `${Math.random() * 3 + 4}s`,
      });
    }
    
    setParticles(newParticles);
  }, []);

  const handleCall = async () => {
    setIsButtonClicked(true);
    
    try {
      // Check if Vapi is available
      const globalWindow = window as typeof window & { vapi?: unknown };
      if (typeof window === 'undefined' || !globalWindow.vapi) {
        return;
      }
      
      const vapi = globalWindow.vapi as { stop: () => void; start: (assistantId: string) => Promise<void> };
      
      // Check if assistant ID is configured
      const assistantId = process.env.NEXT_PUBLIC_VAPI_ASSISTANT_ID || '';
      if (!assistantId) {
        return;
      }
      
      if (isCallActive) {
        // End the call if it's active
        vapi.stop();
      } else {
        // Start a new call with your assistant ID
        console.log('🎤 Starting call with assistant:', assistantId);
        await vapi.start(assistantId);
      }
          } catch (error) {
        console.error('❌ Error with Vapi call:', error);
      } finally {
      // Remove click animation
      setTimeout(() => {
        setIsButtonClicked(false);
      }, 600);
    }
  };

  const getStatusColor = () => {
    if (isCallActive) {
      return 'bg-green-500 shadow-green-500/60';
    }
    
    switch (connectionStatus) {
      case 'connecting':
        return 'bg-orange-500 shadow-orange-500/60';
      case 'connected':
        return 'bg-green-500 shadow-green-500/60';
      default:
        return 'bg-cyan-400 shadow-cyan-400/60';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center overflow-hidden relative">
      {/* Background Particles */}
      <div className="absolute inset-0 overflow-hidden">
        {particles.map((particle) => (
          <div
            key={particle.id}
            className="absolute w-0.5 h-0.5 bg-cyan-400/30 rounded-full animate-float"
            style={{
              left: particle.left,
              top: particle.top,
              animationDelay: particle.delay,
              animationDuration: particle.duration,
            }}
          />
        ))}
      </div>

      {/* Main Container */}
      <div className="relative z-10 w-96 max-w-[90vw]">
        <div className="bg-slate-900/90 border border-cyan-400/20 rounded-3xl p-12 text-center backdrop-blur-xl shadow-2xl shadow-black/50 relative overflow-hidden">
          {/* Card Background Gradient */}
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/5 via-cyan-400/[0.02] to-cyan-400/5 rounded-3xl -z-10" />

          {/* Title */}
          <h1 className="text-3xl font-bold text-cyan-400 mb-2 drop-shadow-[0_0_20px_rgba(0,255,200,0.5)] tracking-tight">
            Aven Assistant
          </h1>
          
          {/* Subtitle */}
          <p className="text-white/60 mb-12 font-normal">
            Ask any questions about Aven to Suki
          </p>

          {/* Avatar */}
          <div className="w-20 h-20 mx-auto mb-8 relative">
            <div className="w-full h-full bg-gradient-to-br from-cyan-400 to-cyan-500 rounded-full flex items-center justify-center relative shadow-[0_0_30px_rgba(0,255,200,0.4),inset_0_2px_4px_rgba(255,255,255,0.2)]">
              {/* Animated border */}
              <div className="absolute -inset-0.5 bg-gradient-to-br from-cyan-400 via-cyan-500 to-cyan-400 rounded-full -z-10 animate-spin-slow" />
              
              {/* Icon */}
              <svg className="w-10 h-10 fill-slate-900" viewBox="0 0 24 24">
                <path d="M12 2L13.09 8.26L19.6 4.7L16.04 11.26L22.3 12L16.04 12.74L19.6 19.3L13.09 15.74L12 22L10.91 15.74L4.4 19.3L7.96 12.74L1.7 12L7.96 11.26L4.4 4.7L10.91 8.26L12 2Z"/>
              </svg>
            </div>
          </div>

          {/* Status */}
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className={`w-2 h-2 rounded-full shadow-lg animate-pulse ${getStatusColor()}`} />
            <span className="text-white/80 text-sm font-medium">
              {isCallActive ? 'connected' : connectionStatus}
            </span>
          </div>

          {/* Voice Status */}
          {!vapiInitialized && (
            <div className="mb-4 p-3 bg-orange-400/10 rounded-lg border border-orange-400/20">
              <div className="text-orange-400 text-sm font-medium mb-2">
                ⚙️ Initializing Voice...
              </div>
              <div className="text-white/80 text-xs">
                Setting up Vapi connection...
              </div>
            </div>
          )}
          
          {/* Voice Status */}
          {isCallActive && (
            <div className="mb-4 p-3 bg-cyan-400/10 rounded-lg border border-cyan-400/20">
              <div className="text-cyan-400 text-sm font-medium mb-2">
                🎤 {isSpeaking ? 'Suki Speaking...' : 'Listening...'}
              </div>
              {userTranscript && (
                <div className="text-white/80 text-xs mb-2">
                  <strong>You:</strong> &ldquo;{userTranscript}&rdquo;
                </div>
              )}
            </div>
          )}

          {/* Assistant Response */}
          {assistantTranscript && (
            <div className="mb-4 p-3 bg-green-400/10 rounded-lg border border-green-400/20">
              <div className="text-green-400 text-sm font-medium mb-2">
                💬 Suki
              </div>
              <div className="text-white/80 text-xs">
                &ldquo;{assistantTranscript}&rdquo;
              </div>
            </div>
          )}

          {/* Call Button */}
          <button
            onClick={handleCall}
            disabled={isButtonClicked}
            className={`w-full py-4 px-6 bg-gradient-to-br from-cyan-400 to-cyan-500 border-none rounded-2xl text-slate-900 text-lg font-bold cursor-pointer transition-all duration-300 relative overflow-hidden shadow-lg shadow-cyan-400/30 hover:shadow-xl hover:shadow-cyan-400/40 hover:-translate-y-0.5 active:translate-y-0 active:shadow-md active:shadow-cyan-400/30 disabled:opacity-50 disabled:cursor-not-allowed ${
              isCallActive ? 'animate-pulse' : ''
            }`}
          >
            {/* Button shine effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full hover:translate-x-full transition-transform duration-500" />
            
            {isCallActive ? '🎤 End Call' : vapiInitialized ? '🎤 Start Voice Call' : '🎤 Initializing...'}
          </button>
        </div>
      </div>


    </div>
  );
};

export default AvenAssistant; 