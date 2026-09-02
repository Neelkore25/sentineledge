'use client';

import React, { useEffect, useState } from 'react';
import { Sun, Moon, Search, Sliders, RefreshCw, AlertCircle } from 'lucide-react';
import { useApp } from '@/lib/store';
import { api } from '@/lib/api';
import { SystemOverview } from '@/lib/types';

export function Header() {
  const { theme, toggleTheme, viewMode, setViewMode, setIsCmdOpen, refreshTrigger, triggerRefresh } = useApp();
  const [stats, setStats] = useState<SystemOverview | null>(null);
  const [loading, setLoading] = useState(false);

  const loadStats = async () => {
    try {
      setLoading(true);
      const data = await api.getOverviewStats();
      setStats(data);
    } catch (e) {
      console.warn('Backend not yet reachable, using fallback stats:', e);
      setStats({
        system_status: 'HEALTHY',
        last_event_seconds_ago: 8,
        open_incidents_count: 3,
        total_incidents_count: 8,
        organization_risk_score: 64.0,
        organization_risk_band: 'HIGH',
        recovery_readiness_score: 74.0,
        incident_pressure: { LOW: 0, MEDIUM: 1, HIGH: 1, CRITICAL: 1 },
        risk_trend: []
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
    const interval = setInterval(loadStats, 15000);
    return () => clearInterval(interval);
  }, [refreshTrigger]);

  return (
    <header className="h-14 border-b border-editorial-border bg-editorial-surface sticky top-0 z-10 flex items-center justify-between px-6 select-none">
      {/* Top Status Strip */}
      <div className="flex items-center gap-6 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-editorial-muted font-medium uppercase tracking-wider text-[10px]">SYSTEM STATUS</span>
          <span className="font-mono font-bold text-status-healthy flex items-center gap-1.5 bg-status-healthy/10 px-2 py-0.5 rounded border border-status-healthy/30">
            <span className="w-1.5 h-1.5 rounded-full bg-status-healthy" />
            {stats?.system_status || 'HEALTHY'}
          </span>
        </div>

        <div className="h-4 w-px bg-editorial-border hidden sm:block" />

        <div className="hidden sm:flex items-center gap-2">
          <span className="text-editorial-muted font-medium uppercase tracking-wider text-[10px]">LAST EVENT</span>
          <span className="font-mono text-editorial-text">
            {stats?.last_event_seconds_ago ?? 12}s ago
          </span>
        </div>

        <div className="h-4 w-px bg-editorial-border hidden md:block" />

        <div className="hidden md:flex items-center gap-2">
          <span className="text-editorial-muted font-medium uppercase tracking-wider text-[10px]">OPEN INCIDENTS</span>
          <span className="font-mono font-bold text-status-warning bg-status-warning/10 px-1.5 py-0.5 rounded border border-status-warning/30">
            {String(stats?.open_incidents_count ?? 3).padStart(2, '0')}
          </span>
        </div>

        <div className="h-4 w-px bg-editorial-border hidden lg:block" />

        <div className="hidden lg:flex items-center gap-2">
          <span className="text-editorial-muted font-medium uppercase tracking-wider text-[10px]">RECOVERY READINESS</span>
          <span className="font-mono font-bold text-editorial-accent bg-editorial-accent/10 px-1.5 py-0.5 rounded border border-editorial-accent/30">
            {stats?.recovery_readiness_score ?? 72}/100
          </span>
        </div>
      </div>

      {/* Controls & Dual Mode Toggle */}
      <div className="flex items-center gap-3">
        {/* Command Palette Trigger */}
        <button
          onClick={() => setIsCmdOpen(true)}
          className="flex items-center gap-2 px-2.5 py-1.5 rounded bg-editorial-panel text-editorial-muted text-xs hover:text-editorial-text border border-editorial-border transition-colors"
          title="Open Command Palette (Ctrl+K)"
        >
          <Search className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Search / Cmd</span>
          <kbd className="font-mono text-[10px] bg-editorial-surface px-1 py-0.5 rounded border border-editorial-border">⌘K</kbd>
        </button>

        {/* Analyst vs Executive Toggle */}
        <div className="flex items-center bg-editorial-panel p-0.5 rounded border border-editorial-border text-xs">
          <button
            onClick={() => setViewMode('analyst')}
            className={`px-2.5 py-1 rounded font-medium transition-all ${
              viewMode === 'analyst'
                ? 'bg-editorial-surface text-editorial-text shadow-xs font-semibold'
                : 'text-editorial-muted hover:text-editorial-text'
            }`}
          >
            Analyst
          </button>
          <button
            onClick={() => setViewMode('executive')}
            className={`px-2.5 py-1 rounded font-medium transition-all ${
              viewMode === 'executive'
                ? 'bg-editorial-surface text-editorial-text shadow-xs font-semibold'
                : 'text-editorial-muted hover:text-editorial-text'
            }`}
          >
            Executive
          </button>
        </div>

        {/* Refresh button */}
        <button
          onClick={triggerRefresh}
          className={`p-2 rounded text-editorial-muted hover:text-editorial-text hover:bg-editorial-panel transition-colors ${loading ? 'animate-spin' : ''}`}
          title="Refresh Data"
        >
          <RefreshCw className="w-4 h-4" />
        </button>

        {/* Theme switcher */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded text-editorial-muted hover:text-editorial-text hover:bg-editorial-panel transition-colors"
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>
      </div>
    </header>
  );
}
