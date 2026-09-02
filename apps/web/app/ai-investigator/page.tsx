'use client';

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
