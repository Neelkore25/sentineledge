'use client';

import React, { useEffect, useState } from 'react';
import { RotateCcw, ShieldCheck, AlertTriangle, CheckCircle2, Clock } from 'lucide-react';
import { api } from '@/lib/api';
import { RecoveryWindow } from '@/components/RecoveryWindow';

export default function RecoveryPage() {
  const [data, setData] = useState<{ overall_readiness_score: number; items: any[] } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await api.getRecoveryInventory();
        setData(res);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const score = data?.overall_readiness_score ?? 74.0;

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div className="border-b border-editorial-border pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Recovery Readiness Center</h1>
          <p className="text-xs text-editorial-muted font-mono mt-0.5">
            Coupling threat detection with disaster restoration posture, RTO/RPO SLAs, and snapshot integrity
          </p>
        </div>
        <div className="flex items-center gap-2 font-mono">
          <span className="text-xs text-editorial-muted">OVERALL READINESS:</span>
          <span className="text-base font-bold text-editorial-accent bg-editorial-accent/10 px-2.5 py-0.5 rounded border border-editorial-accent/30">
            {score.toFixed(0)}/100
          </span>
        </div>
      </div>

      {/* Signature Recovery Window */}
      <RecoveryWindow
        lastBackupHours={4.5}
        targetRpoHours={4.0}
        rpoGapHours={0.5}
        lastTestDays={22}
        readinessScore={score}
        verified={true}
        primaryWeakness="ERP Suite incremental backup test is overdue by 34 days."
      />

      {/* Asset Backup Inventory */}
      <div className="border border-editorial-border rounded-xl bg-editorial-surface p-6 shadow-xs space-y-4">
        <h3 className="font-bold text-sm text-editorial-text border-b border-editorial-border pb-3">
          Asset Backup Inventory & SLA Compliance
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-editorial-panel/60 border-b border-editorial-border text-[10px] text-editorial-muted uppercase">
              <tr>
                <th className="p-3">ASSET</th>
                <th className="p-3">BACKUP TYPE</th>
                <th className="p-3">STATUS</th>
                <th className="p-3">VERIFIED</th>
                <th className="p-3">RTO (ACTUAL/TARGET)</th>
                <th className="p-3">RPO (ACTUAL/TARGET)</th>
                <th className="p-3 text-right">READINESS</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-editorial-border text-[11px]">
              {data?.items.map(item => (
                <tr key={item.id} className="hover:bg-editorial-panel/40 transition-colors">
                  <td className="p-3 font-bold text-editorial-text">{item.asset_name}</td>
                  <td className="p-3 text-editorial-muted">{item.backup_type}</td>
                  <td className="p-3">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                      item.backup_status === 'HEALTHY' ? 'bg-status-healthy/15 text-status-healthy' : 'bg-status-warning/15 text-status-warning'
                    }`}>
                      {item.backup_status}
                    </span>
                  </td>
                  <td className="p-3">
                    {item.verified ? (
                      <span className="text-status-healthy flex items-center gap-1"><CheckCircle2 className="w-3.5 h-3.5" /> Yes</span>
                    ) : (
                      <span className="text-status-warning flex items-center gap-1"><AlertTriangle className="w-3.5 h-3.5" /> No</span>
                    )}
                  </td>
                  <td className="p-3">{item.rto_actual_hours}h / {item.rto_target_hours}h</td>
                  <td className="p-3">{item.rpo_actual_hours}h / {item.rpo_target_hours}h</td>
                  <td className="p-3 text-right font-bold text-editorial-accent">
                    {item.readiness.readiness_index.toFixed(0)}/100
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
