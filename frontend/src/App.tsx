import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import MessageScanner from './views/MessageScanner';
import ScreenshotScanner from './views/ScreenshotScanner';
import UPIAnalyzer from './views/UPIAnalyzer';
import HowItWorks from './views/HowItWorks';
import { checkHealth } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState<'text' | 'image' | 'upi' | 'how-it-works'>('text');
  const [apiConnected, setApiConnected] = useState<boolean>(true);

  useEffect(() => {
    const verifyHealth = async () => {
      const isOk = await checkHealth();
      setApiConnected(isOk);
    };

    verifyHealth();
    const interval = setInterval(verifyHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col selection:bg-emerald-500 selection:text-slate-950">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} apiConnected={apiConnected} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'text' && <MessageScanner />}
        {activeTab === 'image' && <ScreenshotScanner />}
        {activeTab === 'upi' && <UPIAnalyzer />}
        {activeTab === 'how-it-works' && <HowItWorks />}
      </main>

      <Footer />
    </div>
  );
}
