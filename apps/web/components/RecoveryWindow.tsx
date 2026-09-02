'use client';

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
