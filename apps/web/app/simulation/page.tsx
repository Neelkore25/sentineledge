'use client';

import React, { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import {
  Play,
  ArrowRight,
  CheckCircle2,
  UploadCloud,
  FileCode,
  Layers,
  Sparkles,
  AlertCircle
} from 'lucide-react';
import { api } from '@/lib/api';
import { Scenario } from '@/lib/types';
import { useApp } from '@/lib/store';

const SAMPLE_JSON_TELEMETRY = [
  {
    "source": "auth_gateway",
    "user_id": "sarah_connor",
    "asset_id": "asset-prod-db-01",
    "source_ip": "194.26.29.114",
    "event_type": "AUTH_LOGIN",
    "action": "LOGIN_SUCCESS",
    "status": "SUCCESS",
    "location": "Bucharest, Romania",
    "bytes_transferred": 1024,
    "event_metadata": { "mfa": false, "notes": "Off-hours login from unfamiliar geo" }
  },
  {
    "source": "database_proxy",
    "user_id": "sarah_connor",
    "asset_id": "asset-prod-db-01",
    "source_ip": "194.26.29.114",
    "event_type": "DATA_EGRESS",
    "action": "SQL_DUMP",
    "status": "SUCCESS",
    "bytes_transferred": 2800000000,
    "event_metadata": { "query": "SELECT * FROM customer_financial_records", "rows": 450000 }
  }
];

export default function SimulationLabPage() {
  const router = useRouter();
  const { triggerRefresh } = useApp();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [activeTab, setActiveTab] = useState<'catalog' | 'custom'>('catalog');
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [runningKey, setRunningKey] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);

  const [customJson, setCustomJson] = useState<string>(
    JSON.stringify(SAMPLE_JSON_TELEMETRY, null, 2)
  );
  const [jsonError, setJsonError] = useState<string | null>(null);
  const [isScanningJson, setIsScanningJson] = useState(false);

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

  const handleRunPreset = async (key: string) => {
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

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = event => {
      try {
        const text = event.target?.result as string;
        const parsed = JSON.parse(text);
        setCustomJson(JSON.stringify(parsed, null, 2));
        setJsonError(null);
      } catch (err: any) {
        setJsonError(`Invalid JSON file: ${err.message}`);
      }
    };
    reader.readAsText(file);
  };

  const handleScanCustomJson = async () => {
    try {
      setJsonError(null);
      setIsScanningJson(true);
      setResult(null);

      let parsed: any;
      try {
        parsed = JSON.parse(customJson);
      } catch (err: any) {
        setJsonError(`JSON Syntax Error: ${err.message}`);
        setIsScanningJson(false);
        return;
      }

      const payload = Array.isArray(parsed) ? parsed : [parsed];
      const res = await api.ingestCustomTelemetry(payload);
      setResult({
        scenario_name: `Custom JSON Scan (${res.events_ingested} events)`,
        events_generated: res.events_ingested,
        severity: res.severity,
        risk_score: res.risk_score,
        rule_matches: res.rule_matches || [],
        incident_id: res.incident_id
      });
    } catch (err: any) {
      let errMsg = err.message || 'Failed to scan telemetry';
      if (typeof errMsg === 'string' && errMsg.includes('"msg":')) {
        try {
          const parsedErr = JSON.parse(errMsg);
          if (Array.isArray(parsedErr) && parsedErr.length > 0) {
            errMsg = `Telemetry Validation Error: ${parsedErr[0].msg} for field '${parsedErr[0].loc?.slice(1)?.join('.') || 'payload'}'`;
          }
        } catch {}
      }
      setJsonError(`Scan failed: ${errMsg}`);
    } finally {
      setIsScanningJson(false);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div className="border-b border-editorial-border pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Simulation Lab & Telemetry Scanner</h1>
          <p className="text-xs text-editorial-muted font-mono mt-0.5">
            Safely inject synthetic attacks or upload custom JSON telemetry to test detection, AI analysis, and recovery readiness
          </p>
        </div>
        <div className="flex items-center bg-editorial-panel p-1 rounded-lg border border-editorial-border text-xs">
          <button
            onClick={() => setActiveTab('catalog')}
            className={`px-3 py-1.5 rounded-md font-medium transition-all ${
              activeTab === 'catalog'
                ? 'bg-editorial-surface text-editorial-text shadow-xs font-semibold'
                : 'text-editorial-muted hover:text-editorial-text'
            }`}
          >
            Attack Catalog
          </button>
          <button
            onClick={() => setActiveTab('custom')}
            className={`px-3 py-1.5 rounded-md font-medium transition-all ${
              activeTab === 'custom'
                ? 'bg-editorial-surface text-editorial-text shadow-xs font-semibold'
                : 'text-editorial-muted hover:text-editorial-text'
            }`}
          >
            Upload / Paste JSON
          </button>
        </div>
      </div>

      {/* Result Callout Banner */}
      {result && (
        <div className="p-5 rounded-xl border border-editorial-accent bg-editorial-surface shadow-md space-y-4 animate-in fade-in">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-status-healthy" />
              <h3 className="font-bold text-sm text-editorial-text">
                Scan Completed: {result.scenario_name}
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
              <span className="text-[10px] text-editorial-muted">EVENTS PROCESSED</span>
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

      {/* Tab 1: Attack Scenarios Catalog */}
      {activeTab === 'catalog' && (
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
                    onClick={() => handleRunPreset(scen.key)}
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
      )}

      {/* Tab 2: Custom JSON Telemetry Ingestion */}
      {activeTab === 'custom' && (
        <div className="border border-editorial-border rounded-xl bg-editorial-surface p-6 shadow-xs space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-editorial-border pb-4">
            <div>
              <h3 className="font-bold text-base text-editorial-text flex items-center gap-2">
                <FileCode className="w-4 h-4 text-editorial-accent" /> Custom Security Logs Payload
              </h3>
              <p className="text-xs text-editorial-muted font-mono mt-0.5">
                Paste JSON logs array or upload a .json file to run the 3-layer detection pipeline
              </p>
            </div>

            <div className="flex items-center gap-3">
              <input
                ref={fileInputRef}
                type="file"
                accept=".json,application/json"
                onChange={handleFileUpload}
                className="hidden"
              />
              <button
                onClick={() => fileInputRef.current?.click()}
                className="flex items-center gap-2 px-3.5 py-1.5 rounded bg-editorial-panel border border-editorial-border text-xs font-semibold text-editorial-text hover:bg-editorial-panel/80"
              >
                <UploadCloud className="w-3.5 h-3.5 text-editorial-accent" /> Upload .json File
              </button>
              <button
                onClick={() => setCustomJson(JSON.stringify(SAMPLE_JSON_TELEMETRY, null, 2))}
                className="px-3 py-1.5 rounded bg-editorial-panel border border-editorial-border text-xs font-medium text-editorial-muted hover:text-editorial-text"
              >
                Reset Template
              </button>
            </div>
          </div>

          {jsonError && (
            <div className="p-3 rounded-lg bg-status-critical/10 border border-status-critical/30 text-xs text-status-critical flex items-center gap-2 font-mono">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{jsonError}</span>
            </div>
          )}

          <div>
            <label className="block text-xs font-mono text-editorial-muted mb-2 uppercase">
              JSON Telemetry Stream:
            </label>
            <textarea
              rows={12}
              value={customJson}
              onChange={e => setCustomJson(e.target.value)}
              className="w-full font-mono text-xs p-4 rounded-lg bg-editorial-panel border border-editorial-border text-editorial-text focus:outline-none focus:border-editorial-accent transition-colors leading-relaxed"
              placeholder="Paste JSON events array here..."
            />
          </div>

          <div className="flex items-center justify-between pt-2 border-t border-editorial-border">
            <span className="text-xs text-editorial-muted font-mono">
              Processes rules, MAD behavior, temporal correlation, and risk calculation.
            </span>
            <button
              onClick={handleScanCustomJson}
              disabled={isScanningJson}
              className="flex items-center gap-2 px-5 py-2.5 rounded bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              <Sparkles className={`w-3.5 h-3.5 ${isScanningJson ? 'animate-spin' : ''}`} />
              {isScanningJson ? 'Scanning Telemetry Pipeline...' : 'Scan & Ingest JSON Logs'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
