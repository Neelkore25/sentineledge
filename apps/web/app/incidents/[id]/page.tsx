'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import {
  ArrowLeft,
  Sparkles,
  ShieldCheck,
  Layers,
  ChevronDown,
  ChevronUp
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
  const [showTechnicalMath, setShowTechnicalMath] = useState(false);

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
    } catch (err: any) {
      alert(`AI investigation failed: ${err.message || err}`);
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
            <Sparkles className={`w-3.5 h-3.5 text-editorial-accent ${aiLoading ? 'animate-spin' : ''}`} />
            {aiLoading ? 'Analyzing Evidence...' : 'Re-Run AI Assessment'}
          </button>
          <button
            onClick={() => setIsResponseOpen(true)}
            className="flex items-center gap-2 px-4 py-2 rounded bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity"
          >
            <ShieldCheck className="w-4 h-4" />
            Record Analyst Response
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

            <div className="space-y-4 text-xs">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono uppercase text-editorial-accent font-bold px-1.5 py-0.5 rounded bg-editorial-accent/10 border border-editorial-accent/30">
                    AI HYPOTHESIS
                  </span>
                  <span className="text-[11px] text-editorial-muted font-mono">(Probabilistic Assessment)</span>
                </div>
                <p className="font-medium text-editorial-text mt-0.5">
                  {incident.ai_hypothesis || 'Probable credential compromise followed by administrative elevation.'}
                </p>
              </div>

              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono uppercase text-status-healthy font-bold px-1.5 py-0.5 rounded bg-status-healthy/10 border border-status-healthy/30">
                    OBSERVED EVIDENCE
                  </span>
                  <span className="text-[11px] text-editorial-muted font-mono">(Direct Telemetry Facts)</span>
                </div>
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

          {/* Expandable Technical Math Accordion */}
          <div className="border border-editorial-border rounded-xl bg-editorial-surface p-4 shadow-xs text-xs space-y-3">
            <button
              onClick={() => setShowTechnicalMath(!showTechnicalMath)}
              className="w-full flex items-center justify-between font-bold text-editorial-text hover:text-editorial-accent transition-colors"
            >
              <span>Technical Formula & Sub-Score Details</span>
              {showTechnicalMath ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>

            {showTechnicalMath && (
              <div className="pt-2 border-t border-editorial-border space-y-2 font-mono text-[11px] text-editorial-muted animate-in fade-in">
                <div className="p-2 rounded bg-editorial-panel border border-editorial-border">
                  <strong className="text-editorial-text">Formula:</strong>
                  <div className="mt-1">Risk = 0.25·R + 0.20·S + 0.20·C + 0.20·A + 0.15·B</div>
                </div>
                <ul className="space-y-1 list-disc list-inside">
                  <li>R_rule: {incident.risk_breakdown?.r_rule ?? 75}/100</li>
                  <li>S_behavior (MAD): {incident.risk_breakdown?.s_behavior ?? 68}/100</li>
                  <li>C_correlation: {incident.risk_breakdown?.c_correlation ?? 80}/100</li>
                  <li>A_criticality: {incident.risk_breakdown?.a_criticality ?? 100}/100</li>
                  <li>B_impact: {incident.risk_breakdown?.b_impact ?? 88}/100</li>
                </ul>
              </div>
            )}
          </div>

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
