import React, { useState } from 'react';
import { QrCode, Sparkles, Trash2, AlertCircle, Loader2, UserCheck, DollarSign, FileText } from 'lucide-react';
import { analyzeUPI } from '../api';
import { UPIAnalysisResponse } from '../types';
import { ThreatDashboard } from '../components/ThreatDashboard';

const SAMPLE_UPI_URIS = [
  {
    label: 'Suspicious Refund UPI Link',
    badge: 'Scam Intent',
    uri: 'upi://pay?pa=claim-refund-service@ybl&pn=UPI%20Refund%20Verification&am=4999.00&cu=INR&tn=Verification%20Fee%20Refund',
  },
  {
    label: 'Reward / Cashback Intent',
    badge: 'Reward Scam',
    uri: 'upi://pay?pa=cashback-bonus99@paytm&pn=GooglePay%20Reward&am=1500.00&cu=INR&tn=Click%20PIN%20to%20receive%20cashback',
  },
  {
    label: 'Legitimate Merchant Payment',
    badge: 'Safe Intent',
    uri: 'upi://pay?pa=swiggy@icici&pn=Swiggy%20Order&am=350.00&cu=INR&tr=SWG982371982&tn=Food%20Order%20Payment',
  },
];

export default function UPIAnalyzer() {
  const [upiUri, setUpiUri] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<UPIAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (uriToAnalyze?: string) => {
    const uri = uriToAnalyze !== undefined ? uriToAnalyze : upiUri;
    if (!uri.trim()) {
      setError('Please enter a UPI intent URI (e.g. upi://pay?pa=...) or select a sample.');
      return;
    }

    setError(null);
    setLoading(true);
    try {
      const res = await analyzeUPI(uri);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to parse UPI intent URI. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setUpiUri('');
    setResult(null);
    setError(null);
  };

  const handleSampleClick = (uri: string) => {
    setUpiUri(uri);
    handleAnalyze(uri);
  };

  return (
    <div className="space-y-6">
      {/* Sample Scenario Selector */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 backdrop-blur">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles className="w-4 h-4 text-emerald-400" />
          <h2 className="text-sm font-semibold text-slate-200">Sample UPI Intent URIs</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
          {SAMPLE_UPI_URIS.map((sample, idx) => (
            <button
              key={idx}
              onClick={() => handleSampleClick(sample.uri)}
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
              <p className="text-[11px] text-slate-400 font-mono truncate leading-relaxed">
                {sample.uri}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Input Box */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/90 p-5 shadow-lg space-y-4">
        <div>
          <label htmlFor="upi-input" className="block text-sm font-semibold text-slate-200 mb-2">
            Paste UPI Intent URI / QR Code Data (`upi://pay?...`)
          </label>
          <input
            id="upi-input"
            type="text"
            value={upiUri}
            onChange={(e) => setUpiUri(e.target.value)}
            placeholder="upi://pay?pa=payee@vpa&pn=PayeeName&am=1000.00&cu=INR..."
            className="w-full rounded-lg bg-slate-950 border border-slate-800 p-3.5 text-sm text-slate-100 font-mono placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition duration-150"
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
            disabled={loading || (!upiUri && !result)}
            className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800 transition duration-150 disabled:opacity-40"
          >
            <Trash2 className="w-3.5 h-3.5" />
            Clear
          </button>

          <button
            type="button"
            onClick={() => handleAnalyze()}
            disabled={loading || !upiUri.trim()}
            className="flex items-center gap-2 px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-sm rounded-lg shadow-md hover:shadow-emerald-500/20 transition duration-150 disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Parsing UPI Intent...
              </>
            ) : (
              <>
                <QrCode className="w-4 h-4" />
                Analyze UPI Intent
              </>
            )}
          </button>
        </div>
      </div>

      {/* Results Dashboard & Parsed UPI Parameters */}
      {result && (
        <div className="space-y-6">
          {/* Parsed UPI Intent Card */}
          <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-5 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <QrCode className="w-4.5 h-4.5 text-emerald-400" />
                <h3 className="text-sm font-semibold text-slate-200">
                  Parsed UPI Payment Parameters
                </h3>
              </div>
              <span
                className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                  result.is_valid
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                    : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                }`}
              >
                {result.is_valid ? 'Valid UPI Intent URI' : 'Invalid / Non-standard URI'}
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center gap-1.5 mb-1">
                  <UserCheck className="w-3.5 h-3.5 text-slate-400" /> Payee VPA (`pa`)
                </div>
                <div className="text-xs font-mono font-semibold text-slate-200 truncate">
                  {result.payee_vpa || 'N/A'}
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center gap-1.5 mb-1">
                  <UserCheck className="w-3.5 h-3.5 text-slate-400" /> Payee Name (`pn`)
                </div>
                <div className="text-xs font-semibold text-slate-200 truncate">
                  {result.payee_name || 'N/A'}
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center gap-1.5 mb-1">
                  <DollarSign className="w-3.5 h-3.5 text-slate-400" /> Requested Amount (`am`)
                </div>
                <div className="text-xs font-mono font-semibold text-emerald-400">
                  {result.amount ? `₹${result.amount}` : 'N/A'}
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center gap-1.5 mb-1">
                  <FileText className="w-3.5 h-3.5 text-slate-400" /> Transaction Note (`tn`)
                </div>
                <div className="text-xs text-slate-300 truncate">
                  {result.transaction_note || 'N/A'}
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center gap-1.5 mb-1">
                  <FileText className="w-3.5 h-3.5 text-slate-400" /> Currency (`cu`)
                </div>
                <div className="text-xs font-mono text-slate-300 truncate">
                  {result.currency || 'INR'}
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center gap-1.5 mb-1">
                  Raw URI
                </div>
                <div className="text-xs font-mono text-slate-400 truncate">
                  {result.raw_uri}
                </div>
              </div>
            </div>
          </div>

          {/* Threat Dashboard */}
          {result.risk_analysis && (
            <ThreatDashboard data={result.risk_analysis} />
          )}
        </div>
      )}
    </div>
  );
}
