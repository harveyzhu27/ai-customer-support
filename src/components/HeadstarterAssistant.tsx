'use client';

import React, { useEffect, useState } from 'react';

interface Particle {
  id: number;
  left: string;
  top: string;
  delay: string;
  duration: string;
}

const HeadstarterAssistant: React.FC = () => {
  const [particles, setParticles] = useState<Particle[]>([]);
  const [status, setStatus] = useState<'ready' | 'connecting' | 'connected'>('ready');
  const [isButtonClicked, setIsButtonClicked] = useState(false);

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

  const handleCall = () => {
    setIsButtonClicked(true);
    setStatus('connecting');

    // Simulate connection process
    setTimeout(() => {
      setStatus('connected');
      
      // Show a simple alert for now (replace with your backend integration)
      alert('Connected to Headstarter Assistant! 🚀\n\nThis is where you would integrate with your backend to start the call.');
      
      // Reset status after a delay
      setTimeout(() => {
        setStatus('ready');
      }, 2000);
    }, 1500);

    // Remove click animation
    setTimeout(() => {
      setIsButtonClicked(false);
    }, 600);
  };

  const getStatusColor = () => {
    switch (status) {
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
            Headstarter Assistant
          </h1>
          
          {/* Subtitle */}
          <p className="text-white/60 mb-12 font-normal">
            Ask any questions about Headstarter to Scotty
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
          <div className="flex items-center justify-center gap-2 mb-8">
            <div className={`w-2 h-2 rounded-full shadow-lg animate-pulse ${getStatusColor()}`} />
            <span className="text-white/80 text-sm font-medium">
              {status}
            </span>
          </div>

          {/* Call Button */}
          <button
            onClick={handleCall}
            className={`w-full py-4 px-6 bg-gradient-to-br from-cyan-400 to-cyan-500 border-none rounded-2xl text-slate-900 text-lg font-bold cursor-pointer transition-all duration-300 relative overflow-hidden shadow-lg shadow-cyan-400/30 hover:shadow-xl hover:shadow-cyan-400/40 hover:-translate-y-0.5 active:translate-y-0 active:shadow-md active:shadow-cyan-400/30 ${
              isButtonClicked ? 'animate-pulse' : ''
            }`}
          >
            {/* Button shine effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full hover:translate-x-full transition-transform duration-500" />
            
            Call Headstarter
          </button>
        </div>
      </div>


    </div>
  );
};

export default HeadstarterAssistant; 