'use client';

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
