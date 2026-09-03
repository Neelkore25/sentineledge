import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 9. Detection Rules Page (apps/web/app/detections/page.tsx)
write_file("apps/web/app/detections/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import { Binary, Shield, ToggleLeft, ToggleRight, CheckCircle2, Sliders } from 'lucide-react';
import { api } from '@/lib/api';

export default function DetectionsPage() {
  const [rules, setRules] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getRules();
        setRules(data);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const handleToggle = async (ruleId: string, current: boolean) => {
    try {
      await api.toggleRule(ruleId, !current);
      setRules(prev => prev.map(r => r.rule_id === ruleId ? { ...r, enabled: !current } : r));
    } catch (e) {
      alert(`Toggle failed: ${e}`);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Detection Rules Registry</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Deterministic Layer 1 detection rules powering the SentinelEdge hybrid pipeline
        </p>
      </div>

      <div className="grid gap-4">
        {rules.map(rule => (
          <div
            key={rule.rule_id}
            className={`border rounded-lg p-5 shadow-xs transition-all ${
              rule.enabled ? 'bg-editorial-surface border-editorial-border' : 'bg-editorial-panel/40 border-editorial-border/60 opacity-70'
            }`}
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-editorial-border/60 pb-3">
              <div className="flex items-center gap-3">
                <Binary className="w-5 h-5 text-editorial-accent" />
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-editorial-text">{rule.name}</span>
                    <span className="font-mono text-[10px] text-editorial-muted bg-editorial-panel px-1.5 py-0.2 rounded border border-editorial-border">
                      {rule.rule_id}
                    </span>
                  </div>
                  <div className="text-[11px] font-mono text-editorial-muted">{rule.attack_category}</div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <span className={`font-mono text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                  rule.severity === 'CRITICAL' ? 'bg-status-critical/15 text-status-critical' :
                  rule.severity === 'HIGH' ? 'bg-status-warning/15 text-status-warning' :
                  'bg-status-info/15 text-status-info'
                }`}>
                  {rule.severity} (R_rule: {rule.r_rule}/100)
                </span>

                <button
                  onClick={() => handleToggle(rule.rule_id, rule.enabled)}
                  className="flex items-center gap-1.5 text-xs font-mono font-medium px-2.5 py-1 rounded bg-editorial-panel border border-editorial-border hover:bg-editorial-panel/80 text-editorial-text"
                >
                  {rule.enabled ? <ToggleRight className="w-4 h-4 text-status-healthy" /> : <ToggleLeft className="w-4 h-4 text-editorial-muted" />}
                  {rule.enabled ? 'ACTIVE' : 'DISABLED'}
                </button>
              </div>
            </div>

            <div className="pt-3 text-xs text-editorial-muted flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <p>{rule.description}</p>
              {rule.threshold !== undefined && rule.threshold !== null && (
                <span className="font-mono text-[11px] text-editorial-text bg-editorial-panel px-2 py-0.5 rounded border border-editorial-border shrink-0">
                  Threshold: {rule.threshold}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
""")

# 10. Behavior Baselines Page (apps/web/app/behavior/page.tsx)
write_file("apps/web/app/behavior/page.tsx", """'use client';

import React, { useEffect, useState } from 'react';
import { UserCheck, Activity, TrendingUp, AlertTriangle } from 'lucide-react';
import { api } from '@/lib/api';

export default function BehaviorPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getUserBaselines();
        setUsers(data);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">User Behavioral Baselines</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Layer 2 Statistical Anomaly Engine — Robust Z-Score with Median Absolute Deviation (MAD)
        </p>
      </div>

      <div className="grid gap-6">
        {users.map(u => {
          const evalRes = u.baseline_evaluation;
          return (
            <div key={u.id} className="border border-editorial-border rounded-xl bg-editorial-surface p-6 shadow-xs space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-editorial-border pb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded bg-editorial-panel flex items-center justify-center text-editorial-accent font-bold font-mono">
                    {u.username.slice(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <h3 className="font-bold text-base text-editorial-text">{u.full_name}</h3>
                    <div className="text-xs text-editorial-muted font-mono">@{u.username} • {u.role}</div>
                  </div>
                </div>

                <div className="text-right font-mono">
                  <div className="text-[10px] text-editorial-muted uppercase">S_BEHAVIOR DEVIATION</div>
                  <div className="text-xl font-bold text-editorial-accent">{evalRes.s_behavior.toFixed(1)}/100</div>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 font-mono text-xs">
                <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
                  <span className="text-[10px] text-editorial-muted uppercase">LOGIN HOURS</span>
                  <div className="text-sm font-bold text-editorial-text mt-0.5">{u.typical_login_hours}</div>
                </div>

                <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
                  <span className="text-[10px] text-editorial-muted uppercase">TYPICAL LOCATIONS</span>
                  <div className="text-sm font-bold text-editorial-text mt-0.5 truncate">{u.typical_locations.join(', ')}</div>
                </div>

                <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
                  <span className="text-[10px] text-editorial-muted uppercase">DAILY LOGINS</span>
                  <div className="text-sm font-bold text-editorial-text mt-0.5">{u.avg_daily_logins} / day</div>
                </div>

                <div className="p-3 rounded bg-editorial-panel border border-editorial-border">
                  <span className="text-[10px] text-editorial-muted uppercase">MEDIAN DOWNLOAD</span>
                  <div className="text-sm font-bold text-editorial-text mt-0.5">{u.avg_download_mb} MB/day</div>
                </div>
              </div>

              <div className="p-3 rounded bg-editorial-panel/60 border border-editorial-border text-xs flex items-center justify-between font-mono">
                <span className="text-editorial-muted">Robust Z-score Formula: <strong>z_MAD = |x - median| / (1.4826 * MAD)</strong></span>
                <span className="text-editorial-accent font-bold">z_MAD: {evalRes.z_mad_download}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
""")

# 11. Recovery Readiness Center (apps/web/app/recovery/page.tsx)
write_file("apps/web/app/recovery/page.tsx", """'use client';

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
""")

print("Detections, Behavior, and Recovery pages written.")
