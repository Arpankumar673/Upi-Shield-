import React from 'react';
import { Shield, Lock, AlertTriangle, Layers, Zap, Languages, CheckCircle2, Search, ArrowRight } from 'lucide-react';

const SIGNALS_INFO = [
  {
    name: '1. Urgent Pressure',
    weight: 'Weight: 20',
    color: 'border-amber-200 bg-amber-50/40 text-amber-900',
    badgeStyle: 'bg-amber-100 text-amber-800',
    desc: 'Detects artificial deadlines, immediate disconnection threats (e.g. 9:30 PM cutoff), or fake account blocking timers designed to cause panic.',
  },
  {
    name: '2. Threat or Fear',
    weight: 'Weight: 25',
    color: 'border-rose-200 bg-rose-50/40 text-rose-900',
    badgeStyle: 'bg-rose-100 text-rose-800',
    desc: 'Detects coercive threats such as power cutoff, account suspension, legal action, or police complaints.',
  },
  {
    name: '3. Impersonation',
    weight: 'Weight: 20',
    color: 'border-purple-200 bg-purple-50/40 text-purple-900',
    badgeStyle: 'bg-purple-100 text-purple-800',
    desc: 'Identifies fake claims of representing Electricity Boards, Banks, Telecom Operators, or Government Officials.',
  },
  {
    name: '4. Payment Request',
    weight: 'Weight: 25',
    color: 'border-blue-200 bg-blue-50/40 text-blue-900',
    badgeStyle: 'bg-blue-100 text-blue-800',
    desc: 'Detects requests for money transfers, bill updates via personal phone numbers, or fake refund processing fees.',
  },
  {
    name: '5. OTP / Credential Request',
    weight: 'Weight: 30',
    color: 'border-cyan-200 bg-cyan-50/40 text-cyan-900',
    badgeStyle: 'bg-cyan-100 text-cyan-800',
    desc: 'Flags requests for UPI PIN, 6-digit OTP, passwords, or downloading remote access apps (e.g. AnyDesk).',
  },
  {
    name: '6. Fake Refund or Reward',
    weight: 'Weight: 20',
    color: 'border-emerald-200 bg-emerald-50/40 text-emerald-900',
    badgeStyle: 'bg-emerald-100 text-emerald-800',
    desc: 'Detects lottery wins, pending refunds, scratch card rewards, or fake cashback claims requiring user interaction.',
  },
];

