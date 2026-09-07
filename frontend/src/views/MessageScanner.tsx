import React, { useState } from 'react';
import { Send, Trash2, AlertCircle, Sparkles, Loader2 } from 'lucide-react';
import { analyzeText } from '../api';
import { AnalysisResponse } from '../types';
import { ThreatDashboard } from '../components/ThreatDashboard';

const SAMPLE_MESSAGES = [
  {
    label: 'Verification & Refund Scam',
    badge: 'CC-GFG-02 Demo',
    text: 'URGENT: Your refund of ₹4,999 is pending verification. Your UPI account will be suspended if you don\'t complete verification immediately. Click the link below and enter your OTP to receive the refund. http://upi-verify-refund.top',
  },
  {
    label: 'Electricity Bill Urgency Scam',
    badge: 'High Threat',
    text: 'DEAR CUSTOMER YOUR ELECTRICITY POWER WILL BE DISCONNECTED NIGHT 9.30 PM FROM ELECTRICITY OFFICE BECAUSE YOUR PREVIOUS MONTH BILL WAS NOT UPDATED PLEASE IMMEDIATELY CONTACT OUR ELECTRICITY OFFICER AT 9876543210. THANK YOU.',
  },
  {
    label: 'Account Suspended & OTP Scam',
    badge: 'Credential Theft',
    text: 'Your UPI account will be blocked within 2 hours due to unverified KYC. Share your 6-digit OTP with our agent to prevent suspension immediately.',
  },
  {
    label: 'Legitimate Payment Alert',
    badge: 'Safe Demo',
    text: 'Paid Rs. 450 to Swiggy via Google Pay UPI (Ref: 409823178923) on 07/09/2026. Account XX9123 debited.',
  },
];

export default function MessageScanner() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (textToAnalyze?: string) => {
    const text = textToAnalyze !== undefined ? textToAnalyze : message;
    if (!text.trim()) {
      setError('Please enter a message or choose a sample scenario below.');
      return;
    }

    setError(null);
    setLoading(true);
    try {
      const res = await analyzeText(text);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to analyze message. Ensure the FastAPI backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessage('');
    setResult(null);
    setError(null);
  };

  const handleSampleClick = (sampleText: string) => {
    setMessage(sampleText);
    handleAnalyze(sampleText);
  };

  return (
    <div className="space-y-6">
      {/* Sample Scenario Selector */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 backdrop-blur">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles className="w-4 h-4 text-emerald-400" />
          <h2 className="text-sm font-semibold text-slate-200">Quick Test Scenarios (Preset Demos)</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
          {SAMPLE_MESSAGES.map((sample, idx) => (
            <button
              key={idx}
              onClick={() => handleSampleClick(sample.text)}
              disabled={loading}
              className="flex flex-col text-left p-3 rounded-lg bg-slate-800/80 hover:bg-slate-750 border border-slate-700/60 hover:border-slate-500 transition duration-150 group disabled:opacity-50"
            >
              <div className="flex items-center justify-between w-full mb-1">
                <span className="text-xs font-semibold text-slate-200 group-hover:text-emerald-400 transition-colors">
                  {sample.label}
                </span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-700 text-slate-300 font-mono">
                  {sample.badge}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
                {sample.text}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Input Box */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/90 p-5 shadow-lg space-y-4">
        <div>
          <label htmlFor="message-input" className="block text-sm font-semibold text-slate-200 mb-2">
            Paste Suspicious Message / SMS / WhatsApp Text
          </label>
          <textarea
            id="message-input"
            rows={4}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="e.g. URGENT: Your refund of ₹4,999 is pending verification. Click link to complete..."
            className="w-full rounded-lg bg-slate-950 border border-slate-800 p-3.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition duration-150"
          />
        </div>

        {error && (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <div className="flex items-center justify-between pt-1">
          <button
            type="button"
            onClick={handleClear}
            disabled={loading || (!message && !result)}
            className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800 transition duration-150 disabled:opacity-40"
          >
            <Trash2 className="w-3.5 h-3.5" />
            Clear
          </button>

          <button
            type="button"
            onClick={() => handleAnalyze()}
            disabled={loading || !message.trim()}
            className="flex items-center gap-2 px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-sm rounded-lg shadow-md hover:shadow-emerald-500/20 transition duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Analyzing Deception Signals...
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                Analyze Threat Level
              </>
            )}
          </button>
        </div>
      </div>

      {/* Results Dashboard */}
      {result && <ThreatDashboard data={result} />}
    </div>
  );
}
