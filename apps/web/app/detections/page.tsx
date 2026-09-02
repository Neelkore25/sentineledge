'use client';

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
