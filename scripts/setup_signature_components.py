import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 1. Incident Evidence Rail (apps/web/components/EvidenceRail.tsx)
write_file("apps/web/components/EvidenceRail.tsx", """'use client';

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
""")

# 2. Risk Breakdown Stack (apps/web/components/RiskBreakdown.tsx)
write_file("apps/web/components/RiskBreakdown.tsx", """'use client';

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
""")

# 3. Recovery Window (apps/web/components/RecoveryWindow.tsx)
write_file("apps/web/components/RecoveryWindow.tsx", """'use client';

import React from 'react';
import { RotateCcw, AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

interface RecoveryWindowProps {
  lastBackupHours?: number;
  targetRpoHours?: number;
  rpoGapHours?: number;
  lastTestDays?: number;
  readinessScore?: number;
  verified?: boolean;
  primaryWeakness?: string;
}

export function RecoveryWindow({
  lastBackupHours = 18.0,
  targetRpoHours = 4.0,
  rpoGapHours = 14.0,
  lastTestDays = 47,
  readinessScore = 61.0,
  verified = false,
  primaryWeakness = 'Primary weakness: snapshot verification is overdue and RPO gap is 14h.'
}: RecoveryWindowProps) {
  return (
    <div className="border border-editorial-border rounded-lg bg-editorial-surface p-5 shadow-xs">
      <div className="flex items-center justify-between mb-4 border-b border-editorial-border pb-3">
        <div className="flex items-center gap-2">
          <RotateCcw className="w-4 h-4 text-editorial-accent" />
          <h3 className="font-bold text-sm text-editorial-text tracking-tight">The Recovery Window</h3>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-mono text-editorial-muted">READINESS:</span>
          <span className="font-mono font-bold text-base text-editorial-accent bg-editorial-accent/10 px-2 py-0.5 rounded border border-editorial-accent/30">
            {readinessScore.toFixed(0)}/100
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4 font-mono text-xs">
        <div className="p-2.5 rounded bg-editorial-panel border border-editorial-border">
          <div className="text-[10px] text-editorial-muted uppercase">LAST BACKUP</div>
          <div className="text-base font-bold text-editorial-text mt-0.5">{lastBackupHours.toFixed(1)}h ago</div>
          <div className="text-[10px] flex items-center gap-1 mt-1 text-editorial-muted">
            {verified ? <CheckCircle2 className="w-3 h-3 text-status-healthy" /> : <AlertTriangle className="w-3 h-3 text-status-warning" />}
            {verified ? 'Verified' : 'Unverified'}
          </div>
        </div>

        <div className="p-2.5 rounded bg-editorial-panel border border-editorial-border">
          <div className="text-[10px] text-editorial-muted uppercase">TARGET RPO</div>
          <div className="text-base font-bold text-editorial-text mt-0.5">{targetRpoHours.toFixed(1)}h</div>
          <div className="text-[10px] text-editorial-muted mt-1">SLA Tolerance</div>
        </div>

        <div className="p-2.5 rounded bg-editorial-panel border border-editorial-border">
          <div className="text-[10px] text-editorial-muted uppercase">CURRENT GAP</div>
          <div className={`text-base font-bold mt-0.5 ${rpoGapHours > 0 ? 'text-status-critical' : 'text-status-healthy'}`}>
            {rpoGapHours > 0 ? `+${rpoGapHours.toFixed(1)}h` : '0.0h'}
          </div>
          <div className="text-[10px] text-editorial-muted mt-1">
            {rpoGapHours > 0 ? 'Exceeds RPO SLA' : 'Within Target'}
          </div>
        </div>

        <div className="p-2.5 rounded bg-editorial-panel border border-editorial-border">
          <div className="text-[10px] text-editorial-muted uppercase">RECOVERY TEST</div>
          <div className="text-base font-bold text-editorial-text mt-0.5">{lastTestDays} days ago</div>
          <div className="text-[10px] text-status-warning mt-1">
            {lastTestDays > 30 ? 'Drill Overdue' : 'Drill Current'}
          </div>
        </div>
      </div>

      <div className="p-3 rounded bg-editorial-panel/80 border border-editorial-border text-xs flex items-start gap-2.5">
        <ShieldAlert className="w-4 h-4 text-editorial-accent shrink-0 mt-0.5" />
        <div>
          <span className="font-semibold text-editorial-text">Recovery Risk Assessment: </span>
          <span className="text-editorial-muted">{primaryWeakness}</span>
        </div>
      </div>
    </div>
  );
}
""")

