import React from 'react';
import { Shield, MessageSquare, Image, CreditCard, Info } from 'lucide-react';

interface HeaderProps {
  activeTab: 'text' | 'image' | 'upi' | 'how-it-works';
  setActiveTab: (tab: 'text' | 'image' | 'upi' | 'how-it-works') => void;
  apiConnected: boolean;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab, apiConnected }) => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-col sm:flex-row items-center justify-between gap-4">
        
        {/* Brand Logo & Title */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('text')}>
          <div className="p-2.5 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl shadow-lg shadow-emerald-500/20">
            <Shield className="w-6 h-6 text-slate-950 font-bold" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">UPI-Shield</h1>
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                CC-GFG-02
              </span>
            </div>
            <p className="text-xs text-slate-400">Contextual Digital Payment Scam & Coercion Detector</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1 bg-slate-950/60 p-1.5 rounded-xl border border-slate-800 text-sm font-medium">
          <button
            onClick={() => setActiveTab('text')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all ${
              activeTab === 'text'
                ? 'bg-emerald-500 text-slate-950 shadow font-semibold'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <MessageSquare className="w-4 h-4" />
            <span>Scanner</span>
          </button>

          <button
            onClick={() => setActiveTab('image')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all ${
              activeTab === 'image'
                ? 'bg-emerald-500 text-slate-950 shadow font-semibold'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <Image className="w-4 h-4" />
            <span>Screenshot</span>
          </button>

          <button
            onClick={() => setActiveTab('upi')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all ${
              activeTab === 'upi'
                ? 'bg-emerald-500 text-slate-950 shadow font-semibold'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <CreditCard className="w-4 h-4" />
            <span>UPI Intent</span>
          </button>

          <button
            onClick={() => setActiveTab('how-it-works')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all ${
              activeTab === 'how-it-works'
                ? 'bg-emerald-500 text-slate-950 shadow font-semibold'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <Info className="w-4 h-4" />
            <span>How It Works</span>
          </button>
        </nav>

        {/* API Status Indicator */}
        <div className="flex items-center gap-2 text-xs">
          <span
            className={`w-2 h-2 rounded-full ${
              apiConnected ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'
            }`}
          />
          <span className="text-slate-400 font-mono">
            API: {apiConnected ? 'Online' : 'Connecting...'}
          </span>
        </div>

      </div>
    </header>
  );
};
