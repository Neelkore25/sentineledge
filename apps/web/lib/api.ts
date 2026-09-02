const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

async function fetcher<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
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
      const errorText = await res.text();
      throw new Error(`API Error ${res.status} on ${endpoint}: ${errorText}`);
    }
    return await res.json();
  } catch (err: any) {
    console.error(`Failed to fetch ${url}:`, err);
    throw err;
  }
}

export const api = {
  getOverviewStats: () => fetcher<any>('/stats/overview'),
  getEvents: (params?: { skip?: number; limit?: number; event_type?: string; user_id?: string }) => {
    const query = new URLSearchParams(params as any).toString();
    return fetcher<{ total: number; skip: number; limit: number; items: any[] }>(`/telemetry?${query}`);
  },
  getEventById: (id: string) => fetcher<any>(`/telemetry/${id}`),
  getIncidents: (params?: { status?: string; severity?: string; search?: string }) => {
    const query = new URLSearchParams(params as any).toString();
    return fetcher<any[]>(`/incidents?${query}`);
  },
  getIncidentById: (id: string) => fetcher<{ incident: any; related_events: any[] }>(`/incidents/${id}`),
  updateIncidentStatus: (id: string, status: string, reason: string) =>
    fetcher<any>(`/incidents/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status, reason })
    }),
  respondToIncident: (id: string, action_type: string, reason: string, target?: string) =>
    fetcher<any>(`/incidents/${id}/respond`, {
      method: 'POST',
      body: JSON.stringify({ action_type, reason, target })
    }),
  getScenarios: () => fetcher<any[]>('/simulation/scenarios'),
  runScenario: (scenario_key: string) =>
    fetcher<any>('/simulation/run', {
      method: 'POST',
      body: JSON.stringify({ scenario_key })
    }),
  getRules: () => fetcher<any[]>('/detections/rules'),
  toggleRule: (rule_id: string, enabled: boolean) =>
    fetcher<any>(`/detections/rules/${rule_id}`, {
      method: 'PATCH',
      body: JSON.stringify({ enabled })
    }),
  getUserBaselines: () => fetcher<any[]>('/behavior/users'),
  getRecoveryInventory: () => fetcher<{ overall_readiness_score: number; items: any[] }>('/recovery/inventory'),
  investigateIncidentAI: (incident_id: string) =>
    fetcher<any>('/ai/investigate', {
      method: 'POST',
      body: JSON.stringify({ incident_id })
    }),
  getAuditLogs: () => fetcher<any[]>('/audit?limit=50'),
  getSettings: () => fetcher<Record<string, { value: string; description: string; updated_at: string }>>('/settings'),
  updateSetting: (key: string, value: string) =>
    fetcher<any>(`/settings/${key}`, {
      method: 'PUT',
      body: JSON.stringify({ value })
    })
};
