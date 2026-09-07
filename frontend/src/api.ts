import { AnalysisResponse, UPIAnalysisResponse, ImageAnalysisResponse } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function analyzeText(text: string): Promise<AnalysisResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/analyze/text`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: 'API Request failed' }));
      throw new Error(errorData.detail || 'Failed to analyze text.');
    }

    return await res.json();
  } catch (err: any) {
    if (err.name === 'TypeError' && err.message?.includes('fetch')) {
      throw new Error('Cannot reach backend server. The Render backend may be waking up from a cold start (takes ~30s). Please wait a moment and try again.');
    }
    throw err;
  }
}

export async function analyzeUPI(uri: string): Promise<UPIAnalysisResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/analyze/upi`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ uri }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: 'UPI API Request failed' }));
      throw new Error(errorData.detail || 'Failed to analyze UPI URI.');
    }

    return await res.json();
  } catch (err: any) {
    if (err.name === 'TypeError' && err.message?.includes('fetch')) {
      throw new Error('Cannot reach backend server. The Render backend may be waking up from a cold start (takes ~30s). Please wait a moment and try again.');
    }
    throw err;
  }
}

export async function analyzeImage(file: File): Promise<ImageAnalysisResponse> {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch(`${API_BASE_URL}/api/analyze/image`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: 'OCR API Request failed' }));
      throw new Error(errorData.detail || 'Failed to process screenshot.');
    }

    return await res.json();
  } catch (err: any) {
    if (err.name === 'TypeError' && err.message?.includes('fetch')) {
      throw new Error('Cannot reach backend server. The Render backend may be waking up from a cold start (takes ~30s). Please wait a moment and try again.');
    }
    throw err;
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/health`);
    return res.ok;
  } catch {
    return false;
  }
}
