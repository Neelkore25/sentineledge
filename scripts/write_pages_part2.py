import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 6. Events Explorer Page (apps/web/app/events/page.tsx)
write_file("apps/web/app/events/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import { Layers, Search, Filter, ArrowUpDown, Eye, Code, X } from 'lucide-react';
import { api } from '@/lib/api';
import { SecurityEvent } from '@/lib/types';
import { useApp } from '@/lib/store';

export default function EventsPage() {
  const { refreshTrigger } = useApp();
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [selectedEvent, setSelectedEvent] = useState<SecurityEvent | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const res = await api.getEvents({ limit: 50 });
        setEvents(res.items);
        setTotal(res.total);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [refreshTrigger]);

  const filtered = events.filter(e => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      e.id.toLowerCase().includes(q) ||
      e.event_type.toLowerCase().includes(q) ||
      (e.user_id && e.user_id.toLowerCase().includes(q)) ||
      (e.source_ip && e.source_ip.toLowerCase().includes(q)) ||
      (e.endpoint && e.endpoint.toLowerCase().includes(q))
    );
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-editorial-border pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Security Telemetry Explorer</h1>
          <p className="text-xs text-editorial-muted font-mono mt-0.5">
            Normalized raw and simulated telemetry streams ({total} indexed records)
          </p>
        </div>
      </div>

      <div className="p-3 rounded-lg border border-editorial-border bg-editorial-surface flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 flex-1">
          <Search className="w-4 h-4 text-editorial-muted" />
          <input
            type="text"
            placeholder="Search by event ID, IP, user, endpoint, or event type..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-transparent text-editorial-text focus:outline-none text-xs"
          />
        </div>
        <span className="text-[11px] font-mono text-editorial-muted">Showing {filtered.length} of {total} events</span>
      </div>

      <div className="border border-editorial-border rounded-lg bg-editorial-surface shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-editorial-panel/60 border-b border-editorial-border text-[10px] text-editorial-muted uppercase">
              <tr>
                <th className="p-3">EVENT ID</th>
                <th className="p-3">TIMESTAMP</th>
                <th className="p-3">SOURCE & TYPE</th>
                <th className="p-3">SOURCE IP / LOCATION</th>
                <th className="p-3">USER / IDENTITY</th>
                <th className="p-3">STATUS</th>
                <th className="p-3 text-right">PAYLOAD</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-editorial-border text-[11px]">
              {filtered.map(e => (
                <tr key={e.id} className="hover:bg-editorial-panel/40 transition-colors">
                  <td className="p-3 font-bold text-editorial-text">{e.id}</td>
                  <td className="p-3 text-editorial-muted">{e.timestamp.slice(11, 19)}</td>
                  <td className="p-3">
                    <span className="font-bold text-editorial-accent">{e.event_type}</span>
                    <div className="text-[10px] text-editorial-muted">{e.source}</div>
                  </td>
                  <td className="p-3">
                    <div>{e.source_ip || '—'}</div>
                    <div className="text-[10px] text-editorial-muted">{e.location || 'Internal'}</div>
                  </td>
                  <td className="p-3 text-editorial-text">{e.user_id || 'system'}</td>
                  <td className="p-3">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                      e.status === 'FAILURE' || e.status === 'BLOCKED' ? 'bg-status-critical/15 text-status-critical' :
                      e.status === 'ANOMALOUS' ? 'bg-status-warning/15 text-status-warning' :
                      'bg-status-healthy/15 text-status-healthy'
                    }`}>
                      {e.status}
                    </span>
                  </td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => setSelectedEvent(e)}
                      className="px-2 py-1 rounded bg-editorial-panel border border-editorial-border text-editorial-text hover:bg-editorial-panel/80"
                    >
                      <Code className="w-3.5 h-3.5 inline mr-1" /> JSON
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* JSON Modal */}
      {selectedEvent && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-2xl bg-editorial-surface border border-editorial-border rounded-lg shadow-2xl overflow-hidden animate-in fade-in">
            <div className="p-4 border-b border-editorial-border flex items-center justify-between">
              <span className="font-mono font-bold text-sm text-editorial-text">Event Payload: {selectedEvent.id}</span>
              <button onClick={() => setSelectedEvent(null)} className="p-1 text-editorial-muted hover:text-editorial-text">
                <X className="w-4 h-4" />
              </button>
            </div>
            <pre className="p-4 font-mono text-xs text-editorial-text bg-editorial-panel/50 overflow-x-auto max-h-96">
              {JSON.stringify(selectedEvent, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
""")

# 7. Attack Stories Page (apps/web/app/attack-stories/page.tsx)
write_file("apps/web/app/attack-stories/page.tsx", """'use client';

import React from 'react';
import Link from 'next/link';
import { GitCommit, ShieldAlert, ArrowDown, Play, ExternalLink } from 'lucide-react';

const attackStories = [
  {
    title: 'Too Many Doors (Credential Stuffing → Account Hijack)',
    category: 'Credential Access & Initial Access',
    target: 'Admin Identity & Auth Gateway',
    duration: '6 minutes',
    steps: [
      { time: '09:41:02', title: 'Repeated Authentication Failures', desc: '12 rapid failed login attempts from Romanian IP 194.26.29.114 targeting user finance_admin.', type: 'AUTH_BURST' },
      { time: '09:43:18', title: 'Successful Session Authentication', desc: 'Valid credential accepted on Admin Portal without MFA challenge from same external IP.', type: 'INITIAL_ACCESS' },
      { time: '09:44:05', title: 'Administrative User Query', desc: 'Accessed administrative endpoint /api/v1/admin/users and queried all corporate accounts.', type: 'RECON' },
      { time: '09:45:30', title: 'Correlated Incident Triggered', desc: 'SentinelEdge detection engine correlated burst into Incident #INC-1042 (Risk 82/100, CRITICAL).', type: 'ALERT' }
    ]
  },
  {
    title: 'The Privilege Jump (Intern Role Elevation)',
    category: 'Privilege Escalation',
    target: 'Internal IAM / Active Directory',
    duration: '2 minutes',
    steps: [
      { time: '14:10:11', title: 'IAM Roles Enumeration', desc: 'Junior engineer account dev_intern queried administrative role definitions.', type: 'RECON' },
      { time: '14:11:45', title: 'Unauthorized Super-Admin Role Assigned', desc: 'Direct privilege assignment to SuperAdministrator role without associated IT change ticket.', type: 'PRIV_ESC' },
      { time: '14:12:00', title: 'Deterministic Rule Triggered', desc: 'RULE_PRIV_ESCALATION_003 flagged unauthorized privilege mutation.', type: 'ALERT' }
    ]
  },
  {
    title: 'The Large Download (Data Exfiltration Spike)',
    category: 'Exfiltration',
    target: 'Customer Financial Database',
    duration: '4 minutes',
    steps: [
      { time: '03:15:00', title: 'Off-Hours Database SQL Dump', desc: 'Full database export executed against customer financial records (450,000 rows).', type: 'COLLECTION' },
      { time: '03:17:22', title: 'High-Volume Network Egress', desc: 'Outbound transfer of 2.8 GB compressed archive to external file hosting endpoint.', type: 'EXFIL' },
      { time: '03:18:00', title: 'Robust Z-Score MAD Deviation Spike', desc: 'Behavioral engine flagged 62x deviation over rolling daily baseline (45 MB).', type: 'ANOMALY' }
    ]
  }
];

export function AttackStoriesPage() {
  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Attack Storyboards</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Progressive vertical timeline representations of multi-stage security compromise scenarios
        </p>
      </div>

      <div className="space-y-8">
        {attackStories.map((story, idx) => (
          <div key={idx} className="border border-editorial-border rounded-xl bg-editorial-surface p-6 shadow-xs space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-editorial-border pb-4">
              <div>
                <span className="text-[10px] font-mono uppercase text-editorial-accent font-semibold">{story.category}</span>
                <h3 className="font-bold text-lg text-editorial-text mt-0.5">{story.title}</h3>
                <div className="text-xs text-editorial-muted font-mono mt-1">Target Asset: {story.target} | Span: {story.duration}</div>
              </div>
              <Link
                href="/simulation"
                className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded bg-editorial-panel border border-editorial-border text-xs font-semibold text-editorial-text hover:bg-editorial-panel/80 transition-colors"
              >
                <Play className="w-3.5 h-3.5 text-editorial-accent" /> Run Scenario
              </Link>
            </div>

            {/* Vertical Progressive Timeline */}
            <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-editorial-border">
              {story.steps.map((step, stepIdx) => (
                <div key={stepIdx} className="relative group">
                  <div className="absolute -left-6 top-1 w-5 h-5 rounded-full bg-editorial-surface border-2 border-editorial-accent flex items-center justify-center text-[10px] font-mono text-editorial-accent">
                    {stepIdx + 1}
                  </div>
                  <div className="p-3.5 rounded bg-editorial-panel/70 border border-editorial-border space-y-1">
                    <div className="flex items-center justify-between font-mono text-[11px]">
                      <span className="font-bold text-editorial-text">{step.title}</span>
                      <span className="text-editorial-muted">{step.time}</span>
                    </div>
                    <p className="text-xs text-editorial-muted">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AttackStoriesPage;
""")

# 8. Simulation Lab Page (apps/web/app/simulation/page.tsx)
write_file("apps/web/app/simulation/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  FlaskConical,
  Play,
  Layers,
  Sparkles,
  ArrowRight,
  ShieldAlert,
  RotateCcw,
  CheckCircle2
} from 'lucide-react';
import { api } from '@/lib/api';
import { Scenario } from '@/lib/types';
import { useApp } from '@/lib/store';

export default function SimulationLabPage() {
  const router = useRouter();
  const { triggerRefresh } = useApp();
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [runningKey, setRunningKey] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getScenarios();
        setScenarios(data);
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, []);

  const handleRun = async (key: string) => {
    try {
      setRunningKey(key);
      setResult(null);
      const res = await api.runScenario(key);
      setResult(res);
      triggerRefresh();
    } catch (err) {
      alert(`Simulation run failed: ${err}`);
    } finally {
      setRunningKey(null);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div className="border-b border-editorial-border pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Simulation Lab</h1>
          <p className="text-xs text-editorial-muted font-mono mt-0.5">
            Safely generate synthetic telemetry streams to evaluate multi-layer detection, AI investigation, and recovery readiness
          </p>
        </div>
        <span className="text-xs font-mono text-editorial-accent bg-editorial-panel px-3 py-1 rounded border border-editorial-border">
          ZERO-RISK SYNTHETIC ENVIRONMENT
        </span>
      </div>

      {/* Result Callout Banner */}
      {result && (
        <div className="p-5 rounded-xl border border-editorial-accent bg-editorial-surface shadow-md space-y-4 animate-in fade-in">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-status-healthy" />
              <h3 className="font-bold text-sm text-editorial-text">
                Simulation Completed: {result.scenario_name}
              </h3>
            </div>
            <span className={`font-mono text-xs px-2 py-0.5 rounded font-bold uppercase ${
              result.severity === 'CRITICAL' ? 'bg-status-critical/15 text-status-critical' :
              result.severity === 'HIGH' ? 'bg-status-warning/15 text-status-warning' :
              'bg-status-info/15 text-status-info'
            }`}>
              {result.severity} ({result.risk_score}/100)
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
            <div className="p-2.5 rounded bg-editorial-panel border border-editorial-border">
              <span className="text-[10px] text-editorial-muted">EVENTS GENERATED</span>
              <div className="text-base font-bold text-editorial-text mt-0.5">{result.events_generated}</div>
            </div>
            <div className="p-2.5 rounded bg-editorial-panel border border-editorial-border">
              <span className="text-[10px] text-editorial-muted">RULES TRIGGERED</span>
              <div className="text-base font-bold text-editorial-text mt-0.5">{result.rule_matches.length}</div>
            </div>
            <div className="p-2.5 rounded bg-editorial-panel border border-editorial-border">
              <span className="text-[10px] text-editorial-muted">INCIDENT ID</span>
              <div className="text-base font-bold text-editorial-accent mt-0.5">#{result.incident_id}</div>
            </div>
            <div className="p-2.5 rounded bg-editorial-panel border border-editorial-border">
              <span className="text-[10px] text-editorial-muted">CORRELATION</span>
              <div className="text-base font-bold text-status-healthy mt-0.5">COMPLETE</div>
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <button
              onClick={() => router.push(`/incidents/${result.incident_id}`)}
              className="flex items-center gap-2 px-4 py-2 rounded bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity"
            >
              Open Incident Investigation <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Scenarios Grid */}
      <div className="grid md:grid-cols-2 gap-5">
        {scenarios.map(scen => {
          const isRunning = runningKey === scen.key;
          return (
            <div
              key={scen.id}
              className="border border-editorial-border rounded-xl bg-editorial-surface p-5 shadow-xs flex flex-col justify-between space-y-4 hover:border-editorial-accent transition-all"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-[10px] uppercase text-editorial-accent font-semibold">{scen.category}</span>
                  <span className="font-mono text-[10px] text-editorial-muted bg-editorial-panel px-1.5 py-0.5 rounded border border-editorial-border">
                    {scen.event_count} EVENTS
                  </span>
                </div>
                <h3 className="font-bold text-base text-editorial-text">{scen.name}</h3>
                <p className="text-xs text-editorial-muted leading-relaxed">{scen.description}</p>
                <div className="text-[11px] font-mono text-editorial-muted pt-1">
                  Target: <strong>{scen.target_asset}</strong> {scen.target_user ? `(User: ${scen.target_user})` : ''}
                </div>
              </div>

              <div className="pt-2 border-t border-editorial-border flex items-center justify-between">
                <span className="text-[11px] font-mono text-editorial-muted">Synthesizes live telemetry</span>
                <button
                  onClick={() => handleRun(scen.key)}
                  disabled={isRunning}
                  className="flex items-center gap-2 px-3.5 py-2 rounded bg-editorial-panel border border-editorial-border text-xs font-bold text-editorial-text hover:bg-editorial-panel/80 hover:text-editorial-accent transition-colors shadow-xs"
                >
                  <Play className={`w-3.5 h-3.5 ${isRunning ? 'animate-spin' : 'text-editorial-accent'}`} />
                  {isRunning ? 'Injecting Telemetry...' : 'Run Simulation'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
""")

print("Events, Attack Stories, and Simulation Lab pages written.")
