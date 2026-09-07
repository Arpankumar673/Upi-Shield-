import React from 'react';
import { ShieldCheck, Lock, AlertCircle } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-200/80 bg-white py-8 mt-16 text-slate-600 text-xs shadow-inner">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-b border-slate-100 pb-6">
          <div className="flex items-center gap-2 text-slate-800 font-semibold">
            <ShieldCheck className="w-4 h-4 text-blue-600" />
            <span>UPI-Shield | CC-GFG-02</span>
            <span className="text-slate-400 font-normal hidden sm:inline">• Contextual Digital Payment Scam & Coercion Detector</span>
          </div>
          <div className="flex items-center gap-2 text-blue-700 bg-blue-50/80 px-3 py-1 rounded-full border border-blue-100 text-[11px] font-medium">
            <Lock className="w-3.5 h-3.5" />
            <span>In-Memory Processing • Zero Persistent Log Storage</span>
          </div>
        </div>

        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-slate-500">
          <p className="flex items-center gap-1.5 leading-relaxed max-w-3xl">
            <AlertCircle className="w-4 h-4 text-amber-500 shrink-0" />
            <span>
              <strong>Safety Disclaimer:</strong> UPI-Shield evaluates payment messages for psychological coercion and scam signals. It never asks for or processes real UPI PINs, bank passwords, or OTPs, and cannot initiate money transfers.
            </span>
          </p>
          <p className="shrink-0 font-semibold text-slate-700 text-[11px]">
            Built for a Safer Digital India
          </p>
        </div>
      </div>
    </footer>
  );
};
