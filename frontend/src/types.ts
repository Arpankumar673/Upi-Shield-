export interface SignalDetail {
  name: string;
  display_name: string;
  score: number;
  detected: boolean;
  evidence: string[];
  reasons: string[];
}

export interface ExtractedContext {
  char_count: number;
  word_count: number;
  has_urls: boolean;
  extracted_urls: string[];
  has_upi_ids: boolean;
  extracted_upi_ids: string[];
  has_phones: boolean;
  extracted_phones: string[];
  has_amounts: boolean;
  extracted_amounts: string[];
  is_truncated: boolean;
}

export interface AnalysisResponse {
  score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  triggered_signals: string[];
  indicators: Record<string, number>;
  signals: SignalDetail[];
  explanation_summary: string;
  reasons: string[];
  evidence: string[];
  recommendation_en: string;
  recommendation_hi: string;
  action_bullets_en: string[];
  action_bullets_hi: string[];
  extracted_context: ExtractedContext;
}

export interface UPIAnalysisResponse {
  is_valid: boolean;
  payee_vpa?: string;
  payee_name?: string;
  amount?: string;
  currency?: string;
  transaction_note?: string;
  raw_uri: string;
  errors: string[];
  risk_analysis?: AnalysisResponse;
}

export interface ImageAnalysisResponse {
  ocr_success: boolean;
  extracted_text: string;
  ocr_error?: string;
  risk_analysis?: AnalysisResponse;
  process_time_ms?: number;
}
