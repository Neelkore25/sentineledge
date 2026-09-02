'use client';

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
