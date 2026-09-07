import React, { useState, useRef } from 'react';
import { Upload, FileImage, AlertCircle, Loader2, FileText, CheckCircle2, X } from 'lucide-react';
import { analyzeImage } from '../api';
import { ImageAnalysisResponse } from '../types';
import { ThreatDashboard } from '../components/ThreatDashboard';

export default function ScreenshotScanner() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ImageAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (file: File | null) => {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      setError('Please select a valid image file (PNG, JPG, JPEG, WEBP).');
      return;
    }

    setSelectedFile(file);
    setError(null);
    setResult(null);

    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select an image file first.');
      return;
    }

    setError(null);
    setLoading(true);
    try {
      const res = await analyzeImage(selectedFile);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to process screenshot OCR. Ensure backend is operational.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setImagePreview(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload Zone */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/90 p-5 shadow-lg space-y-4">
        <div>
          <h2 className="text-sm font-semibold text-slate-200 mb-1">
            Upload Scam SMS / Payment Screenshot
          </h2>
          <p className="text-xs text-slate-400">
            Upload an image of a suspicious message or UPI payment notification for OCR extraction and threat analysis.
          </p>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={(e) => handleFileChange(e.target.files ? e.target.files[0] : null)}
          className="hidden"
          id="screenshot-file-input"
        />

        {!imagePreview ? (
          <div
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-slate-700 hover:border-emerald-500/60 rounded-xl p-8 text-center cursor-pointer transition duration-150 bg-slate-950/50 hover:bg-slate-900/50 group"
          >
            <div className="mx-auto w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 group-hover:text-emerald-400 group-hover:scale-110 transition duration-150 mb-3">
              <Upload className="w-6 h-6" />
            </div>
            <p className="text-sm font-medium text-slate-300 group-hover:text-slate-100">
              Click to upload or drag & drop image here
            </p>
            <p className="text-xs text-slate-500 mt-1">PNG, JPG, JPEG, WEBP (Max 10MB)</p>
          </div>
        ) : (
          <div className="relative rounded-lg overflow-hidden border border-slate-800 bg-slate-950 p-4 flex flex-col sm:flex-row items-center gap-4">
            <img
              src={imagePreview}
              alt="Screenshot Preview"
              className="max-h-48 rounded object-contain border border-slate-800 bg-black/40"
            />
            <div className="flex-1 space-y-2 text-left w-full">
              <div className="flex items-center gap-2">
                <FileImage className="w-4 h-4 text-emerald-400" />
                <span className="text-sm font-semibold text-slate-200 truncate">
                  {selectedFile?.name}
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Size: {selectedFile ? (selectedFile.size / 1024).toFixed(1) : 0} KB
              </p>
              <button
                type="button"
                onClick={handleClear}
                className="text-xs text-rose-400 hover:text-rose-300 flex items-center gap-1 pt-1"
              >
                <X className="w-3.5 h-3.5" /> Remove image
              </button>
            </div>
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {imagePreview && (
          <div className="flex justify-end pt-1">
            <button
              type="button"
              onClick={handleAnalyze}
              disabled={loading}
              className="flex items-center gap-2 px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-sm rounded-lg shadow-md hover:shadow-emerald-500/20 transition duration-150 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Extracting OCR & Analyzing...
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4" />
                  Run OCR & Threat Scan
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* OCR Text Output & Results */}
      {result && (
        <div className="space-y-6">
          {/* Extracted Text Box */}
          <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-4 space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-emerald-400" />
                <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Extracted OCR Text
                </h3>
              </div>
              <span
                className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                  result.ocr_success
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                    : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                }`}
              >
                {result.ocr_success ? 'OCR Engine: Active' : 'OCR Engine: Unavailable / Fallback'}
              </span>
            </div>

            <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-300 font-mono whitespace-pre-wrap">
              {result.extracted_text || 'No text extracted from image.'}
            </div>

            {result.ocr_error && (
              <p className="text-[11px] text-[amber-400] italic">Note: {result.ocr_error}</p>
            )}
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