export default function HowItWorks() {
  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header Banner */}
      <div className="text-center space-y-3 bg-gradient-to-r from-blue-50 via-indigo-50/40 to-white rounded-3xl p-6 sm:p-8 border border-blue-100 shadow-sm">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-100/70 border border-blue-200 text-blue-800 text-xs font-bold">
          <Shield className="w-3.5 h-3.5 text-blue-600" /> Explainable Fraud Prevention Architecture
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          How UPI-Shield Keeps You Safe
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 max-w-2xl mx-auto leading-relaxed font-medium">
          UPI-Shield does not rely on simple keyword lists or blacklists. Instead, it extracts context and evaluates 6 core psychological scam indicators to compute a continuous 0–100 threat score.
        </p>
      </div>

      {/* 5-Step Pipeline Visual */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 space-y-5 shadow-sm">
        <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
          <Layers className="w-5 h-5 text-blue-600" />
          <h2 className="text-base font-bold text-slate-900">5-Step Analysis Pipeline</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-3 relative">
          <div className="p-4 rounded-xl bg-blue-50/50 border border-blue-100 space-y-2">
            <div className="w-7 h-7 rounded-full bg-blue-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
              1
            </div>
            <h3 className="text-xs font-bold text-slate-900">Paste or Upload</h3>
            <p className="text-[11px] text-slate-600 leading-normal">
              Accepts raw SMS text, screenshot images (OCR), or UPI links (`upi://pay`).
            </p>
          </div>

          <div className="p-4 rounded-xl bg-blue-50/50 border border-blue-100 space-y-2">
            <div className="w-7 h-7 rounded-full bg-blue-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
              2
            </div>
            <h3 className="text-xs font-bold text-slate-900">Find Warning Signs</h3>
            <p className="text-[11px] text-slate-600 leading-normal">
              Scans for urgency, coercive threats, fake rewards, and credential requests.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-blue-600 text-white space-y-2 shadow-md">
            <div className="w-7 h-7 rounded-full bg-white text-blue-600 font-bold text-xs flex items-center justify-center shadow-xs">
              3
            </div>
            <h3 className="text-xs font-bold text-white">Calculate Risk</h3>
            <p className="text-[11px] opacity-90 leading-normal">
              Applies signal weights and multi-signal boosts to compute a 0–100 score.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-blue-50/50 border border-blue-100 space-y-2">
            <div className="w-7 h-7 rounded-full bg-blue-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
              4
            </div>
            <h3 className="text-xs font-bold text-slate-900">Explain Result</h3>
            <p className="text-[11px] text-slate-600 leading-normal">
              Explains why the message was flagged in simple language with matched evidence.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-blue-50/50 border border-blue-100 space-y-2">
            <div className="w-7 h-7 rounded-full bg-blue-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
              5
            </div>
            <h3 className="text-xs font-bold text-slate-900">Give Safety Advice</h3>
            <p className="text-[11px] text-slate-600 leading-normal">
              Provides actionable English & Hindi safety guidance to protect the user.
            </p>
          </div>
        </div>
      </div>

      {/* The 6 Core Scam Categories Grid */}
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <Zap className="w-5 h-5 text-blue-600" />
          <h2 className="text-base font-bold text-slate-900">The 6 Core Deception Categories</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {SIGNALS_INFO.map((sig, idx) => (
            <div
              key={idx}
              className={`p-4.5 rounded-2xl border ${sig.color} space-y-2 transition duration-150 shadow-xs hover:shadow-md`}
            >
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-bold text-slate-900">{sig.name}</h3>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${sig.badgeStyle}`}>
                  {sig.weight}
                </span>
              </div>
              <p className="text-xs text-slate-700 leading-relaxed font-medium">{sig.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Thresholds & Safety Philosophy */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 space-y-3 shadow-sm">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4.5 h-4.5 text-amber-500" />
            <h3 className="text-sm font-bold text-slate-900">Risk Score Levels</h3>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed font-medium">
            The threat score is calculated on a 0–100 scale with continuous boundaries:
          </p>
          <ul className="space-y-2 text-xs">
            <li className="flex justify-between p-2.5 rounded-xl bg-emerald-50 border border-emerald-200">
              <span className="text-emerald-800 font-bold">0 – 30 Score</span>
              <span className="text-slate-700 font-medium">LOW Risk (Safe / Normal)</span>
            </li>
            <li className="flex justify-between p-2.5 rounded-xl bg-amber-50 border border-amber-200">
              <span className="text-amber-800 font-bold">&gt;30 – 60 Score</span>
              <span className="text-slate-700 font-medium">MEDIUM Risk (Caution Advised)</span>
            </li>
            <li className="flex justify-between p-2.5 rounded-xl bg-orange-50 border border-orange-200">
              <span className="text-orange-800 font-bold">&gt;60 – 80 Score</span>
              <span className="text-slate-700 font-medium">HIGH Risk (High Threat Found)</span>
            </li>
            <li className="flex justify-between p-2.5 rounded-xl bg-rose-50 border border-rose-200">
              <span className="text-rose-800 font-bold">&gt;80 – 100 Score</span>
              <span className="text-slate-700 font-medium">CRITICAL Risk (Severe Scam Request)</span>
            </li>
          </ul>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 space-y-3 shadow-sm">
          <div className="flex items-center gap-2">
            <Languages className="w-4.5 h-4.5 text-blue-600" />
            <h3 className="text-sm font-bold text-slate-900">Bilingual Safety Guidance</h3>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed font-medium">
            Every analysis produces safety instructions in both English and Hindi for maximum accessibility:
          </p>
          <div className="space-y-2 text-xs">
            <div className="p-3 rounded-xl bg-blue-50/80 border border-blue-200 text-slate-800">
              <span className="font-bold text-blue-700">English:</span> "NEVER enter your 6-digit UPI PIN to receive money. UPI PIN is strictly for DEBITING funds."
            </div>
            <div className="p-3 rounded-xl bg-amber-50/80 border border-amber-200 text-slate-800">
              <span className="font-bold text-amber-800">हिंदी (Hindi):</span> "पैसे प्राप्त करने के लिए कभी भी UPI PIN न दर्ज करें। PIN केवल आपके खाते से पैसे कटने के लिए होता है।"
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}
