import React from 'react';
import { AnalysisResponse } from '../types';
import { ShieldAlert, AlertTriangle, CheckCircle2, Link2, CreditCard, Phone, IndianRupee, HelpCircle, ShieldCheck, Info } from 'lucide-react';

interface ThreatDashboardProps {
  data: AnalysisResponse;
}

const CATEGORY_LABEL_MAP: Record<string, string> = {
  urgency: 'Urgent pressure',
  threat: 'Threat or fear',
  authority_impersonation: 'Impersonation',
  payment_pressure: 'Payment request',
  credential_request: 'OTP or PIN request',
  reward_manipulation: 'Fake refund or reward',
};

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

  // Determine Colors & Styling based on Risk Level
  const getBadgeStyle = () => {
    switch (risk_level) {
      case 'LOW':
        return {
          bg: 'bg-emerald-50 border-emerald-200 text-emerald-700',
          bannerBg: 'bg-emerald-50/90 border-emerald-200 text-emerald-900',
          gaugeColor: '#10b981',
          label: 'LOW RISK',
          bannerMessage: 'This message does not show strong scam signs.',
        };
      case 'MEDIUM':
        return {
          bg: 'bg-amber-50 border-amber-200 text-amber-700',
          bannerBg: 'bg-amber-50/90 border-amber-200 text-amber-900',
          gaugeColor: '#f59e0b',
          label: 'MEDIUM RISK',
          bannerMessage: '⚠️ Caution Advised — This message shows suspicious payment or verification requests.',
        };
      case 'HIGH':
        return {
          bg: 'bg-orange-50 border-orange-200 text-orange-700',
          bannerBg: 'bg-rose-50 border-rose-200 text-rose-900',
          gaugeColor: '#f97316',
          label: 'HIGH RISK',
          bannerMessage: '⚠️ This message looks risky — Do not pay, click links, or share your OTP/PIN until you verify the request.',
        };
      case 'CRITICAL':
      default:
        return {
          bg: 'bg-red-50 border-red-200 text-red-700',
          bannerBg: 'bg-red-50 border-red-200 text-red-900',
          gaugeColor: '#ef4444',
          label: 'CRITICAL THREAT',
          bannerMessage: '⚠️ Critical Scam Risk — Do not pay, click links, or share your OTP/PIN under any circumstances.',
        };
    }
  };

  const style = getBadgeStyle();

  return (
    <div className="space-y-6 animate-fadeIn mt-6">
      
      {/* Risk Warning Banner */}
      <div className={`p-4.5 rounded-2xl border ${style.bannerBg} flex items-start gap-3 shadow-sm`}>
        <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5 text-amber-600" />
        <div>
          <h3 className="font-bold text-sm leading-snug">{style.bannerMessage}</h3>
          <p className="text-xs opacity-90 mt-0.5">
            Always double-check payment requests directly with the official company or recipient.
          </p>
        </div>
      </div>

      {/* Grid Layout: Threat Meter & Why this looks risky */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        
        {/* Score Radial / Meter Card (5 cols) */}
        <div className="md:col-span-5 bg-white border border-slate-200 rounded-2xl p-6 flex flex-col items-center justify-center text-center shadow-sm">
          <div className="text-xs font-semibold text-slate-500 tracking-wider uppercase mb-3">
            Threat Meter Score
          </div>

          {/* SVG Radial Gauge */}
          <div className="relative w-44 h-44 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="40"
                stroke="#E2E8F0"
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
              <span className="text-4xl font-extrabold text-slate-900 tracking-tight">{score}</span>
              <span className="text-xs font-medium text-slate-500">/ 100</span>
            </div>
          </div>

          {/* Risk Level Badge */}
          <div className={`mt-4 px-4 py-1.5 rounded-full border text-xs font-extrabold tracking-wide ${style.bg}`}>
            {style.label}
          </div>

          {/* Extracted Context Entities */}
          {extracted_context && (
            <div className="mt-5 w-full pt-4 border-t border-slate-100 text-left space-y-2 text-xs text-slate-600">
              <div className="font-semibold text-slate-800 mb-1">Details Found in Message:</div>
              {extracted_context.has_urls && (
                <div className="flex items-center gap-1.5 text-blue-600 truncate">
                  <Link2 className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate">{extracted_context.extracted_urls.join(', ')}</span>
                </div>
              )}
              {extracted_context.has_upi_ids && (
                <div className="flex items-center gap-1.5 text-purple-600 truncate">
                  <CreditCard className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate">{extracted_context.extracted_upi_ids.join(', ')}</span>
                </div>
              )}
              {extracted_context.has_phones && (
                <div className="flex items-center gap-1.5 text-emerald-600 truncate">
                  <Phone className="w-3.5 h-3.5 shrink-0" />
                  <span>{extracted_context.extracted_phones.join(', ')}</span>
                </div>
              )}
              {extracted_context.has_amounts && (
                <div className="flex items-center gap-1.5 text-amber-600 truncate">
                  <IndianRupee className="w-3.5 h-3.5 shrink-0" />
                  <span>{extracted_context.extracted_amounts.join(', ')}</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Why this looks risky & Evidence Card (7 cols) */}
        <div className="md:col-span-7 bg-white border border-slate-200 rounded-2xl p-6 flex flex-col justify-between space-y-4 shadow-sm">
          <div>
            <div className="flex items-center gap-2 text-base font-bold text-slate-900 mb-2">
              <HelpCircle className="w-5 h-5 text-blue-600" />
              Why this looks risky
            </div>
            <p className="text-xs sm:text-sm text-slate-700 font-medium leading-relaxed bg-blue-50/50 p-3.5 rounded-xl border border-blue-100 mb-4">
              {explanation_summary}
            </p>

            <ul className="space-y-2 text-xs sm:text-sm text-slate-700">
              {reasons.map((r, idx) => (
                <li key={idx} className="flex items-start gap-2 bg-slate-50 p-2.5 rounded-xl border border-slate-200/80">
                  <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                  <span>{r}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Matched Evidence Snippets */}
          {evidence && evidence.length > 0 && (
            <div className="pt-4 border-t border-slate-100">
              <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                Matched Words & Evidence
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {evidence.map((ev, idx) => (
                  <span
                    key={idx}
                    className="text-xs px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 text-slate-700 font-medium"
                  >
                    {ev}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>

      {/* Warning Signs Found */}
      <div>
        <h3 className="text-base font-bold text-slate-900 mb-3 flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-blue-600" />
          Warning Signs Found
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {signals.map((sig) => {
            const friendlyName = CATEGORY_LABEL_MAP[sig.name] || sig.display_name;
            return (
              <div
                key={sig.name}
                className={`p-4 rounded-xl border transition-all ${
                  sig.detected
                    ? 'bg-amber-50/40 border-amber-200 shadow-sm'
                    : 'bg-white border-slate-200 opacity-60'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                    {sig.detected ? (
                      <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                    ) : (
                      <CheckCircle2 className="w-4 h-4 text-slate-400 shrink-0" />
                    )}
                    {friendlyName}
                  </span>
                  <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full ${
                    sig.detected ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-500'
                  }`}>
                    {sig.detected ? 'Found' : 'Clear'}
                  </span>
                </div>

                {/* Progress Confidence Bar */}
                <div className="w-full bg-slate-200 rounded-full h-2 mb-2 overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-700 ${
                      sig.detected ? 'bg-amber-500' : 'bg-slate-300'
                    }`}
                    style={{ width: `${Math.round(sig.score * 100)}%` }}
                  />
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-500 font-medium">
                  <span>Match Strength: {Math.round(sig.score * 100)}%</span>
                  <span>+{data.indicators[sig.name] || 0} pts</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Bilingual Safety Guidance Cards */}
      <div className="space-y-3">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-blue-600" />
          Safety Advice / सुरक्षा मार्गदर्शन
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          
          {/* English Safety Guidance Card */}
          <div className="bg-blue-50/60 border border-blue-200/80 rounded-2xl p-5 space-y-3 shadow-sm">
            <div className="flex items-center gap-2 text-blue-900 font-bold text-sm border-b border-blue-200/60 pb-2">
              <span>🇬🇧 English Safety Advice</span>
            </div>
            <p className="text-xs sm:text-sm text-blue-950 font-semibold bg-white p-3 rounded-xl border border-blue-200/60 leading-relaxed">
              {recommendation_en}
            </p>
            {action_bullets_en && action_bullets_en.length > 0 && (
              <div className="space-y-1.5 text-xs text-slate-700">
                <div className="font-bold text-slate-900">What you should do:</div>
                <ul className="list-disc list-inside space-y-1">
                  {action_bullets_en.map((b, idx) => (
                    <li key={idx} className="leading-relaxed">{b}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Hindi Safety Guidance Card */}
          <div className="bg-amber-50/60 border border-amber-200/80 rounded-2xl p-5 space-y-3 shadow-sm">
            <div className="flex items-center gap-2 text-amber-900 font-bold text-sm border-b border-amber-200/60 pb-2">
              <span>🇮🇳 हिंदी सुरक्षा सुझाव</span>
            </div>
            <p className="text-xs sm:text-sm text-amber-950 font-semibold bg-white p-3 rounded-xl border border-amber-200/60 leading-relaxed">
              {recommendation_hi}
            </p>
            {action_bullets_hi && action_bullets_hi.length > 0 && (
              <div className="space-y-1.5 text-xs text-slate-700">
                <div className="font-bold text-slate-900">सुझाई गई कार्रवाइयां:</div>
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
