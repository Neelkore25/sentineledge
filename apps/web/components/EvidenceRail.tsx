'use client';

import React from 'react';
import { Eye, Network, Gauge, Sparkles, AlertOctagon, CheckCircle2 } from 'lucide-react';

interface EvidenceRailProps {
  currentStage?: 'observed' | 'correlated' | 'scored' | 'explained' | 'prioritized' | 'responded';
  eventCount?: number;
  riskScore?: number;
  status?: string;
}

const stages = [
  { id: 'observed', label: 'Observed', subtext: 'Raw Telemetry Ingest', icon: Eye },
  { id: 'correlated', label: 'Correlated', subtext: 'Sliding Window Grouping', icon: Network },
  { id: 'scored', label: 'Scored', subtext: 'Explainable Risk Model v1', icon: Gauge },
  { id: 'explained', label: 'Explained', subtext: 'Evidence-Grounded AI', icon: Sparkles },
  { id: 'prioritized', label: 'Prioritized', subtext: 'Business & Recovery Context', icon: AlertOctagon },
  { id: 'responded', label: 'Responded', subtext: 'Human-in-the-Loop Audit', icon: CheckCircle2 },
];

export function EvidenceRail({ currentStage = 'explained', eventCount = 12, riskScore = 82, status = 'OPEN' }: EvidenceRailProps) {
  const getStageIndex = (stage: string) => {
    return stages.findIndex(s => s.id === stage);
  };

  const currentIndex = status === 'MITIGATED' || status === 'RESOLVED' ? 5 : getStageIndex(currentStage);

  return (
    <div className="border border-editorial-border rounded-lg bg-editorial-surface p-4 shadow-xs">
      <div className="flex items-center justify-between mb-3 border-b border-editorial-border pb-2">
        <span className="text-[11px] font-mono uppercase tracking-wider text-editorial-muted">
          INCIDENT EVIDENCE PIPELINE RAIL
        </span>
        <span className="text-xs font-mono text-editorial-accent bg-editorial-panel px-2 py-0.5 rounded border border-editorial-border">
          {status === 'MITIGATED' ? 'CONTAINMENT APPLIED' : `ACTIVE STAGE: ${stages[currentIndex]?.label.toUpperCase()}`}
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-6 gap-2">
        {stages.map((stage, idx) => {
          const Icon = stage.icon;
          const isPassed = idx <= currentIndex;
          const isCurrent = idx === currentIndex;

          return (
            <div
              key={stage.id}
              className={`p-3 rounded border transition-all ${
                isCurrent
                  ? 'bg-editorial-panel border-editorial-accent text-editorial-text shadow-xs'
                  : isPassed
                  ? 'bg-editorial-surface border-editorial-border text-editorial-text'
                  : 'bg-editorial-panel/30 border-dashed border-editorial-border text-editorial-muted opacity-60'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <Icon className={`w-4 h-4 ${isCurrent ? 'text-editorial-accent' : isPassed ? 'text-status-healthy' : 'text-editorial-muted'}`} />
                <span className="text-[10px] font-mono text-editorial-muted">0{idx + 1}</span>
              </div>
              <div className="font-semibold text-xs text-editorial-text leading-tight">{stage.label}</div>
              <div className="text-[10px] text-editorial-muted truncate mt-0.5">{stage.subtext}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
