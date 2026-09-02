export interface SecurityEvent {
  id: string;
  timestamp: string;
  source: string;
  user_id?: string | null;
  asset_id?: string | null;
  source_ip?: string | null;
  event_type: string;
  action?: string | null;
  status: string;
  endpoint?: string | null;
  device_id?: string | null;
  location?: string | null;
  bytes_transferred: number;
  event_metadata: Record<string, any>;
}

export interface RiskBreakdown {
  composite_risk_score: number;
  severity_band: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  r_rule: number;
  s_behavior: number;
  c_correlation: number;
  a_criticality: number;
  b_impact: number;
  weights: Record<string, number>;
  weighted_contributions: Record<string, number>;
  formula: string;
  model_version: string;
}

export interface Incident {
  id: string;
  title: string;
  description: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  risk_score: number;
  status: 'OPEN' | 'INVESTIGATING' | 'MITIGATED' | 'RESOLVED' | 'FALSE_POSITIVE';
  detected_at: string;
  first_seen: string;
  last_seen: string;
  affected_asset: string;
  affected_user?: string | null;
  attack_category: string;
  business_impact: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  confidence: number;
  correlation_group: string;
  event_ids: string[];
  risk_breakdown: RiskBreakdown;
  ai_summary?: string | null;
  ai_hypothesis?: string | null;
  ai_alternative?: string | null;
  ai_missing_evidence?: string | null;
  recommended_action?: string | null;
  created_at: string;
  updated_at: string;
}
