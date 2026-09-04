'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  AlertTriangle,
  ArrowRight,
  Sparkles,
  ShieldCheck,
  Play,
  FileCode,
  Layers,
  Activity,
  CheckCircle2,
  Lock
} from 'lucide-react';
import { useApp } from '@/lib/store';
import { api } from '@/lib/api';
import { Incident, SystemOverview, SecurityEvent } from '@/lib/types';
import { EvidenceRail } from '@/components/EvidenceRail';
import { RecoveryWindow } from '@/components/RecoveryWindow';

export default function DashboardPage() {
  const router = useRouter();
  const { viewMode, refreshTrigger, triggerRefresh } = useApp();
  const [stats, setStats] = useState<SystemOverview | null>(null);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [recentEvents, setRecentEvents] = useState<SecurityEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSeedingDemo, setIsSeedingDemo] = useState(false);

  useEffect(() => {
    async function loadDashboard() {
      try {
        setIsLoading(true);
        const [statsData, incData, eventData] = await Promise.all([
          api.getOverviewStats().catch(() => null),
          api.getIncidents().catch(() => []),
          api.getEvents({ limit: 8 }).catch(() => ({ items: [] }))
        ]);
        if (statsData) setStats(statsData);
        if (incData) setIncidents(incData);
        if (eventData?.items) setRecentEvents(eventData.items);
      } catch (e) {
        console.error('Failed to load dashboard:', e);
      } finally {
        setIsLoading(false);
      }
    }
    loadDashboard();
  }, [refreshTrigger]);

  const handleRunDemoExample = async () => {
    try {
      setIsSeedingDemo(true);
      await api.runScenario('brute_force');
      triggerRefresh();
    } catch (err: any) {
      alert(`Demo run failed: ${err.message || err}`);
    } finally {
      setIsSeedingDemo(false);
    }
  };

  const openIncidents = incidents.filter(i => i.status === 'OPEN' || i.status === 'INVESTIGATING');
  const orgRisk = stats?.organization_risk_score ?? 0.0;
  const orgBand = stats?.organization_risk_band ?? 'LOW';
  const hasNoData = incidents.length === 0;

  return (
    <div className="space-y-8 select-none">
      {/* Empty State Onboarding Banner */}
      {hasNoData && !isLoading && (
        <div className="border border-editorial-border rounded-xl bg-editorial-surface p-8 shadow-sm space-y-6 animate-in fade-in">
          <div className="max-w-2xl space-y-3">
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-status-healthy/10 border border-status-healthy/30 text-status-healthy text-xs font-mono font-semibold">
              <ShieldCheck className="w-3.5 h-3.5" /> SYSTEM CLEAN • NO ACTIVE INCIDENTS
            </div>
            <h2 className="text-2xl font-bold tracking-tight text-editorial-text">
              Start Your First Security Analysis
            </h2>
            <p className="text-xs text-editorial-muted leading-relaxed">
              SentinelEdge analyzes security event logs to detect brute-force attacks, privilege escalation, and data exfiltration spikes. Upload your own security logs or run a safe synthetic simulation to see how SentinelEdge detects and correlates multi-stage threats.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Link
              href="/analyze"
              className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity"
            >
              <FileCode className="w-4 h-4" /> Analyze Security Logs <ArrowRight className="w-3.5 h-3.5" />
            </Link>

            <button
              onClick={handleRunDemoExample}
              disabled={isSeedingDemo}
              className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-editorial-panel border border-editorial-border text-xs font-semibold text-editorial-text hover:bg-editorial-panel/80 hover:text-editorial-accent transition-colors shadow-xs"
            >
              <Sparkles className={`w-4 h-4 text-editorial-accent ${isSeedingDemo ? 'animate-spin' : ''}`} />
              {isSeedingDemo ? 'Injecting Synthetic Demo...' : 'Try Synthetic Example (1-Click)'}
            </button>
          </div>

          {/* 3 Step Workflow Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-editorial-border font-mono text-xs">
            <div className="p-4 rounded-lg bg-editorial-panel/60 border border-editorial-border space-y-1.5">
              <div className="text-[10px] text-editorial-accent font-bold">STEP 01</div>
              <h4 className="font-bold text-editorial-text text-sm">Provide Telemetry</h4>
              <p className="text-[11px] text-editorial-muted">
                Upload JSON event streams or select safe attack scenarios in the Simulation Lab.
              </p>
            </div>

            <div className="p-4 rounded-lg bg-editorial-panel/60 border border-editorial-border space-y-1.5">
              <div className="text-[10px] text-editorial-accent font-bold">STEP 02</div>
              <h4 className="font-bold text-editorial-text text-sm">3-Layer Analysis</h4>
              <p className="text-[11px] text-editorial-muted">
                FastAPI engine evaluates deterministic rules, MAD anomaly baselines, and temporal correlation.
              </p>
            </div>

            <div className="p-4 rounded-lg bg-editorial-panel/60 border border-editorial-border space-y-1.5">
              <div className="text-[10px] text-editorial-accent font-bold">STEP 03</div>
              <h4 className="font-bold text-editorial-text text-sm">Investigate & Respond</h4>
              <p className="text-[11px] text-editorial-muted">
                Review grounded AI evidence citations, evaluate recovery readiness, and record analyst actions.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Populated Operations Dashboard */}
      {!hasNoData && (
        <>
          <EvidenceRail currentStage="scored" eventCount={recentEvents.length} riskScore={orgRisk} />

          <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
            <div className="md:col-span-4 border border-editorial-border rounded-lg bg-editorial-surface p-5 flex flex-col justify-between shadow-xs">
              <div>
                <div className="flex items-center justify-between text-[11px] font-mono text-editorial-muted uppercase mb-2">
                  <span>ORGANIZATION RISK</span>
                  <span className={`font-semibold ${
                    orgBand === 'CRITICAL' ? 'text-status-critical' :
                    orgBand === 'HIGH' ? 'text-status-warning' : 'text-status-healthy'
                  }`}>
                    {orgBand}
                  </span>
                </div>
                <div className="flex items-baseline gap-3">
                  <span className="text-5xl font-extrabold font-mono text-editorial-text">{orgRisk.toFixed(0)}</span>
                  <span className="text-xs text-editorial-muted font-mono">/ 100</span>
                </div>
                <p className="text-xs text-editorial-muted mt-2">
                  {viewMode === 'executive'
                    ? 'Composite business exposure across critical infrastructure assets and active incident pressure.'
                    : 'Weighted risk calculated from deterministic rules, MAD anomaly deviations, and asset impact.'}
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
                      {stats?.incident_pressure.CRITICAL ?? 0}
                    </div>
                  </div>
                  <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
                    <div className="text-[10px] text-editorial-muted uppercase">HIGH</div>
                    <div className="text-xl font-bold text-status-warning mt-1">
                      {stats?.incident_pressure.HIGH ?? 0}
                    </div>
                  </div>
                  <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
                    <div className="text-[10px] text-editorial-muted uppercase">MEDIUM</div>
                    <div className="text-xl font-bold text-status-info mt-1">
                      {stats?.incident_pressure.MEDIUM ?? 0}
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
                <Link href="/analyze" className="text-editorial-accent font-semibold flex items-center gap-1 hover:underline">
                  Analyze New Telemetry <ArrowRight className="w-3.5 h-3.5" />
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
                          <span
                            className={`font-mono text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${
                              inc.severity === 'CRITICAL'
                                ? 'bg-status-critical/15 text-status-critical'
                                : inc.severity === 'HIGH'
                                ? 'bg-status-warning/15 text-status-warning'
                                : 'bg-status-info/15 text-status-info'
                            }`}
                          >
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
            </div>

            <div className="md:col-span-5">
              <RecoveryWindow
                lastBackupHours={3.5}
                targetRpoHours={4.0}
                rpoGapHours={0.0}
                lastTestDays={18}
                readinessScore={stats?.recovery_readiness_score ?? 85.0}
                verified={true}
                primaryWeakness="ERP Suite incremental backup restore test is overdue by 34 days."
              />
            </div>
          </div>
        </>
      )}
    </div>
  );
}
