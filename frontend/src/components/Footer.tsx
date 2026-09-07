import React from 'react';
import { ShieldCheck, Lock, AlertTriangle } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-800 bg-slate-950 py-8 mt-16 text-slate-400 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-b border-slate-800/60 pb-6">
          <div className="flex items-center gap-2 text-slate-300 font-medium">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>UPI-Shield Cyber Security Engine • CC-GFG-02</span>
          </div>
          <div className="flex items-center gap-2 text-slate-400">
            <Lock className="w-3.5 h-3.5 text-slate-500" />
            <span>In-Memory Local Processing • Zero Persistent Log Storage</span>
          </div>
        </div>

        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-slate-500">
          <p className="flex items-center gap-1.5 leading-relaxed max-w-3xl">
            <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0" />
            <span>
              <strong>Safety Disclaimer:</strong> UPI-Shield evaluates digital payment messages for psychological coercion, urgency, and social engineering triggers. It never asks for or processes real UPI PINs, bank passwords, or OTPs, and cannot initiate payments.
            </span>
          </p>
          <p className="shrink-0 font-mono text-[11px]">
            Career Catalyst Club × GeeksforGeeks
          </p>
        </div>
      </div>
    </footer>
  );
};
