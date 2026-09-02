'use client';

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
