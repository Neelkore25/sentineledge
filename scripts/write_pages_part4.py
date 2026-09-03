import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 12. AI Investigator Studio Page (apps/web/app/ai-investigator/page.tsx)
write_file("apps/web/app/ai-investigator/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import { Sparkles, Shield, AlertTriangle, Play, CheckCircle2, Layers } from 'lucide-react';
import { api } from '@/lib/api';
import { Incident } from '@/lib/types';

export default function AIInvestigatorPage() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [selectedId, setSelectedId] = useState<string>('');
  const [analysis, setAnalysis] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getIncidents();
        setIncidents(data);
        if (data.length > 0) {
          setSelectedId(data[0].id);
        }
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, []);

  const handleInvestigate = async () => {
    if (!selectedId) return;
    try {
      setLoading(true);
      const res = await api.investigateIncidentAI(selectedId);
      setAnalysis(res);
    } catch (err) {
      alert(`Investigation failed: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  const currentInc = incidents.find(i => i.id === selectedId);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Evidence-Grounded AI Investigator</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Advisory incident consultation strictly grounded in supplied telemetry IDs, baseline metrics, and asset context
        </p>
      </div>

      <div className="border border-editorial-border rounded-xl bg-editorial-surface p-5 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3 flex-1">
          <span className="text-xs font-mono text-editorial-muted uppercase">SELECT INCIDENT:</span>
          <select
            value={selectedId}
            onChange={e => setSelectedId(e.target.value)}
            className="p-2 rounded bg-editorial-panel border border-editorial-border text-xs text-editorial-text font-mono focus:outline-none flex-1 max-w-md"
          >
            {incidents.map(inc => (
              <option key={inc.id} value={inc.id}>
                #{inc.id} — {inc.title} ({inc.severity})
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={handleInvestigate}
          disabled={loading || !selectedId}
          className="flex items-center gap-2 px-5 py-2.5 rounded bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity"
        >
          <Sparkles className="w-4 h-4" />
          {loading ? 'Synthesizing Evidence...' : 'Run Grounded AI Investigation'}
        </button>
      </div>

      {/* Analysis Output */}
      {analysis ? (
        <div className="border border-editorial-border rounded-xl bg-editorial-surface p-6 shadow-xs space-y-6 animate-in fade-in">
          <div className="flex items-center justify-between border-b border-editorial-border pb-3">
            <div>
              <span className="font-mono text-[10px] uppercase text-editorial-accent font-semibold">{analysis.mode}</span>
              <h3 className="font-bold text-base text-editorial-text mt-0.5">Investigation Findings for #{selectedId}</h3>
            </div>
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-editorial-panel border border-editorial-border text-editorial-muted">
              CONFIDENCE: {(analysis.confidence_score * 100).toFixed(0)}%
            </span>
          </div>

          <div className="space-y-4 text-xs">
            <div>
              <span className="font-mono text-[10px] uppercase text-editorial-muted font-bold">SUMMARY</span>
              <p className="text-editorial-text leading-relaxed mt-1">{analysis.summary}</p>
            </div>

            <div>
              <span className="font-mono text-[10px] uppercase text-editorial-muted font-bold">PRIMARY HYPOTHESIS</span>
              <p className="font-semibold text-editorial-text leading-relaxed mt-1 p-3 rounded bg-editorial-panel border border-editorial-border">
                {analysis.primary_hypothesis}
              </p>
            </div>

            <div>
              <span className="font-mono text-[10px] uppercase text-editorial-muted font-bold">EVIDENCE CITATIONS (GROUNDED LOGS)</span>
              <ul className="space-y-1.5 mt-1 font-mono text-[11px] text-editorial-text">
                {analysis.evidence_citations?.map((c: string, i: number) => (
                  <li key={i} className="p-2 rounded bg-editorial-panel/80 border border-editorial-border">
                    • {c}
                  </li>
                ))}
              </ul>
            </div>

            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <span className="font-mono text-[10px] uppercase text-editorial-muted font-bold">ALTERNATIVE EXPLANATION</span>
                <p className="text-editorial-muted mt-1 leading-relaxed">{analysis.alternative_explanation}</p>
              </div>
              <div>
                <span className="font-mono text-[10px] uppercase text-editorial-muted font-bold">MISSING EVIDENCE</span>
                <p className="text-editorial-muted mt-1 leading-relaxed">{analysis.missing_evidence}</p>
              </div>
            </div>

            {analysis.recommended_actions && (
              <div className="p-4 rounded bg-editorial-accent/10 border border-editorial-accent/30 space-y-2">
                <span className="font-bold font-mono text-[10px] text-editorial-accent uppercase">RECOMMENDED HUMAN ACTIONS:</span>
                <ul className="space-y-1 font-semibold text-xs text-editorial-text">
                  {analysis.recommended_actions.map((act: string, idx: number) => (
                    <li key={idx}>✓ {act}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="border border-editorial-border border-dashed rounded-xl p-12 text-center text-xs text-editorial-muted space-y-2">
          <Sparkles className="w-8 h-8 text-editorial-accent mx-auto" />
          <p className="font-medium text-editorial-text">Select an incident and click 'Run Grounded AI Investigation'.</p>
          <p>The AI receives strict JSON evidence and strictly adheres to verifiable citations.</p>
        </div>
      )}
    </div>
  );
}
""")

# 13. Reports Page (apps/web/app/reports/page.tsx)
write_file("apps/web/app/reports/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import { FileText, Printer, Download, Shield } from 'lucide-react';
import { api } from '@/lib/api';
import { Incident } from '@/lib/types';

export default function ReportsPage() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getIncidents();
        setIncidents(data);
        if (data.length > 0) setSelectedIncident(data[0]);
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, []);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-editorial-border pb-4 print:hidden">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Incident & Post-Mortem Reports</h1>
          <p className="text-xs text-editorial-muted font-mono mt-0.5">
            Exportable executive and technical post-incident review documents
          </p>
        </div>
        <button
          onClick={handlePrint}
          className="flex items-center gap-2 px-4 py-2 rounded bg-editorial-panel border border-editorial-border text-xs font-bold text-editorial-text hover:bg-editorial-panel/80 transition-colors"
        >
          <Printer className="w-4 h-4" /> Print / Save as PDF
        </button>
      </div>

      {selectedIncident && (
        <div className="border border-editorial-border rounded-xl bg-editorial-surface p-8 shadow-xs space-y-6 text-xs print:border-none print:shadow-none">
          <div className="flex items-center justify-between border-b border-editorial-border pb-4">
            <div>
              <div className="text-[10px] font-mono text-editorial-muted uppercase">SENTINELEDGE RESILIENCE PLATFORM</div>
              <h2 className="text-xl font-bold text-editorial-text mt-1">{selectedIncident.title}</h2>
              <div className="text-xs font-mono text-editorial-muted mt-0.5">Incident ID: #{selectedIncident.id} • Detected: {selectedIncident.detected_at.slice(0, 19).replace('T', ' ')}</div>
            </div>
            <div className="text-right font-mono">
              <span className="text-xs px-2 py-0.5 rounded font-bold uppercase bg-editorial-panel border border-editorial-border text-editorial-accent">
                {selectedIncident.severity} SEVERITY ({selectedIncident.risk_score}/100)
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-[11px]">
            <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
              <span className="text-[10px] text-editorial-muted uppercase">AFFECTED ASSET</span>
              <div className="font-bold text-editorial-text mt-0.5">{selectedIncident.affected_asset}</div>
            </div>
            <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
              <span className="text-[10px] text-editorial-muted uppercase">AFFECTED IDENTITY</span>
              <div className="font-bold text-editorial-text mt-0.5">{selectedIncident.affected_user || 'System'}</div>
            </div>
            <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
              <span className="text-[10px] text-editorial-muted uppercase">BUSINESS IMPACT</span>
              <div className="font-bold text-editorial-accent mt-0.5">{selectedIncident.business_impact}</div>
            </div>
            <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
              <span className="text-[10px] text-editorial-muted uppercase">STATUS</span>
              <div className="font-bold text-status-healthy mt-0.5">{selectedIncident.status}</div>
            </div>
          </div>

          <div className="space-y-2">
            <h3 className="font-bold text-xs text-editorial-text font-mono uppercase">Executive Summary</h3>
            <p className="text-editorial-muted leading-relaxed">
              {selectedIncident.ai_summary || selectedIncident.description}
            </p>
          </div>

          <div className="space-y-2">
            <h3 className="font-bold text-xs text-editorial-text font-mono uppercase">Primary Technical Hypothesis</h3>
            <p className="text-editorial-text leading-relaxed p-3 rounded bg-editorial-panel border border-editorial-border">
              {selectedIncident.ai_hypothesis || 'Multi-stage anomalous authentication burst triggering credential compromise alert.'}
            </p>
          </div>

          <div className="space-y-2">
            <h3 className="font-bold text-xs text-editorial-text font-mono uppercase">Applied Remediation & Recommendations</h3>
            <p className="text-editorial-muted leading-relaxed">
              {selectedIncident.recommended_action || 'Simulate session revocation and force multi-factor authentication re-verification.'}
            </p>
          </div>

          <div className="pt-6 border-t border-editorial-border flex items-center justify-between text-[11px] font-mono text-editorial-muted">
            <span>SentinelEdge Explainable AI Platform</span>
            <span>Generated from Grounded Telemetry Logs</span>
          </div>
        </div>
      )}
    </div>
  );
}
""")

# 14. Audit Log Page (apps/web/app/audit/page.tsx)
write_file("apps/web/app/audit/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import { History, ShieldCheck, Lock, UserX, RefreshCw } from 'lucide-react';
import { api } from '@/lib/api';
import { AuditLogItem } from '@/lib/types';
import { useApp } from '@/lib/store';

export default function AuditPage() {
  const { refreshTrigger } = useApp();
  const [logs, setLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await api.getAuditLogs();
        setLogs(data);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [refreshTrigger]);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Immutable Audit Ledger</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Tamper-evident log of all human-in-the-loop response actions, status transitions, and system events
        </p>
      </div>

      <div className="border border-editorial-border rounded-lg bg-editorial-surface shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-editorial-panel/60 border-b border-editorial-border text-[10px] text-editorial-muted uppercase">
              <tr>
                <th className="p-3">LOG ID</th>
                <th className="p-3">TIMESTAMP</th>
                <th className="p-3">ACTOR & ROLE</th>
                <th className="p-3">ACTION</th>
                <th className="p-3">TARGET RESOURCE</th>
                <th className="p-3">REASON / JUSTIFICATION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-editorial-border text-[11px]">
              {logs.map(log => (
                <tr key={log.id} className="hover:bg-editorial-panel/40 transition-colors">
                  <td className="p-3 font-bold text-editorial-text">{log.id}</td>
                  <td className="p-3 text-editorial-muted">{log.timestamp.slice(11, 19)}</td>
                  <td className="p-3">
                    <span className="font-bold text-editorial-text">{log.actor}</span>
                    <div className="text-[10px] text-editorial-muted">({log.role})</div>
                  </td>
                  <td className="p-3">
                    <span className="font-bold text-editorial-accent bg-editorial-panel px-1.5 py-0.5 rounded border border-editorial-border">
                      {log.action}
                    </span>
                  </td>
                  <td className="p-3 text-editorial-text max-w-[200px] truncate">{log.resource}</td>
                  <td className="p-3 text-editorial-muted max-w-[250px] truncate font-sans text-xs">{log.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
""")

# 15. Research Hub Page (apps/web/app/research/page.tsx)
write_file("apps/web/app/research/page.tsx", """import React from 'react';
import { BookOpen, Layers, CheckCircle2, AlertTriangle, Cpu } from 'lucide-react';

export default function ResearchPage() {
  return (
    <div className="space-y-8 max-w-4xl mx-auto py-4">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Research Methodology & Evaluation</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Academic foundations, hypotheses testing framework, and comparative benchmarking for SME cyber resilience
        </p>
      </div>

      {/* Core Research Question */}
      <section className="p-6 rounded-xl border border-editorial-accent bg-editorial-surface shadow-xs space-y-3">
        <span className="text-[10px] font-mono uppercase text-editorial-accent font-bold">CORE RESEARCH QUESTION</span>
        <blockquote className="text-base font-semibold text-editorial-text italic">
          "Can a lightweight, explainable AI-assisted cybersecurity platform improve incident prioritization
          and recovery readiness for resource-constrained SMEs compared with conventional rule-based detection?"
        </blockquote>
      </section>

      {/* Formal Hypotheses */}
      <section className="space-y-4">
        <h2 className="text-sm font-bold font-mono text-editorial-text uppercase">Evaluation Hypotheses</h2>
        <div className="grid gap-4">
          <div className="p-5 rounded-lg border border-editorial-border bg-editorial-surface space-y-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-editorial-accent bg-editorial-panel px-2 py-0.5 rounded border border-editorial-border">H1</span>
              <h3 className="font-bold text-sm text-editorial-text">Hybrid Multi-Layer Detection Superiority</h3>
            </div>
            <p className="text-xs text-editorial-muted leading-relaxed">
              Combining deterministic rules, statistical Robust Z-Score (MAD) behavioral baselines, and temporal event correlation
              significantly reduces false-positive alert fatigue compared to isolated rule-only alerting.
            </p>
          </div>

          <div className="p-5 rounded-lg border border-editorial-border bg-editorial-surface space-y-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-editorial-accent bg-editorial-panel px-2 py-0.5 rounded border border-editorial-border">H2</span>
              <h3 className="font-bold text-sm text-editorial-text">Comprehension via Evidence-Grounded AI</h3>
            </div>
            <p className="text-xs text-editorial-muted leading-relaxed">
              Enforcing strict evidence packaging (citable telemetry IDs, baseline deviations, and explicit uncertainty boundaries)
              accelerates incident comprehension without hallucinated technical artifacts.
            </p>
          </div>

          <div className="p-5 rounded-lg border border-editorial-border bg-editorial-surface space-y-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-editorial-accent bg-editorial-panel px-2 py-0.5 rounded border border-editorial-border">H3</span>
              <h3 className="font-bold text-sm text-editorial-text">Coupled Recovery & Business Impact Prioritization</h3>
            </div>
            <p className="text-xs text-editorial-muted leading-relaxed">
              Evaluating technical threat severity alongside asset downtime costs and RPO/RTO disaster recovery compliance
              produces more actionable business prioritization than technical CVE severity alone.
            </p>
          </div>
        </div>
      </section>

      {/* Comparative Model Architecture */}
      <section className="border border-editorial-border rounded-xl bg-editorial-surface p-6 space-y-4">
        <h2 className="text-sm font-bold font-mono text-editorial-text uppercase">Architectural Comparison</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-editorial-panel/60 border-b border-editorial-border text-[10px] text-editorial-muted uppercase">
              <tr>
                <th className="p-2.5">DIMENSION</th>
                <th className="p-2.5">RULE-ONLY BASELINE</th>
                <th className="p-2.5">GENERIC SIEM CLONE</th>
                <th className="p-2.5 text-editorial-accent">SENTINELEDGE PLATFORM</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-editorial-border text-[11px]">
              <tr>
                <td className="p-2.5 font-bold">Detection</td>
                <td className="p-2.5 text-editorial-muted">Static thresholds</td>
                <td className="p-2.5 text-editorial-muted">Heavy queries</td>
                <td className="p-2.5 font-bold text-editorial-text">Rules + Robust Z-Score MAD + Sliding Correlation</td>
              </tr>
              <tr>
                <td className="p-2.5 font-bold">Explainability</td>
                <td className="p-2.5 text-editorial-muted">None (Boolean flag)</td>
                <td className="p-2.5 text-editorial-muted">Opaque logs</td>
                <td className="p-2.5 font-bold text-editorial-text">Evidence Rail + 5-Factor Risk Stack</td>
              </tr>
              <tr>
                <td className="p-2.5 font-bold">Recovery Integration</td>
                <td className="p-2.5 text-editorial-muted">Disconnected</td>
                <td className="p-2.5 text-editorial-muted">Disconnected</td>
                <td className="p-2.5 font-bold text-editorial-accent">Integrated Recovery Window (RPO/RTO SLA)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
""")

# 16. System Settings Page (apps/web/app/settings/page.tsx)
write_file("apps/web/app/settings/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import { Sliders, Save, CheckCircle2 } from 'lucide-react';
import { api } from '@/lib/api';

export default function SettingsPage() {
  const [windowMins, setWindowMins] = useState('30');
  const [bruteThreshold, setBruteThreshold] = useState('5');
  const [aiProvider, setAiProvider] = useState('local');
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await api.getSettings();
        if (data.correlation_window_minutes) setWindowMins(data.correlation_window_minutes.value);
        if (data.brute_force_threshold) setBruteThreshold(data.brute_force_threshold.value);
        if (data.ai_provider) setAiProvider(data.ai_provider.value);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await Promise.all([
        api.updateSetting('correlation_window_minutes', windowMins),
        api.updateSetting('brute_force_threshold', bruteThreshold),
        api.updateSetting('ai_provider', aiProvider)
      ]);
      setSaved(true);
      setTimeout(() => setSaved(false), 2500);
    } catch (err) {
      alert(`Save failed: ${err}`);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">System Settings</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Configure detection thresholds, AI engine provider, and temporal correlation parameters
        </p>
      </div>

      <form onSubmit={handleSave} className="border border-editorial-border rounded-xl bg-editorial-surface p-6 shadow-xs space-y-6">
        <div className="space-y-4 text-xs">
          <div className="space-y-1.5">
            <label className="font-bold text-editorial-text font-mono flex items-center justify-between">
              <span>TEMPORAL CORRELATION WINDOW (MINUTES)</span>
              <span className="text-editorial-accent">{windowMins} min</span>
            </label>
            <p className="text-editorial-muted text-[11px]">
              Sliding time window used by Detection Engine Layer 3 to group security events by entity and map MITRE attack stages.
            </p>
            <input
              type="number"
              min={5}
              max={180}
              value={windowMins}
              onChange={e => setWindowMins(e.target.value)}
              className="w-full p-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text font-mono text-xs focus:outline-none focus:border-editorial-accent"
            />
          </div>

          <div className="space-y-1.5 pt-3 border-t border-editorial-border">
            <label className="font-bold text-editorial-text font-mono">
              BRUTE FORCE THRESHOLD (FAILED ATTEMPTS)
            </label>
            <p className="text-editorial-muted text-[11px]">
              Minimum authentication failures within the correlation window required to trigger RULE_AUTH_BRUTE_FORCE_001.
            </p>
            <input
              type="number"
              min={2}
              max={50}
              value={bruteThreshold}
              onChange={e => setBruteThreshold(e.target.value)}
              className="w-full p-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text font-mono text-xs focus:outline-none focus:border-editorial-accent"
            />
          </div>

          <div className="space-y-1.5 pt-3 border-t border-editorial-border">
            <label className="font-bold text-editorial-text font-mono">
              AI INVESTIGATION PROVIDER
            </label>
            <p className="text-editorial-muted text-[11px]">
              Select AI model provider for advisory incident analysis. Falls back automatically to deterministic local mode.
            </p>
            <select
              value={aiProvider}
              onChange={e => setAiProvider(e.target.value)}
              className="w-full p-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text font-mono text-xs focus:outline-none focus:border-editorial-accent"
            >
              <option value="local">Local Research Assistant (Deterministic Evidence Grounded)</option>
              <option value="openai">OpenAI (GPT-4o-mini / GPT-4o)</option>
              <option value="gemini">Google Gemini 1.5 / 2.0</option>
              <option value="anthropic">Anthropic Claude 3.5</option>
            </select>
          </div>
        </div>

        <div className="pt-4 border-t border-editorial-border flex items-center justify-between">
          {saved ? (
            <span className="text-status-healthy text-xs font-mono flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" /> Settings persisted to database.
            </span>
          ) : <span />}

          <button
            type="submit"
            className="flex items-center gap-2 px-5 py-2.5 rounded bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity"
          >
            <Save className="w-4 h-4" /> Save System Settings
          </button>
        </div>
      </form>
    </div>
  );
}
""")

print("Part 4 pages created successfully!")
