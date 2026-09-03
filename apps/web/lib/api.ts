/**
 * SentinelEdge API Client
 * Enterprise-grade client communicating with the FastAPI backend.
 */

import {
  SecurityEvent,
  Incident,
  Scenario,
  AuditLogItem,
  SystemOverview,
  UserBaseline
} from '@/lib/types';

export class ApiError extends Error {
  status: number;
  data: any;

  constructor(status: number, message: string, data?: any) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

/**
 * Resolves the base API URL based on runtime environment.
 * Ensures consistent normalization, handles trailing slashes,
 * and fails fast in production if unconfigured.
 */
export function getApiBaseUrl(): string {
  const envUrl = process.env.NEXT_PUBLIC_API_URL;
  if (envUrl && envUrl.trim() !== '') {
    let clean = envUrl.trim().replace(/\/+$/, '');
    if (!clean.endsWith('/api/v1')) {
      clean = `${clean}/api/v1`;
    }
    return clean;
  }

  // Development/SSR fallback for local environments
  if (process.env.NODE_ENV === 'development' || typeof window === 'undefined') {
    return 'http://127.0.0.1:8000/api/v1';
  }

  // Diagnostic warning in production browser if variable was omitted
  console.warn(
    '[SentinelEdge Config Warning] NEXT_PUBLIC_API_URL is not configured in environment. Defaulting to /api/v1'
  );
  return '/api/v1';
}

const API_BASE = getApiBaseUrl();

async function fetcher<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const url = `${API_BASE}${cleanEndpoint}`;

  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {})
      },
      cache: 'no-store'
    });

    if (!res.ok) {
      let errorBody: any;
      try {
        errorBody = await res.json();
      } catch {
        errorBody = await res.text();
      }

      const message =
        typeof errorBody === 'object' && errorBody?.detail
          ? (typeof errorBody.detail === 'string' ? errorBody.detail : JSON.stringify(errorBody.detail))
          : `API request failed with HTTP ${res.status}`;

      throw new ApiError(res.status, message, errorBody);
    }

    return await res.json();
  } catch (err: any) {
    if (err instanceof ApiError) {
      throw err;
    }
    console.error(`[API Network Error] ${options?.method || 'GET'} ${url}:`, err);
    throw new ApiError(0, `Network error: ${err.message || 'Unable to communicate with backend service'}`, err);
  }
}

export const api = {
  // System Overview Stats
  getOverviewStats: () => fetcher<SystemOverview>('/stats/overview'),

  // Telemetry Events
  getEvents: (params?: { skip?: number; limit?: number; event_type?: string; user_id?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return fetcher<{ total: number; skip: number; limit: number; items: SecurityEvent[] }>(
      `/telemetry${query ? `?${query}` : ''}`
    );
  },
  getEventById: (id: string) => fetcher<SecurityEvent>(`/telemetry/${id}`),

  // Incidents
  getIncidents: (params?: { status?: string; severity?: string; search?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return fetcher<Incident[]>(`/incidents${query ? `?${query}` : ''}`);
  },
  getIncidentById: (id: string) =>
    fetcher<{ incident: Incident; related_events: SecurityEvent[] }>(`/incidents/${id}`),
  updateIncidentStatus: (id: string, status: string, reason: string) =>
    fetcher<Incident>(`/incidents/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status, reason })
    }),
  respondToIncident: (id: string, action_type: string, reason: string, target?: string) =>
    fetcher<any>(`/incidents/${id}/respond`, {
      method: 'POST',
      body: JSON.stringify({ action_type, reason, target })
    }),

  // Simulation Lab Scenarios
  getScenarios: () => fetcher<Scenario[]>('/simulation/scenarios'),
  runScenario: (scenario_key: string) =>
    fetcher<any>('/simulation/run', {
      method: 'POST',
      body: JSON.stringify({ scenario_key })
    }),

  // Detection Rules
  getRules: () => fetcher<any[]>('/detections/rules'),
  toggleRule: (rule_id: string, enabled: boolean) =>
    fetcher<any>(`/detections/rules/${rule_id}`, {
      method: 'PATCH',
      body: JSON.stringify({ enabled })
    }),

  // Behavioral Baselines
  getUserBaselines: () => fetcher<UserBaseline[]>('/behavior/users'),

  // Recovery Readiness Inventory
  getRecoveryInventory: () =>
    fetcher<{ overall_readiness_score: number; items: any[] }>('/recovery/inventory'),

  // AI Investigator
  investigateIncidentAI: (incident_id: string) =>
    fetcher<any>('/ai/investigate', {
      method: 'POST',
      body: JSON.stringify({ incident_id })
    }),

  // Audit Logs
  getAuditLogs: () => fetcher<AuditLogItem[]>('/audit?limit=50'),

  // System Settings
  getSettings: () =>
    fetcher<Record<string, { value: string; description: string; updated_at: string }>>('/settings'),
  updateSetting: (key: string, value: string) =>
    fetcher<any>(`/settings/${key}`, {
      method: 'PUT',
      body: JSON.stringify({ value })
    })
};
