'use client';

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
