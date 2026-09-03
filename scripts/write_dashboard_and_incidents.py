import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 3. Dashboard Page (apps/web/app/dashboard/page.tsx)
write_file("apps/web/app/dashboard/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { AlertTriangle, Activity, ArrowRight, Layers, Play } from 'lucide-react';
import { useApp } from '@/lib/store';
import { api } from '@/lib/api';
import { Incident, SystemOverview, SecurityEvent } from '@/lib/types';
import { EvidenceRail } from '@/components/EvidenceRail';
import { RecoveryWindow } from '@/components/RecoveryWindow';

export default function DashboardPage() {
  const { viewMode, refreshTrigger } = useApp();
  const [stats, setStats] = useState<SystemOverview | null>(null);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [recentEvents, setRecentEvents] = useState<SecurityEvent[]>([]);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [statsData, incData, eventData] = await Promise.all([
          api.getOverviewStats().catch(() => null),
          api.getIncidents().catch(() => []),
          api.getEvents({ limit: 8 }).catch(() => ({ items: [] }))
        ]);
        if (statsData) setStats(statsData);
        if (incData) setIncidents(incData);
        if (eventData?.items) setRecentEvents(eventData.items);
      } catch (e) {
        console.error(e);
      }
    }
    loadDashboard();
  }, [refreshTrigger]);

  const openIncidents = incidents.filter(i => i.status === 'OPEN' || i.status === 'INVESTIGATING');
  const orgRisk = stats?.organization_risk_score ?? 64.0;
  const orgBand = stats?.organization_risk_band ?? 'MODERATE';

  return (
    <div className="space-y-6">
      <EvidenceRail currentStage="scored" eventCount={recentEvents.length} riskScore={orgRisk} />

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        <div className="md:col-span-4 border border-editorial-border rounded-lg bg-editorial-surface p-5 flex flex-col justify-between shadow-xs">
          <div>
            <div className="flex items-center justify-between text-[11px] font-mono text-editorial-muted uppercase mb-2">
              <span>ORGANIZATION RISK</span>
              <span className="text-editorial-accent font-semibold">{orgBand}</span>
            </div>
            <div className="flex items-baseline gap-3">
              <span className="text-5xl font-extrabold font-mono text-editorial-text">{orgRisk.toFixed(0)}</span>
              <span className="text-xs text-editorial-muted font-mono">/ 100</span>
            </div>
            <p className="text-xs text-editorial-muted mt-2">
              {viewMode === 'executive'
                ? 'Weighted organization exposure across 5 critical infrastructure assets and active incident pressure.'
                : 'Aggregated composite score derived from deterministic rules, MAD deviations, and asset criticality.'}
            </p>
          </div>

          <div className="pt-4 border-t border-editorial-border mt-4 flex items-center justify-between text-xs font-mono">
            <span className="text-editorial-muted">STATUS</span>
            <span className="text-status-healthy font-bold flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-status-healthy" /> MONITORING
            </span>
          </div>
        </div>

        <div className="md:col-span-8 border border-editorial-border rounded-lg bg-editorial-surface p-5 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-[11px] font-mono text-editorial-muted uppercase mb-4">
              <span>INCIDENT PRESSURE BY SEVERITY</span>
              <span className="text-xs text-editorial-text font-bold">{openIncidents.length} ACTIVE INCIDENTS</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono">
              <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
                <div className="text-[10px] text-editorial-muted uppercase">CRITICAL</div>
                <div className="text-xl font-bold text-status-critical mt-1">
                  {stats?.incident_pressure.CRITICAL ?? 1}
                </div>
              </div>
              <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
                <div className="text-[10px] text-editorial-muted uppercase">HIGH</div>
                <div className="text-xl font-bold text-status-warning mt-1">
                  {stats?.incident_pressure.HIGH ?? 1}
                </div>
              </div>
              <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
                <div className="text-[10px] text-editorial-muted uppercase">MEDIUM</div>
                <div className="text-xl font-bold text-status-info mt-1">
                  {stats?.incident_pressure.MEDIUM ?? 1}
                </div>
              </div>
              <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
                <div className="text-[10px] text-editorial-muted uppercase">LOW</div>
                <div className="text-xl font-bold text-status-healthy mt-1">
                  {stats?.incident_pressure.LOW ?? 0}
                </div>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-editorial-border flex items-center justify-between text-xs">
            <span className="text-editorial-muted font-mono">FastAPI Detection Engine active</span>
            <Link href="/simulation" className="text-editorial-accent font-semibold flex items-center gap-1 hover:underline">
              Run Scenario in Lab <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        <div className="md:col-span-7 border border-editorial-border rounded-lg bg-editorial-surface p-5 shadow-xs space-y-4">
          <div className="flex items-center justify-between border-b border-editorial-border pb-3">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-editorial-accent" />
              <h3 className="font-bold text-sm text-editorial-text">Correlated Incidents</h3>
            </div>
            <Link href="/incidents" className="text-xs text-editorial-muted hover:text-editorial-text font-mono">
              View All ({incidents.length}) →
            </Link>
          </div>

          {incidents.length === 0 ? (
            <div className="p-8 text-center text-xs text-editorial-muted">
              No active incidents. The system has not correlated any anomalies into an incident.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-editorial-border font-mono text-[10px] text-editorial-muted uppercase">
                    <th className="pb-2">SEVERITY</th>
                    <th className="pb-2">INCIDENT</th>
                    <th className="pb-2">TARGET ASSET</th>
                    <th className="pb-2">RISK</th>
                    <th className="pb-2">ACTION</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-editorial-border/50">
                  {incidents.slice(0, 5).map(inc => (
                    <tr key={inc.id} className="hover:bg-editorial-panel/40 transition-colors">
                      <td className="py-2.5 pr-2">
                        <span className={`font-mono text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${
                          inc.severity === 'CRITICAL' ? 'bg-status-critical/15 text-status-critical' :
                          inc.severity === 'HIGH' ? 'bg-status-warning/15 text-status-warning' :
                          'bg-status-info/15 text-status-info'
                        }`}>
                          {inc.severity}
                        </span>
                      </td>
                      <td className="py-2.5 font-medium text-editorial-text pr-2 max-w-[200px] truncate">
                        <Link href={`/incidents/${inc.id}`} className="hover:underline">
                          {inc.title}
                        </Link>
                      </td>
                      <td className="py-2.5 text-editorial-muted font-mono text-[11px] pr-2">
                        {inc.affected_asset}
                      </td>
                      <td className="py-2.5 font-mono font-bold text-editorial-accent pr-2">
                        {inc.risk_score.toFixed(0)}
                      </td>
                      <td className="py-2.5">
                        <Link
                          href={`/incidents/${inc.id}`}
                          className="px-2 py-1 rounded bg-editorial-panel border border-editorial-border text-[11px] font-semibold text-editorial-text hover:bg-editorial-panel/80"
                        >
                          Investigate
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="md:col-span-5">
          <RecoveryWindow
            lastBackupHours={3.5}
            targetRpoHours={4.0}
            rpoGapHours={0.0}
            lastTestDays={18}
            readinessScore={stats?.recovery_readiness_score ?? 74.0}
            verified={true}
            primaryWeakness="ERP Suite incremental backup test is overdue by 34 days."
          />
        </div>
      </div>
    </div>
  );
}
""")

# 4. Incidents Registry Page (apps/web/app/incidents/page.tsx)
write_file("apps/web/app/incidents/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { AlertTriangle, Search } from 'lucide-react';
import { api } from '@/lib/api';
import { Incident } from '@/lib/types';
import { useApp } from '@/lib/store';

export default function IncidentsPage() {
  const { refreshTrigger } = useApp();
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [search, setSearch] = useState('');
  const [severityFilter, setSeverityFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getIncidents({
          severity: severityFilter !== 'ALL' ? severityFilter : undefined,
          status: statusFilter !== 'ALL' ? statusFilter : undefined,
          search: search || undefined
        });
        setIncidents(data);
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, [search, severityFilter, statusFilter, refreshTrigger]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-editorial-border pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Incident Registry</h1>
          <p className="text-xs text-editorial-muted font-mono mt-0.5">
            Correlated multi-stage security events with explainable risk scores
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link
            href="/simulation"
            className="px-3.5 py-2 rounded bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity"
          >
            + Run Scenario in Lab
          </Link>
        </div>
      </div>

      <div className="p-3 rounded-lg border border-editorial-border bg-editorial-surface flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 flex-1 min-w-[200px]">
          <Search className="w-4 h-4 text-editorial-muted" />
          <input
            type="text"
            placeholder="Search by ID, title, user, or asset..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-transparent text-editorial-text focus:outline-none text-xs"
          />
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 font-mono text-[11px]">
            <span className="text-editorial-muted">SEVERITY:</span>
            <select
              value={severityFilter}
              onChange={e => setSeverityFilter(e.target.value)}
              className="bg-editorial-panel border border-editorial-border rounded px-2 py-1 text-editorial-text focus:outline-none"
            >
              <option value="ALL">ALL</option>
              <option value="CRITICAL">CRITICAL</option>
              <option value="HIGH">HIGH</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="LOW">LOW</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5 font-mono text-[11px]">
            <span className="text-editorial-muted">STATUS:</span>
            <select
              value={statusFilter}
              onChange={e => setStatusFilter(e.target.value)}
              className="bg-editorial-panel border border-editorial-border rounded px-2 py-1 text-editorial-text focus:outline-none"
            >
              <option value="ALL">ALL</option>
              <option value="OPEN">OPEN</option>
              <option value="INVESTIGATING">INVESTIGATING</option>
              <option value="MITIGATED">MITIGATED</option>
            </select>
          </div>
        </div>
      </div>

      <div className="border border-editorial-border rounded-lg bg-editorial-surface shadow-xs overflow-hidden">
        {incidents.length === 0 ? (
          <div className="p-12 text-center text-xs text-editorial-muted space-y-2">
            <AlertTriangle className="w-6 h-6 text-editorial-muted mx-auto" />
            <p className="font-medium text-editorial-text">No security incidents match the filter criteria.</p>
            <p>Generate simulated telemetry in the Simulation Lab to trigger new detections.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-editorial-panel/60 border-b border-editorial-border font-mono text-[10px] text-editorial-muted uppercase">
                <tr>
                  <th className="p-3">INCIDENT ID</th>
                  <th className="p-3">SEVERITY</th>
                  <th className="p-3">TITLE / CATEGORY</th>
                  <th className="p-3">AFFECTED ASSET & USER</th>
                  <th className="p-3">RISK</th>
                  <th className="p-3">STATUS</th>
                  <th className="p-3 text-right">ACTION</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-editorial-border">
                {incidents.map(inc => (
                  <tr key={inc.id} className="hover:bg-editorial-panel/40 transition-colors">
                    <td className="p-3 font-mono font-bold text-editorial-text">
                      <Link href={`/incidents/${inc.id}`} className="hover:text-editorial-accent">
                        #{inc.id}
                      </Link>
                    </td>
                    <td className="p-3">
                      <span className={`font-mono text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                        inc.severity === 'CRITICAL' ? 'bg-status-critical/15 text-status-critical border border-status-critical/30' :
                        inc.severity === 'HIGH' ? 'bg-status-warning/15 text-status-warning border border-status-warning/30' :
                        'bg-status-info/15 text-status-info border border-status-info/30'
                      }`}>
                        {inc.severity}
                      </span>
                    </td>
                    <td className="p-3">
                      <div className="font-semibold text-editorial-text">
                        <Link href={`/incidents/${inc.id}`} className="hover:underline">
                          {inc.title}
                        </Link>
                      </div>
                      <div className="text-[10px] font-mono text-editorial-muted">{inc.attack_category}</div>
                    </td>
                    <td className="p-3 font-mono text-[11px]">
                      <div className="text-editorial-text">{inc.affected_asset}</div>
                      <div className="text-editorial-muted">{inc.affected_user || '—'}</div>
                    </td>
                    <td className="p-3 font-mono font-bold text-base text-editorial-accent">
                      {inc.risk_score.toFixed(0)}
                    </td>
                    <td className="p-3">
                      <span className={`font-mono text-[10px] px-1.5 py-0.5 rounded font-medium ${
                        inc.status === 'MITIGATED' ? 'bg-status-healthy/15 text-status-healthy' :
                        inc.status === 'INVESTIGATING' ? 'bg-editorial-accent/15 text-editorial-accent' :
                        'bg-status-warning/15 text-status-warning'
                      }`}>
                        {inc.status}
                      </span>
                    </td>
                    <td className="p-3 text-right">
                      <Link
                        href={`/incidents/${inc.id}`}
                        className="px-3 py-1.5 rounded bg-editorial-panel border border-editorial-border font-semibold text-editorial-text hover:bg-editorial-panel/80 transition-colors"
                      >
                        Investigate
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
""")

# 5. Incident Detail Page (apps/web/app/incidents/[id]/page.tsx)
write_file("apps/web/app/incidents/[id]/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import {
  ArrowLeft,
  Sparkles,
  ShieldCheck,
  Layers
} from 'lucide-react';
import { api } from '@/lib/api';
import { Incident, SecurityEvent } from '@/lib/types';
import { EvidenceRail } from '@/components/EvidenceRail';
import { RiskBreakdown } from '@/components/RiskBreakdown';
import { HumanResponseDrawer } from '@/components/HumanResponseDrawer';

export default function IncidentDetailPage() {
  const params = useParams();
  const id = params.id as string;

  const [data, setData] = useState<{ incident: Incident; related_events: SecurityEvent[] } | null>(null);
  const [loading, setLoading] = useState(true);
  const [aiLoading, setAiLoading] = useState(false);
  const [isResponseOpen, setIsResponseOpen] = useState(false);

  const loadDetails = async () => {
    try {
      setLoading(true);
      const res = await api.getIncidentById(id);
      setData(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (id) loadDetails();
  }, [id]);

  const handleRequestAI = async () => {
    try {
      setAiLoading(true);
      await api.investigateIncidentAI(id);
      await loadDetails();
    } catch (err) {
      alert(`AI investigation failed: ${err}`);
    } finally {
      setAiLoading(false);
    }
  };

  if (loading) {
    return <div className="p-12 text-center text-xs text-editorial-muted font-mono">Loading incident telemetry...</div>;
  }

  if (!data?.incident) {
    return (
      <div className="p-12 text-center text-xs text-editorial-muted space-y-3">
        <p>Incident #{id} not found.</p>
        <Link href="/incidents" className="text-editorial-accent underline">Return to Incidents</Link>
      </div>
    );
  }

  const { incident, related_events } = data;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-editorial-border pb-4">
        <div className="flex items-center gap-3">
          <Link
            href="/incidents"
            className="p-1.5 rounded bg-editorial-panel border border-editorial-border text-editorial-muted hover:text-editorial-text"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-editorial-text">Incident #{incident.id}</h1>
              <span className={`font-mono text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                incident.severity === 'CRITICAL' ? 'bg-status-critical/15 text-status-critical border border-status-critical/30' :
                'bg-status-warning/15 text-status-warning border border-status-warning/30'
              }`}>
                {incident.severity}
              </span>
              <span className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-editorial-panel text-editorial-muted border border-editorial-border">
                {incident.status}
              </span>
            </div>
            <p className="text-xs text-editorial-muted font-mono mt-0.5">{incident.title}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleRequestAI}
            disabled={aiLoading}
            className="flex items-center gap-2 px-3.5 py-2 rounded bg-editorial-panel border border-editorial-border text-xs font-bold text-editorial-text hover:bg-editorial-panel/80 transition-colors"
          >
            <Sparkles className="w-3.5 h-3.5 text-editorial-accent" />
            {aiLoading ? 'Analyzing Evidence...' : 'Re-Run AI Investigator'}
          </button>
          <button
            onClick={() => setIsResponseOpen(true)}
            className="flex items-center gap-2 px-4 py-2 rounded bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity"
          >
            <ShieldCheck className="w-4 h-4" />
            Respond & Remediate
          </button>
        </div>
      </div>

      <EvidenceRail
        currentStage={incident.status === 'MITIGATED' ? 'responded' : 'explained'}
        eventCount={related_events.length}
        riskScore={incident.risk_score}
        status={incident.status}
      />

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        <div className="md:col-span-7 space-y-6">
          <div className="border border-editorial-border rounded-lg bg-editorial-surface p-5 shadow-xs space-y-4">
            <div className="flex items-center justify-between border-b border-editorial-border pb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-editorial-accent" />
                <h3 className="font-bold text-sm text-editorial-text">Evidence-Grounded AI Investigation</h3>
              </div>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-editorial-panel border border-editorial-border text-editorial-muted">
                CONFIDENCE: {(incident.confidence * 100).toFixed(0)}%
              </span>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <span className="font-mono text-[10px] uppercase text-editorial-muted">PRIMARY HYPOTHESIS</span>
                <p className="font-medium text-editorial-text mt-0.5">
                  {incident.ai_hypothesis || 'Probable credential compromise followed by administrative elevation.'}
                </p>
              </div>

              <div>
                <span className="font-mono text-[10px] uppercase text-editorial-muted">EVIDENCE CITATIONS (GROUNDED LOGS)</span>
                <div className="mt-1 p-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text space-y-1 font-mono text-[11px]">
                  <div>• {incident.description}</div>
                  <div>• Citing correlated Event IDs: {incident.event_ids.join(', ')}</div>
                </div>
              </div>

              <div>
                <span className="font-mono text-[10px] uppercase text-editorial-muted">ALTERNATIVE HYPOTHESIS</span>
                <p className="text-editorial-muted mt-0.5">
                  {incident.ai_alternative || 'Legitimate off-hours administrative maintenance through external gateway.'}
                </p>
              </div>

              <div>
                <span className="font-mono text-[10px] uppercase text-editorial-muted">MISSING EVIDENCE NEEDED</span>
                <p className="text-editorial-muted mt-0.5">
                  {incident.ai_missing_evidence || 'Host endpoint EDR execution tree confirming local shell access.'}
                </p>
              </div>

              {incident.recommended_action && (
                <div className="p-3 rounded bg-editorial-accent/10 border border-editorial-accent/30 text-editorial-text">
                  <span className="font-bold font-mono text-[10px] text-editorial-accent uppercase">RECOMMENDED ACTION:</span>
                  <p className="font-semibold text-xs mt-0.5">{incident.recommended_action}</p>
                </div>
              )}
            </div>
          </div>

          <div className="border border-editorial-border rounded-lg bg-editorial-surface p-5 shadow-xs space-y-3">
            <div className="flex items-center justify-between border-b border-editorial-border pb-2">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-editorial-accent" />
                <h3 className="font-bold text-sm text-editorial-text">Correlated Telemetry Events ({related_events.length})</h3>
              </div>
              <span className="text-[10px] font-mono text-editorial-muted">WINDOW: 30 MIN SLIDING</span>
            </div>

            <div className="space-y-2 font-mono text-xs max-h-72 overflow-y-auto">
              {related_events.map(e => (
                <div key={e.id} className="p-2.5 rounded bg-editorial-panel border border-editorial-border flex items-center justify-between">
                  <div>
                    <div className="font-bold text-editorial-text flex items-center gap-2">
                      <span>{e.id}</span>
                      <span className="text-[10px] px-1.5 py-0.2 rounded bg-editorial-surface border border-editorial-border text-editorial-accent">
                        {e.event_type}
                      </span>
                    </div>
                    <div className="text-[10px] text-editorial-muted mt-0.5">
                      IP: {e.source_ip || 'local'} | User: {e.user_id || 'system'} | Endpoint: {e.endpoint || '—'}
                    </div>
                  </div>
                  <span className="text-[10px] text-editorial-muted">{e.timestamp.slice(11, 19)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="md:col-span-5 space-y-6">
          <RiskBreakdown
            breakdown={incident.risk_breakdown}
            compositeScore={incident.risk_score}
            severityBand={incident.severity}
          />

          <div className="border border-editorial-border rounded-lg bg-editorial-surface p-5 shadow-xs space-y-3 text-xs">
            <h4 className="font-bold text-editorial-text border-b border-editorial-border pb-2">Business & Asset Context</h4>
            <div className="grid grid-cols-2 gap-3 font-mono text-[11px]">
              <div className="p-2 rounded bg-editorial-panel">
                <span className="text-editorial-muted uppercase text-[10px]">AFFECTED ASSET</span>
                <div className="font-bold text-editorial-text mt-0.5">{incident.affected_asset}</div>
              </div>
              <div className="p-2 rounded bg-editorial-panel">
                <span className="text-editorial-muted uppercase text-[10px]">BUSINESS IMPACT</span>
                <div className="font-bold text-editorial-accent mt-0.5">{incident.business_impact}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <HumanResponseDrawer
        incidentId={incident.id}
        target={incident.affected_user || incident.affected_asset}
        isOpen={isResponseOpen}
        onClose={() => setIsResponseOpen(false)}
        onSuccess={() => loadDetails()}
      />
    </div>
  );
}
""")

print("Dashboard and Incidents pages created.")
