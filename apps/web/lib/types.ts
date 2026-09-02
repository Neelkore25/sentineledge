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
  severity_band: string;
  r_rule: number;
  s_behavior: number;
  c_correlation: number;
  a_criticality: number;
  b_impact: number;
  weights: Record<string, number>;
  weighted_contributions: {
    rule: number;
    behavior: number;
    correlation: number;
    criticality: number;
    impact: number;
  };
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

export interface SystemOverview {
  system_status: 'HEALTHY' | 'ALERT';
  last_event_seconds_ago: number;
  open_incidents_count: number;
  total_incidents_count: number;
  organization_risk_score: number;
  organization_risk_band: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  recovery_readiness_score: number;
  incident_pressure: {
    LOW: number;
    MEDIUM: number;
    HIGH: number;
    CRITICAL: number;
  };
  risk_trend: Array<{ time: string; score: number }>;
}

export interface Scenario {
  id: string;
  key: string;
  name: string;
  category: string;
  description: string;
  event_count: number;
  target_asset: string;
  target_user?: string | null;
}

export interface RecoveryInventoryItem {
  id: string;
  asset_id: string;
  asset_name: string;
  last_backup: string;
  backup_type: string;
  backup_status: string;
  verified: boolean;
  retention_days: number;
  rto_target_hours: number;
  rto_actual_hours: number;
  rpo_target_hours: number;
  rpo_actual_hours: number;
  last_test_date: string;
  test_result: string;
  readiness: {
    readiness_index: number;
    b_freshness: number;
    v_verified: number;
    t_recency: number;
    r_compliance: number;
    rpo_gap_hours: number;
    primary_weakness: string;
    weaknesses: string[];
  };
}

export interface AuditLogItem {
  id: string;
  timestamp: string;
  actor: string;
  role: string;
  action: string;
  resource: string;
  before_state?: any;
  after_state?: any;
  reason: string;
}
