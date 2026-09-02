'use client';

import React from 'react';
import { RiskBreakdown as RiskType } from '@/lib/types';

interface RiskBreakdownProps {
  breakdown?: RiskType | null;
  compositeScore?: number;
  severityBand?: string;
}

export function RiskBreakdown({ breakdown, compositeScore = 78.5, severityBand = 'CRITICAL' }: RiskBreakdownProps) {
  const r_rule = breakdown?.r_rule ?? 75.0;
  const s_behavior = breakdown?.s_behavior ?? 80.0;
  const c_correlation = breakdown?.c_correlation ?? 70.0;
  const a_criticality = breakdown?.a_criticality ?? 100.0;
  const b_impact = breakdown?.b_impact ?? 85.0;
  const total = breakdown?.composite_risk_score ?? compositeScore;
  const band = breakdown?.severity_band ?? severityBand;

  const rows = [
    { label: 'RULE SIGNAL', sub: 'R_rule (Deterministic trigger)', value: r_rule, weight: 0.25, pts: 0.25 * r_rule, color: 'bg-status-warning' },
    { label: 'BEHAVIOR DEVIATION', sub: 'S_behavior (Robust Z-Score MAD)', value: s_behavior, weight: 0.20, pts: 0.20 * s_behavior, color: 'bg-status-warning' },
    { label: 'CORRELATION GROUP', sub: 'C_correlation (Temporal multi-stage)', value: c_correlation, weight: 0.20, pts: 0.20 * c_correlation, color: 'bg-editorial-accent' },
    { label: 'ASSET CRITICALITY', sub: 'A_criticality (Crown Jewel tier)', value: a_criticality, weight: 0.20, pts: 0.20 * a_criticality, color: 'bg-status-critical' },
    { label: 'BUSINESS IMPACT', sub: 'B_impact (Downtime & sensitivity)', value: b_impact, weight: 0.15, pts: 0.15 * b_impact, color: 'bg-status-critical' },
  ];

  return (
    <div className="border border-editorial-border rounded-lg bg-editorial-surface p-5 shadow-xs">
      <div className="flex items-center justify-between mb-4 border-b border-editorial-border pb-3">
        <div>
          <h3 className="font-bold text-sm text-editorial-text tracking-tight">Explainable Risk Breakdown</h3>
          <p className="text-[11px] text-editorial-muted font-mono">SentinelEdge Research Risk Model v1</p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold font-mono text-editorial-accent">{total.toFixed(1)}</div>
          <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase ${
            band === 'CRITICAL' ? 'bg-status-critical/15 text-status-critical border border-status-critical/30' :
            band === 'HIGH' ? 'bg-status-warning/15 text-status-warning border border-status-warning/30' :
            'bg-status-info/15 text-status-info border border-status-info/30'
          }`}>
            {band} SEVERITY
          </span>
        </div>
      </div>

      <div className="space-y-3 font-mono text-xs">
        {rows.map((row, i) => (
          <div key={i} className="flex flex-col gap-1 border-b border-editorial-border/40 pb-2.5">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-editorial-text">{row.label}</span>
              <div className="flex items-center gap-3">
                <span className="text-editorial-muted text-[11px]">Normalized: <strong>{row.value.toFixed(0)}/100</strong> (wt: {row.weight})</span>
                <span className="font-bold text-editorial-text w-12 text-right">+{row.pts.toFixed(2)}</span>
              </div>
            </div>
            <div className="w-full h-1.5 bg-editorial-panel rounded-full overflow-hidden">
              <div
                className={`h-full ${row.color} rounded-full transition-all duration-500`}
                style={{ width: `${row.value}%` }}
              />
            </div>
            <span className="text-[10px] text-editorial-muted font-sans">{row.sub}</span>
          </div>
        ))}

        <div className="pt-2 flex items-center justify-between font-bold text-sm">
          <span className="font-sans text-editorial-text">TOTAL WEIGHTED COMPOSITE RISK</span>
          <span className="font-mono text-editorial-accent text-base">{total.toFixed(1)} / 100</span>
        </div>
      </div>
    </div>
  );
}
