import React from 'react';
import { AnalysisResponse } from '../types';
import { ShieldAlert, AlertOctagon, CheckCircle2, Link2, CreditCard, Phone, IndianRupee, HelpCircle, ShieldCheck } from 'lucide-react';

interface ThreatDashboardProps {
  data: AnalysisResponse;
}

export const ThreatDashboard: React.FC<ThreatDashboardProps> = ({ data }) => {
  const {
    score,
    risk_level,
    signals,
    explanation_summary,
    reasons,
    evidence,
    recommendation_en,
    recommendation_hi,
    action_bullets_en,
    action_bullets_hi,
    extracted_context,
  } = data;

  // Determine Badge Color & Gradient based on Risk Level
  const getBadgeStyle = () => {
    switch (risk_level) {
      case 'LOW':
        return {
          bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
          gaugeColor: '#10b981',
          label: 'LOW RISK',
        };
      case 'MEDIUM':
        return {
          bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
          gaugeColor: '#f59e0b',
          label: 'MEDIUM RISK',
        };
      case 'HIGH':
        return {
          bg: 'bg-orange-500/10 border-orange-500/30 text-orange-400',
          gaugeColor: '#f97316',
          label: 'HIGH RISK',
        };
      case 'CRITICAL':
      default:
        return {
          bg: 'bg-red-500/10 border-red-500/30 text-red-400',
          gaugeColor: '#ef4444',
          label: 'CRITICAL THREAT',
        };
    }
  };

  const style = getBadgeStyle();
  const detectedSignals = signals.filter((s) => s.detected);

  return (
    <div className="space-y-8 animate-fadeIn mt-6">
      {/* Header Section */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <ShieldAlert className="w-6 h-6 text-emerald-400" />
          Threat Assessment Dashboard
        </h2>
        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${style.bg}`}>
          {style.label} ({score}/100)
        </span>
      </div>

      {/* Grid Layout: Score Meter & Why Flagged */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        
        {/* Score Radial / Gauge Card (4 cols) */}
        <div className="md:col-span-5 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 flex flex-col items-center justify-center text-center relative overflow-hidden shadow-xl">
          <div className="text-xs font-semibold text-slate-400 tracking-wider uppercase mb-4">
            Threat Meter Score
          </div>

          {/* SVG Radial Gauge */}
          <div className="relative w-44 h-44 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="40"
                stroke="#1e293b"
                strokeWidth="8"
                fill="transparent"
              />
              <circle
                cx="50"
                cy="50"
                r="40"
                stroke={style.gaugeColor}
                strokeWidth="8"
                strokeDasharray={251.2}
                strokeDashoffset={251.2 - (251.2 * score) / 100}
                strokeLinecap="round"
                fill="transparent"
                className="transition-all duration-1000 ease-out"
              />
            </svg>
            <div className="absolute flex flex-col items-center">
              <span className="text-4xl font-extrabold text-white tracking-tight">{score}</span>
              <span className="text-xs font-medium text-slate-400">/ 100</span>
            </div>
          </div>

          {/* Risk Level Badge */}
          <div className={`mt-4 px-4 py-1.5 rounded-xl border text-sm font-extrabold ${style.bg}`}>
            {risk_level}
          </div>

          {/* Extracted Context Entities */}
          {extracted_context && (
            <div className="mt-6 w-full pt-4 border-t border-slate-800/80 text-left space-y-2 text-xs text-slate-400">
              <div className="font-semibold text-slate-300 mb-2">Context Entities Extracted:</div>
              {extracted_context.has_urls && (
                <div className="flex items-center gap-1.5 text-sky-400 truncate">
                  <Link2 className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate">{extracted_context.extracted_urls.join(', ')}</span>
                </div>
              )}
              {extracted_context.has_upi_ids && (
                <div className="flex items-center gap-1.5 text-purple-400 truncate">
                  <CreditCard className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate">{extracted_context.extracted_upi_ids.join(', ')}</span>
                </div>
              )}
              {extracted_context.has_phones && (
                <div className="flex items-center gap-1.5 text-emerald-400 truncate">
                  <Phone className="w-3.5 h-3.5 shrink-0" />
                  <span>{extracted_context.extracted_phones.join(', ')}</span>
                </div>
              )}
              {extracted_context.has_amounts && (
                <div className="flex items-center gap-1.5 text-amber-400 truncate">
                  <IndianRupee className="w-3.5 h-3.5 shrink-0" />
                  <span>{extracted_context.extracted_amounts.join(', ')}</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Why Flagged & Evidence Card (7 cols) */}
        <div className="md:col-span-7 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between space-y-4 shadow-xl">
          <div>
            <div className="flex items-center gap-2 text-lg font-bold text-white mb-2">
              <HelpCircle className="w-5 h-5 text-emerald-400" />
              Why was this flagged?
            </div>
            <p className="text-sm text-slate-300 font-medium leading-relaxed bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80 mb-4">
              {explanation_summary}
            </p>

            <ul className="space-y-2 text-xs sm:text-sm text-slate-300">
              {reasons.map((r, idx) => (
                <li key={idx} className="flex items-start gap-2 bg-slate-950/40 p-2.5 rounded-lg border border-slate-800/50">
                  <AlertOctagon className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                  <span>{r}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Matched Evidence Snippets */}
          {evidence && evidence.length > 0 && (
            <div className="pt-4 border-t border-slate-800">
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Matched Evidence Snippets
              </h4>
              <div className="flex flex-wrap gap-2">
                {evidence.map((ev, idx) => (
                  <span
                    key={idx}
                    className="text-xs px-2.5 py-1 rounded-md bg-slate-950 border border-slate-700 text-slate-300 font-mono"
                  >
                    {ev}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>

      {/* Deception Indicator Breakdown Cards */}
      <div>
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-emerald-400" />
          Deception Indicators Breakdown
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {signals.map((sig) => (
            <div
              key={sig.name}
              className={`p-4 rounded-xl border transition-all ${
                sig.detected
                  ? 'bg-slate-900 border-amber-500/40 shadow-lg shadow-amber-500/5'
                  : 'bg-slate-900/40 border-slate-800/60 opacity-70'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-white flex items-center gap-1.5">
                  {sig.detected ? (
                    <AlertOctagon className="w-4 h-4 text-amber-400 shrink-0" />
                  ) : (
                    <CheckCircle2 className="w-4 h-4 text-slate-600 shrink-0" />
                  )}
                  {sig.display_name}
                </span>
                <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                  sig.detected ? 'bg-amber-500/20 text-amber-300' : 'bg-slate-800 text-slate-400'
                }`}>
                  {sig.detected ? 'Detected' : 'Clear'}
                </span>
              </div>

              {/* Progress Confidence Bar */}
              <div className="w-full bg-slate-950 rounded-full h-2 mb-2 overflow-hidden border border-slate-800">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    sig.detected ? 'bg-amber-500' : 'bg-slate-700'
                  }`}
                  style={{ width: `${Math.round(sig.score * 100)}%` }}
                />
              </div>

              <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>Confidence: {Math.round(sig.score * 100)}%</span>
                <span>Impact: +{data.indicators[sig.name] || 0} pts</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Bilingual Safety Guidance Cards */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          Bilingual Safety Guidance / सुरक्षा मार्गदर्शन
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* English Safety Guidance Card */}
          <div className="bg-slate-900 border border-sky-500/30 rounded-2xl p-6 space-y-4 shadow-xl">
            <div className="flex items-center gap-2 text-sky-400 font-bold text-base border-b border-slate-800 pb-2">
              <span>🇬🇧 English Safety Advice</span>
            </div>
            <p className="text-sm text-sky-100 font-semibold bg-sky-950/40 p-3 rounded-xl border border-sky-500/20 leading-relaxed">
              {recommendation_en}
            </p>
            {action_bullets_en && action_bullets_en.length > 0 && (
              <div className="space-y-2 text-xs text-slate-300">
                <div className="font-semibold text-slate-200">Recommended Actions:</div>
                <ul className="list-disc list-inside space-y-1">
                  {action_bullets_en.map((b, idx) => (
                    <li key={idx} className="leading-relaxed">{b}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Hindi Safety Guidance Card */}
          <div className="bg-slate-900 border border-amber-500/30 rounded-2xl p-6 space-y-4 shadow-xl">
            <div className="flex items-center gap-2 text-amber-400 font-bold text-base border-b border-slate-800 pb-2">
              <span>🇮🇳 हिंदी सुरक्षा सुझाव</span>
            </div>
            <p className="text-sm text-amber-100 font-semibold bg-amber-950/40 p-3 rounded-xl border border-amber-500/20 leading-relaxed">
              {recommendation_hi}
            </p>
            {action_bullets_hi && action_bullets_hi.length > 0 && (
              <div className="space-y-2 text-xs text-slate-300">
                <div className="font-semibold text-slate-200">सुझाई गई कार्रवाइयां:</div>
                <ul className="list-disc list-inside space-y-1">
                  {action_bullets_hi.map((b, idx) => (
                    <li key={idx} className="leading-relaxed">{b}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

        </div>
      </div>

    </div>
  );
};
