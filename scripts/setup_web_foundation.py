import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 1. tsconfig.json
write_file("apps/web/tsconfig.json", """{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
""")

# 2. next.config.js
write_file("apps/web/next.config.mjs", """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL 
          ? `${process.env.NEXT_PUBLIC_API_URL}/:path*`
          : 'http://127.0.0.1:8000/api/v1/:path*'
      }
    ];
  }
};

export default nextConfig;
""")

# 3. postcss.config.js
write_file("apps/web/postcss.config.js", """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
""")

# 4. tailwind.config.js
write_file("apps/web/tailwind.config.js", """/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        editorial: {
          bg: 'var(--bg-primary)',
          surface: 'var(--bg-surface)',
          panel: 'var(--bg-panel)',
          border: 'var(--border-color)',
          text: 'var(--text-primary)',
          muted: 'var(--text-muted)',
          accent: 'var(--accent-signal)',
          accentMuted: 'var(--accent-muted)',
        },
        status: {
          healthy: '#10B981',
          warning: '#F59E0B',
          critical: '#EF4444',
          info: '#3B82F6',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'IBM Plex Mono', 'monospace'],
      }
    },
  },
  plugins: [],
};
""")

# 5. globals.css
write_file("apps/web/app/globals.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --bg-primary: #F9F9FB;
    --bg-surface: #FFFFFF;
    --bg-panel: #F2F3F6;
    --border-color: #E2E4E8;
    --text-primary: #121316;
    --text-muted: #6B7280;
    --accent-signal: #E86A25;
    --accent-muted: #FDF2E9;
  }

  .dark {
    --bg-primary: #0D0E11;
    --bg-surface: #14161B;
    --bg-panel: #1A1D24;
    --border-color: #22252D;
    --text-primary: #F3F4F6;
    --text-muted: #9CA3AF;
    --accent-signal: #F59E0B;
    --accent-muted: #261B0E;
  }
}

body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* Subtle millimeter grid background pattern */
.grid-bg-light {
  background-image: radial-gradient(rgba(0, 0, 0, 0.05) 1px, transparent 1px);
  background-size: 24px 24px;
}

.grid-bg-dark {
  background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 24px 24px;
}

/* Custom scrollbars */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}
""")

# 6. TypeScript definitions (apps/web/lib/types.ts)
write_file("apps/web/lib/types.ts", """export interface SecurityEvent {
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
""")

# 7. API Client (apps/web/lib/api.ts)
write_file("apps/web/lib/api.ts", """const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

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
""")

print("Phase 3 Next.js foundation, types, and API client created!")
