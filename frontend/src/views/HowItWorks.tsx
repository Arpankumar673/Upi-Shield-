import React from 'react';
import { Shield, Cpu, Lock, FileText, CheckCircle2, AlertTriangle, Layers, Zap, Languages } from 'lucide-react';

const SIGNALS_INFO = [
  {
    name: '1. Urgency / Time Pressure',
    weight: 'Weight: 20',
    color: 'border-amber-500/40 bg-amber-500/5',
    iconColor: 'text-amber-400',
    desc: 'Detects artificial deadlines, immediate disconnection threats (e.g. 9:30 PM), or fake account blocking timers designed to cause panic.',
  },
  {
    name: '2. Threat / Fear / Consequences',
    weight: 'Weight: 25',
    color: 'border-rose-500/40 bg-rose-500/5',
    iconColor: 'text-rose-400',
    desc: 'Detects coercive threats such as power cutoff, account suspension, police complaint, or legal action.',
  },
  {
    name: '3. Authority Impersonation',
    weight: 'Weight: 20',
    color: 'border-purple-500/40 bg-purple-500/5',
    iconColor: 'text-purple-400',
    desc: 'Identifies fake claims of representing Electricity Boards, Banks, Telecom Operators, or Government Officials.',
  },
  {
    name: '4. Payment Pressure / Manipulation',
    weight: 'Weight: 25',
    color: 'border-emerald-500/40 bg-emerald-500/5',
    iconColor: 'text-emerald-400',
    desc: 'Detects requests for money transfers, bill updates via personal numbers, or fake refund processing fees.',
  },
  {
    name: '5. Credential / Security Request',
    weight: 'Weight: 30',
    color: 'border-cyan-500/40 bg-cyan-500/5',
    iconColor: 'text-cyan-400',
    desc: 'Flags requests for UPI PIN, 6-digit OTP, passwords, or downloading remote access software (e.g. AnyDesk).',
  },
  {
    name: '6. Reward / Refund / Cashback',
    weight: 'Weight: 20',
    color: 'border-blue-500/40 bg-blue-500/5',
    iconColor: 'text-blue-400',
    desc: 'Detects lottery wins, pending refunds, scratch card rewards, or fake cashback claims requiring user interaction.',
  },
];