# 4. Human Response Drawer / Action Modal (apps/web/components/HumanResponseDrawer.tsx)
write_file("apps/web/components/HumanResponseDrawer.tsx", """'use client';

import React, { useState } from 'react';
import { ShieldCheck, Lock, UserX, RefreshCw, X, AlertCircle } from 'lucide-react';
import { api } from '@/lib/api';
import { useApp } from '@/lib/store';

interface HumanResponseDrawerProps {
  incidentId: string;
  target: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

const actionOptions = [
  { id: 'SIMULATE_ACCOUNT_LOCK', name: 'Lock User Account', icon: UserX, desc: 'Temporarily disable authentication session and mandate password reset.' },
  { id: 'SIMULATE_SESSION_REVOCATION', name: 'Revoke All Active Sessions', icon: Lock, desc: 'Invalidate OAuth2 bearer tokens and force immediate re-authentication.' },
  { id: 'SIMULATE_IP_BLOCK', name: 'Block Inbound Source IP', icon: ShieldCheck, desc: 'Apply edge firewall drop rule for offending IP address.' },
  { id: 'INITIATE_BACKUP_RESTORE_DRILL', name: 'Initiate Restore Simulation', icon: RefreshCw, desc: 'Trigger sandbox restore drill on affected database asset.' }
];

export function HumanResponseDrawer({ incidentId, target, isOpen, onClose, onSuccess }: HumanResponseDrawerProps) {
  const { userRole, triggerRefresh } = useApp();
  const [selectedAction, setSelectedAction] = useState(actionOptions[0].id);
  const [reason, setReason] = useState('Correlated security anomaly confirmed by security analyst.');
  const [submitting, setSubmitting] = useState(false);
  const [confirmed, setConfirmed] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      await api.respondToIncident(incidentId, selectedAction, reason, target);
      setConfirmed(true);
      triggerRefresh();
      setTimeout(() => {
        onSuccess();
        onClose();
      }, 1200);
    } catch (err) {
      alert(`Action failed: ${err}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
      <div className="w-full max-w-lg bg-editorial-surface border border-editorial-border rounded-lg shadow-2xl overflow-hidden animate-in fade-in zoom-in-95">
        <div className="p-4 border-b border-editorial-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-editorial-accent" />
            <h3 className="font-bold text-sm text-editorial-text">Human-in-the-Loop Response Action</h3>
          </div>
          <button onClick={onClose} className="p-1 text-editorial-muted hover:text-editorial-text rounded">
            <X className="w-4 h-4" />
          </button>
        </div>

        {confirmed ? (
          <div className="p-8 text-center space-y-3">
            <div className="w-12 h-12 rounded-full bg-status-healthy/20 border border-status-healthy text-status-healthy flex items-center justify-center mx-auto">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h4 className="font-bold text-base text-editorial-text">Action Executed & Logged</h4>
            <p className="text-xs text-editorial-muted">Incident status updated to MITIGATED. Tamper-evident record committed to Audit Trail.</p>
          </div>
        ) : (
          <div className="p-5 space-y-4 text-xs">
            <div className="p-3 rounded bg-editorial-panel border border-editorial-border space-y-1">
              <div className="flex justify-between text-editorial-muted font-mono">
                <span>INCIDENT: <strong>#{incidentId}</strong></span>
                <span>ACTOR: <strong>{userRole}</strong></span>
              </div>
              <div className="text-editorial-text font-medium">Target Resource: <span className="font-mono text-editorial-accent">{target}</span></div>
            </div>

            <div className="space-y-2">
              <label className="font-semibold text-editorial-text">Select Remediation Action:</label>
              <div className="space-y-1.5">
                {actionOptions.map(opt => {
                  const Icon = opt.icon;
                  return (
                    <button
                      key={opt.id}
                      type="button"
                      onClick={() => setSelectedAction(opt.id)}
                      className={`w-full p-2.5 rounded border text-left flex items-start gap-3 transition-colors ${
                        selectedAction === opt.id
                          ? 'border-editorial-accent bg-editorial-panel text-editorial-text shadow-xs'
                          : 'border-editorial-border bg-editorial-surface text-editorial-muted hover:bg-editorial-panel/50'
                      }`}
                    >
                      <Icon className="w-4 h-4 text-editorial-accent mt-0.5 shrink-0" />
                      <div>
                        <div className="font-bold text-editorial-text">{opt.name}</div>
                        <div className="text-[11px] text-editorial-muted">{opt.desc}</div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="font-semibold text-editorial-text">Operational Justification / Reason:</label>
              <textarea
                value={reason}
                onChange={e => setReason(e.target.value)}
                rows={2}
                className="w-full p-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text text-xs focus:outline-none focus:border-editorial-accent"
              />
            </div>

            <div className="p-2.5 rounded bg-editorial-panel/60 border border-editorial-border text-[11px] text-editorial-muted flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-editorial-accent shrink-0" />
              <span>Simulated response changes incident status and permanently writes state changes to <strong>/audit</strong>.</span>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-editorial-border">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded text-editorial-muted hover:bg-editorial-panel border border-editorial-border transition-colors font-medium"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSubmit}
                disabled={submitting}
                className="px-4 py-2 rounded bg-editorial-accent text-white font-bold hover:opacity-90 transition-opacity shadow-xs"
              >
                {submitting ? 'Executing...' : 'Confirm Response Action'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
""")

print("Phase 3 signature components created successfully!")
