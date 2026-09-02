'use client';

import React, { useEffect, useState } from 'react';
import { Sliders, Save, CheckCircle2 } from 'lucide-react';
import { api } from '@/lib/api';

export default function SettingsPage() {
  const [windowMins, setWindowMins] = useState('30');
  const [bruteThreshold, setBruteThreshold] = useState('5');
  const [aiProvider, setAiProvider] = useState('local');
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await api.getSettings();
        if (data.correlation_window_minutes) setWindowMins(data.correlation_window_minutes.value);
        if (data.brute_force_threshold) setBruteThreshold(data.brute_force_threshold.value);
        if (data.ai_provider) setAiProvider(data.ai_provider.value);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await Promise.all([
        api.updateSetting('correlation_window_minutes', windowMins),
        api.updateSetting('brute_force_threshold', bruteThreshold),
        api.updateSetting('ai_provider', aiProvider)
      ]);
      setSaved(true);
      setTimeout(() => setSaved(false), 2500);
    } catch (err) {
      alert(`Save failed: ${err}`);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">System Settings</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Configure detection thresholds, AI engine provider, and temporal correlation parameters
        </p>
      </div>

      <form onSubmit={handleSave} className="border border-editorial-border rounded-xl bg-editorial-surface p-6 shadow-xs space-y-6">
        <div className="space-y-4 text-xs">
          <div className="space-y-1.5">
            <label className="font-bold text-editorial-text font-mono flex items-center justify-between">
              <span>TEMPORAL CORRELATION WINDOW (MINUTES)</span>
              <span className="text-editorial-accent">{windowMins} min</span>
            </label>
            <p className="text-editorial-muted text-[11px]">
              Sliding time window used by Detection Engine Layer 3 to group security events by entity and map MITRE attack stages.
            </p>
            <input
              type="number"
              min={5}
              max={180}
              value={windowMins}
              onChange={e => setWindowMins(e.target.value)}
              className="w-full p-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text font-mono text-xs focus:outline-none focus:border-editorial-accent"
            />
          </div>

          <div className="space-y-1.5 pt-3 border-t border-editorial-border">
            <label className="font-bold text-editorial-text font-mono">
              BRUTE FORCE THRESHOLD (FAILED ATTEMPTS)
            </label>
            <p className="text-editorial-muted text-[11px]">
              Minimum authentication failures within the correlation window required to trigger RULE_AUTH_BRUTE_FORCE_001.
            </p>
            <input
              type="number"
              min={2}
              max={50}
              value={bruteThreshold}
              onChange={e => setBruteThreshold(e.target.value)}
              className="w-full p-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text font-mono text-xs focus:outline-none focus:border-editorial-accent"
            />
          </div>

          <div className="space-y-1.5 pt-3 border-t border-editorial-border">
            <label className="font-bold text-editorial-text font-mono">
              AI INVESTIGATION PROVIDER
            </label>
            <p className="text-editorial-muted text-[11px]">
              Select AI model provider for advisory incident analysis. Falls back automatically to deterministic local mode.
            </p>
            <select
              value={aiProvider}
              onChange={e => setAiProvider(e.target.value)}
              className="w-full p-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text font-mono text-xs focus:outline-none focus:border-editorial-accent"
            >
              <option value="local">Local Research Assistant (Deterministic Evidence Grounded)</option>
              <option value="openai">OpenAI (GPT-4o-mini / GPT-4o)</option>
              <option value="gemini">Google Gemini 1.5 / 2.0</option>
              <option value="anthropic">Anthropic Claude 3.5</option>
            </select>
          </div>
        </div>

        <div className="pt-4 border-t border-editorial-border flex items-center justify-between">
          {saved ? (
            <span className="text-status-healthy text-xs font-mono flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" /> Settings persisted to database.
            </span>
          ) : <span />}

          <button
            type="submit"
            className="flex items-center gap-2 px-5 py-2.5 rounded bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity"
          >
            <Save className="w-4 h-4" /> Save System Settings
          </button>
        </div>
      </form>
    </div>
  );
}