export default function HowItWorks() {
  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Intro Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
          <Shield className="w-3.5 h-3.5" /> Explainable Deception Detection Architecture
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
          How UPI-Shield Prevents Financial Coercion & Fraud
        </h1>
        <p className="text-sm text-slate-400 max-w-2xl mx-auto leading-relaxed">
          UPI-Shield does not rely on simple keyword lists or blacklists. Instead, it extracts structured entities and evaluates 6 core psychological deception signals to compute an explainable threat score.
        </p>
      </div>

      {/* Architecture Pipeline Visual */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/90 p-6 space-y-6 shadow-xl">
        <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
          <Layers className="w-5 h-5 text-emerald-400" />
          <h2 className="text-base font-bold text-slate-200">5-Stage Security Pipeline</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-3 relative">
          <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 space-y-2">
            <div className="w-7 h-7 rounded-full bg-slate-800 text-slate-300 font-bold text-xs flex items-center justify-center">
              1
            </div>
            <h3 className="text-xs font-bold text-slate-200">Input Layer</h3>
            <p className="text-[11px] text-slate-400 leading-normal">
              Accepts raw SMS text, screenshot images (Tesseract OCR), or UPI intent URIs (`upi://pay`).
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 space-y-2">
            <div className="w-7 h-7 rounded-full bg-slate-800 text-slate-300 font-bold text-xs flex items-center justify-center">
              2
            </div>
            <h3 className="text-xs font-bold text-slate-200">Preprocessing</h3>
            <p className="text-[11px] text-slate-400 leading-normal">
              Normalizes text, strips noise, and extracts URLs, phone numbers, UPI VPAs, and monetary amounts.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 space-y-2">
            <div className="w-7 h-7 rounded-full bg-emerald-500/20 text-emerald-400 font-bold text-xs flex items-center justify-center border border-emerald-500/40">
              3
            </div>
            <h3 className="text-xs font-bold text-emerald-400">Signal Detection</h3>
            <p className="text-[11px] text-slate-400 leading-normal">
              Evaluates 6 independent deception signal detectors to calculate signal confidence scores (0.0 to 1.0).
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 space-y-2">
            <div className="w-7 h-7 rounded-full bg-slate-800 text-slate-300 font-bold text-xs flex items-center justify-center">
              4
            </div>
            <h3 className="text-xs font-bold text-slate-200">Risk Engine</h3>
            <p className="text-[11px] text-slate-400 leading-normal">
              Applies risk weights, non-linear multi-signal boosts, and maps to bounded levels (LOW, MEDIUM, HIGH, CRITICAL).
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 space-y-2">
            <div className="w-7 h-7 rounded-full bg-slate-800 text-slate-300 font-bold text-xs flex items-center justify-center">
              5
            </div>
            <h3 className="text-xs font-bold text-slate-200">Bilingual Guidance</h3>
            <p className="text-[11px] text-slate-400 leading-normal">
              Generates clear English & Hindi safety instructions tailored to the triggered deception vectors.
            </p>
          </div>
        </div>
      </div>

      {/* 6 Deception Categories Grid */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <Zap className="w-5 h-5 text-emerald-400" />
          <h2 className="text-lg font-bold text-slate-200">The 6 Core Deception Categories</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {SIGNALS_INFO.map((sig, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-xl border ${sig.color} space-y-2 transition duration-150 hover:border-slate-600`}
            >
              <div className="flex items-center justify-between">
                <h3 className={`text-xs font-bold ${sig.iconColor}`}>{sig.name}</h3>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                  {sig.weight}
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">{sig.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Thresholds & Safety Philosophy */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="rounded-xl border border-slate-800 bg-slate-900/90 p-5 space-y-3">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4.5 h-4.5 text-amber-400" />
            <h3 className="text-sm font-bold text-slate-200">Bounded Risk Level Thresholds</h3>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            The risk score is calculated on a strict 0–100 scale with continuous, fully verified boundaries:
          </p>
          <ul className="space-y-2 text-xs font-mono">
            <li className="flex justify-between p-2 rounded bg-slate-950 border border-slate-800">
              <span className="text-emerald-400 font-bold">0 – 30 Score</span>
              <span className="text-slate-300">LOW Risk (Safe / Legitimate)</span>
            </li>
            <li className="flex justify-between p-2 rounded bg-slate-950 border border-slate-800">
              <span className="text-amber-400 font-bold">&gt;30 – 60 Score</span>
              <span className="text-slate-300">MEDIUM Risk (Caution Advised)</span>
            </li>
            <li className="flex justify-between p-2 rounded bg-slate-950 border border-slate-800">
              <span className="text-orange-400 font-bold">&gt;60 – 80 Score</span>
              <span className="text-slate-300">HIGH Risk (High Threat Detected)</span>
            </li>
            <li className="flex justify-between p-2 rounded bg-slate-950 border border-slate-800">
              <span className="text-rose-400 font-bold">&gt;80 – 100 Score</span>
              <span className="text-slate-300">CRITICAL Risk (Severe Coercion / Theft)</span>
            </li>
          </ul>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/90 p-5 space-y-3">
          <div className="flex items-center gap-2">
            <Languages className="w-4.5 h-4.5 text-emerald-400" />
            <h3 className="text-sm font-bold text-slate-200">Bilingual Safety Guidance</h3>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Every scan produces immediate action items in both English and Hindi. This ensures accessibility across diverse demographics in India:
          </p>
          <div className="space-y-2 text-xs">
            <div className="p-2.5 rounded bg-slate-950 border border-slate-800 text-slate-300">
              <span className="font-bold text-emerald-400">English:</span> "NEVER enter your 6-digit UPI PIN to receive money. UPI PIN is strictly for DEBITING funds."
            </div>
            <div className="p-2.5 rounded bg-slate-950 border border-slate-800 text-slate-300">
              <span className="font-bold text-emerald-400">हिंदी (Hindi):</span> "पैसे प्राप्त करने के लिए कभी भी UPI PIN न दर्ज करें। PIN केवल आपके खाते से पैसे कटने के लिए होता है।"
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
