'use client';

import React, { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import {
  Sparkles,
  UploadCloud,
  FileCode,
  Play,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  ShieldAlert,
  Info,
  Layers,
  RotateCcw
} from 'lucide-react';
import { api } from '@/lib/api';
import { Scenario } from '@/lib/types';
import { useApp } from '@/lib/store';

const SYNTHETIC_TELEMETRY_EXAMPLE = [
  {
    "source": "auth_gateway",
    "user_id": "sarah_connor",
    "asset_id": "ASSET_AUTH_PORTAL",
    "source_ip": "194.26.29.114",
    "event_type": "LOGIN_FAILED",
    "action": "LOGIN",
    "status": "FAILURE",
    "endpoint": "/api/v1/auth/login",
    "location": "Bucharest, RO",
    "bytes_transferred": 1024,
    "event_metadata": { "synthetic": true, "reason": "Invalid credential attempt 1" }
  },
  {
    "source": "auth_gateway",
    "user_id": "sarah_connor",
    "asset_id": "ASSET_AUTH_PORTAL",
    "source_ip": "194.26.29.114",
    "event_type": "LOGIN_FAILED",
    "action": "LOGIN",
    "status": "FAILURE",
    "endpoint": "/api/v1/auth/login",
    "location": "Bucharest, RO",
    "bytes_transferred": 1024,
    "event_metadata": { "synthetic": true, "reason": "Invalid credential attempt 2" }
  },
  {
    "source": "auth_gateway",
    "user_id": "sarah_connor",
    "asset_id": "ASSET_AUTH_PORTAL",
    "source_ip": "194.26.29.114",
    "event_type": "LOGIN_SUCCESS",
    "action": "LOGIN",
    "status": "SUCCESS",
    "endpoint": "/api/v1/auth/login",
    "location": "Bucharest, RO",
    "bytes_transferred": 2048,
    "event_metadata": { "synthetic": true, "mfa_bypassed": true }
  },
  {
    "source": "database_proxy",
    "user_id": "sarah_connor",
    "asset_id": "ASSET_CUSTOMER_DB",
    "source_ip": "194.26.29.114",
    "event_type": "DATA_EGRESS",
    "action": "SQL_DUMP",
    "status": "SUCCESS",
    "endpoint": "/api/v1/data/export",
    "location": "Bucharest, RO",
    "bytes_transferred": 2800000000,
    "event_metadata": { "synthetic": true, "query": "SELECT * FROM customer_financial_records", "rows": 450000 }
  }
];

export default function AnalyzePage() {
  const router = useRouter();
  const { triggerRefresh } = useApp();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [activeTab, setActiveTab] = useState<'upload' | 'simulations'>('upload');
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [runningKey, setRunningKey] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);

  const [customJson, setCustomJson] = useState<string>('');
  const [validationState, setValidationState] = useState<{ isValid: boolean; message: string; count?: number } | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    async function loadScenarios() {
      try {
        const data = await api.getScenarios();
        setScenarios(data);
      } catch (e) {
        console.error('Failed to load scenarios:', e);
      }
    }
    loadScenarios();
  }, []);

  const handleJsonChange = (text: string) => {
    setCustomJson(text);
    if (!text.trim()) {
      setValidationState(null);
      return;
    }

    try {
      const parsed = JSON.parse(text);
      const items = Array.isArray(parsed) ? parsed : [parsed];
      if (items.length === 0) {
        setValidationState({ isValid: false, message: 'JSON array is empty.' });
        return;
      }
      setValidationState({
        isValid: true,
        message: `Valid JSON telemetry stream detected (${items.length} event${items.length > 1 ? 's' : ''}).`,
        count: items.length
      });
    } catch (err: any) {
      setValidationState({ isValid: false, message: `JSON Syntax Error: ${err.message}` });
    }
  };

  const handleLoadSyntheticExample = () => {
    const formatted = JSON.stringify(SYNTHETIC_TELEMETRY_EXAMPLE, null, 2);
    handleJsonChange(formatted);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = event => {
      const text = event.target?.result as string;
      handleJsonChange(text);
    };
    reader.readAsText(file);
  };

  const handleAnalyzeJson = async () => {
    if (!customJson.trim()) {
      setValidationState({ isValid: false, message: 'Please upload or paste JSON telemetry to analyze.' });
      return;
    }

    try {
      setIsAnalyzing(true);
      setResult(null);

      const parsed = JSON.parse(customJson);
      const payload = Array.isArray(parsed) ? parsed : [parsed];

      const res = await api.ingestCustomTelemetry(payload);
      setResult({
        title: `Analysis Complete: ${res.events_ingested} Events Processed`,
        events_count: res.events_ingested,
        severity: res.severity,
        risk_score: res.risk_score,
        rule_matches: res.rule_matches || [],
        incident_id: res.incident_id,
        target_asset: res.target_asset
      });
      triggerRefresh();
    } catch (err: any) {
      let errMsg = err.message || 'Unable to process telemetry';
      if (typeof errMsg === 'string' && errMsg.includes('"msg":')) {
        try {
          const parsedErr = JSON.parse(errMsg);
          if (Array.isArray(parsedErr) && parsedErr.length > 0) {
            errMsg = `Telemetry Validation Error: ${parsedErr[0].msg} for field '${parsedErr[0].loc?.slice(1)?.join('.') || 'payload'}'`;
          }
        } catch {}
      }
      setValidationState({ isValid: false, message: `Analysis failed: ${errMsg}` });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleRunSimulation = async (key: string) => {
    try {
      setRunningKey(key);
      setResult(null);
      const res = await api.runScenario(key);
      setResult({
        title: `Simulation Executed: ${res.scenario_name}`,
        events_count: res.events_generated,
        severity: res.severity,
        risk_score: res.risk_score,
        rule_matches: res.rule_matches || [],
        incident_id: res.incident_id
      });
      triggerRefresh();
    } catch (err: any) {
      alert(`Simulation failed: ${err.message || err}`);
    } finally {
      setRunningKey(null);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto select-none">
      {/* Page Header */}
      <div className="border-b border-editorial-border pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Analyze Security Data</h1>
          <p className="text-xs text-editorial-muted font-mono mt-0.5">
            Provide structured telemetry logs or execute safe attack simulations to run the 3-layer detection pipeline
          </p>
        </div>

        {/* Tab Toggle */}
        <div className="flex items-center bg-editorial-panel p-1 rounded-lg border border-editorial-border text-xs">
          <button
            onClick={() => setActiveTab('upload')}
            className={`px-3.5 py-1.5 rounded-md font-medium transition-all ${
              activeTab === 'upload'
                ? 'bg-editorial-surface text-editorial-text shadow-xs font-semibold'
                : 'text-editorial-muted hover:text-editorial-text'
            }`}
          >
            Upload / Paste JSON
          </button>
          <button
            onClick={() => setActiveTab('simulations')}
            className={`px-3.5 py-1.5 rounded-md font-medium transition-all ${
              activeTab === 'simulations'
                ? 'bg-editorial-surface text-editorial-text shadow-xs font-semibold'
                : 'text-editorial-muted hover:text-editorial-text'
            }`}
          >
            Safe Simulations
          </button>
        </div>
      </div>

      {/* Dynamic Results Banner */}
      {result && (
        <div className="p-5 rounded-xl border border-editorial-accent bg-editorial-surface shadow-md space-y-4 animate-in fade-in">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <CheckCircle2 className="w-5 h-5 text-status-healthy" />
              <div>
                <h3 className="font-bold text-sm text-editorial-text">{result.title}</h3>
                <div className="text-xs text-editorial-muted font-mono">
                  {result.rule_matches.length > 0
                    ? `Correlated into Incident #${result.incident_id}`
                    : 'No critical violations triggered.'}
                </div>
              </div>
            </div>
            <span
              className={`font-mono text-xs px-2.5 py-1 rounded font-bold uppercase ${
                result.severity === 'CRITICAL'
                  ? 'bg-status-critical/15 text-status-critical'
                  : result.severity === 'HIGH'
                  ? 'bg-status-warning/15 text-status-warning'
                  : 'bg-status-info/15 text-status-info'
              }`}
            >
              {result.severity} ({result.risk_score}/100)
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
            <div className="p-2.5 rounded bg-editorial-panel border border-editorial-border">
              <span className="text-[10px] text-editorial-muted">EVENTS ANALYZED</span>
              <div className="text-base font-bold text-editorial-text mt-0.5">{result.events_count}</div>
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
              <span className="text-[10px] text-editorial-muted">CORRELATION STATUS</span>
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

      {/* Tab 1: Upload / Paste JSON */}
      {activeTab === 'upload' && (
        <div className="border border-editorial-border rounded-xl bg-editorial-surface p-6 shadow-xs space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-editorial-border pb-4">
            <div>
              <h3 className="font-bold text-base text-editorial-text flex items-center gap-2">
                <FileCode className="w-4 h-4 text-editorial-accent" /> Security Telemetry Stream (JSON)
              </h3>
              <p className="text-xs text-editorial-muted font-mono mt-0.5">
                Paste structured security event logs or load a pre-validated synthetic test stream
              </p>
            </div>

            <div className="flex items-center gap-2.5">
              <input
                ref={fileInputRef}
                type="file"
                accept=".json,application/json"
                onChange={handleFileUpload}
                className="hidden"
              />
              <button
                onClick={() => fileInputRef.current?.click()}
                className="flex items-center gap-2 px-3 py-1.5 rounded bg-editorial-panel border border-editorial-border text-xs font-semibold text-editorial-text hover:bg-editorial-panel/80"
              >
                <UploadCloud className="w-3.5 h-3.5 text-editorial-accent" /> Upload .json File
              </button>
              <button
                onClick={handleLoadSyntheticExample}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-editorial-accent/10 border border-editorial-accent/30 text-xs font-bold text-editorial-accent hover:bg-editorial-accent/20 transition-colors"
              >
                <Sparkles className="w-3.5 h-3.5" /> Load Synthetic Example
              </button>
            </div>
          </div>

          {/* Validation Status Indicator */}
          {validationState && (
            <div
              className={`p-3 rounded-lg border text-xs flex items-center gap-2 font-mono ${
                validationState.isValid
                  ? 'bg-status-healthy/10 border-status-healthy/30 text-status-healthy'
                  : 'bg-status-critical/10 border-status-critical/30 text-status-critical'
              }`}
            >
              {validationState.isValid ? (
                <CheckCircle2 className="w-4 h-4 shrink-0" />
              ) : (
                <AlertCircle className="w-4 h-4 shrink-0" />
              )}
              <span>{validationState.message}</span>
            </div>
          )}

          {/* JSON Textarea */}
          <div>
            <div className="flex items-center justify-between text-xs font-mono text-editorial-muted mb-2">
              <span className="uppercase">JSON PAYLOAD:</span>
              <span>Supported: Array of SecurityEvent objects</span>
            </div>
            <textarea
              rows={12}
              value={customJson}
              onChange={e => handleJsonChange(e.target.value)}
              className="w-full font-mono text-xs p-4 rounded-lg bg-editorial-panel border border-editorial-border text-editorial-text focus:outline-none focus:border-editorial-accent transition-colors leading-relaxed"
              placeholder="Paste JSON events array here, or click 'Load Synthetic Example' above..."
            />
          </div>

          {/* Educational Note */}
          <div className="p-3.5 rounded-lg bg-editorial-panel/60 border border-editorial-border text-xs text-editorial-muted flex items-start gap-2.5">
            <Info className="w-4 h-4 text-editorial-accent shrink-0 mt-0.5" />
            <div>
              <strong className="text-editorial-text font-semibold">How SentinelEdge Analyzes Events:</strong> Each event is validated against standard security schemas, evaluated against deterministic rules (e.g. brute force, unauthorized privilege escalation), checked for statistical deviations using Median Absolute Deviation (MAD), and temporally correlated into an incident.
            </div>
          </div>

          {/* Action Row */}
          <div className="flex items-center justify-between pt-2 border-t border-editorial-border">
            <span className="text-xs text-editorial-muted font-mono">
              Zero cloud exposure — evaluated entirely through your SentinelEdge backend.
            </span>
            <button
              onClick={handleAnalyzeJson}
              disabled={isAnalyzing || (validationState !== null && !validationState.isValid)}
              className="flex items-center gap-2 px-6 py-2.5 rounded bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              <Sparkles className={`w-3.5 h-3.5 ${isAnalyzing ? 'animate-spin' : ''}`} />
              {isAnalyzing ? 'Processing Detection Pipeline...' : 'Analyze Telemetry Stream'}
            </button>
          </div>
        </div>
      )}

      {/* Tab 2: Safe Attack Simulations */}
      {activeTab === 'simulations' && (
        <div className="space-y-6">
          <div className="p-4 rounded-xl bg-editorial-surface border border-editorial-border text-xs text-editorial-muted flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-editorial-accent" />
              <span>
                <strong>Safe Simulation Lab:</strong> Generates multi-stage synthetic telemetry streams directly inside SentinelEdge without interacting with external networks.
              </span>
            </div>
            <span className="font-mono text-[10px] text-editorial-accent bg-editorial-panel px-2 py-0.5 rounded border border-editorial-border">
              6 SCENARIOS READY
            </span>
          </div>

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
                      <span className="font-mono text-[10px] uppercase text-editorial-accent font-semibold">
                        {scen.category}
                      </span>
                      <span className="font-mono text-[10px] text-editorial-muted bg-editorial-panel px-2 py-0.5 rounded border border-editorial-border">
                        {scen.event_count} EVENTS
                      </span>
                    </div>
                    <h3 className="font-bold text-base text-editorial-text">{scen.name}</h3>
                    <p className="text-xs text-editorial-muted leading-relaxed">{scen.description}</p>
                    <div className="text-[11px] font-mono text-editorial-muted pt-1">
                      Target: <strong>{scen.target_asset}</strong> {scen.target_user ? `(User: ${scen.target_user})` : ''}
                    </div>
                  </div>

                  <div className="pt-3 border-t border-editorial-border flex items-center justify-between">
                    <span className="text-[11px] font-mono text-editorial-muted">Simulates live stream</span>
                    <button
                      onClick={() => handleRunSimulation(scen.key)}
                      disabled={isRunning}
                      className="flex items-center gap-2 px-3.5 py-2 rounded bg-editorial-panel border border-editorial-border text-xs font-bold text-editorial-text hover:bg-editorial-panel/80 hover:text-editorial-accent transition-colors shadow-xs"
                    >
                      <Play className={`w-3.5 h-3.5 ${isRunning ? 'animate-spin' : 'text-editorial-accent'}`} />
                      {isRunning ? 'Injecting Stream...' : 'Run Simulation'}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
