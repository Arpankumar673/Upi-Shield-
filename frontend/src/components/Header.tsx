import React from 'react';
import { Shield, MessageSquare, Image, CreditCard, Info } from 'lucide-react';

interface HeaderProps {
  activeTab: 'text' | 'image' | 'upi' | 'how-it-works';
  setActiveTab: (tab: 'text' | 'image' | 'upi' | 'how-it-works') => void;
  apiConnected: boolean;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab, apiConnected }) => {
  return (
    <header className="border-b border-slate-200/80 bg-white/95 backdrop-blur sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Brand Logo & Subtitle */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('text')}>
          <div className="p-2.5 bg-blue-600 rounded-xl text-white shadow-md shadow-blue-500/20">
            <Shield className="w-6 h-6 font-bold" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-extrabold tracking-tight text-slate-900">UPI-Shield</h1>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200/70 font-bold tracking-wide">
                CC-GFG-02
              </span>
            </div>
            <p className="text-xs text-slate-500 font-medium">Stay Alert. Stay Safe.</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1 bg-slate-100/80 p-1.5 rounded-xl border border-slate-200/80 text-sm font-medium">
          <button
            onClick={() => setActiveTab('text')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all ${
              activeTab === 'text'
                ? 'bg-blue-600 text-white shadow font-semibold'
                : 'text-slate-600 hover:text-blue-700 hover:bg-white'
            }`}
          >
            <MessageSquare className="w-4 h-4" />
            <span>Scanner</span>
          </button>

          <button
            onClick={() => setActiveTab('image')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all ${
              activeTab === 'image'
                ? 'bg-blue-600 text-white shadow font-semibold'
                : 'text-slate-600 hover:text-blue-700 hover:bg-white'
            }`}
          >
            <Image className="w-4 h-4" />
            <span>Screenshot</span>
          </button>

          <button
            onClick={() => setActiveTab('upi')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all ${
              activeTab === 'upi'
                ? 'bg-blue-600 text-white shadow font-semibold'
                : 'text-slate-600 hover:text-blue-700 hover:bg-white'
            }`}
          >
            <CreditCard className="w-4 h-4" />
            <span>UPI Link</span>
          </button>

          <button
            onClick={() => setActiveTab('how-it-works')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all ${
              activeTab === 'how-it-works'
                ? 'bg-blue-600 text-white shadow font-semibold'
                : 'text-slate-600 hover:text-blue-700 hover:bg-white'
            }`}
          >
            <Info className="w-4 h-4" />
            <span>How It Works</span>
          </button>
        </nav>

        {/* API Status Indicator */}
        <div className="flex items-center gap-2 text-xs bg-slate-50 px-3 py-1.5 rounded-full border border-slate-200">
          <span
            className={`w-2 h-2 rounded-full ${
              apiConnected ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'
            }`}
          />
          <span className="text-slate-600 font-medium">
            {apiConnected ? 'API Online' : 'Connecting...'}
          </span>
        </div>

      </div>
    </header>
  );
};
