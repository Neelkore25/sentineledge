'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
  Search,
  AlertTriangle,
  Play,
  RotateCcw,
  Activity,
  Sparkles,
  Sliders,
  Moon,
  Sun,
  X
} from 'lucide-react';
import { useApp } from '@/lib/store';

export function CommandPalette() {
  const { isCmdOpen, setIsCmdOpen, toggleTheme, setViewMode, viewMode } = useApp();
  const [query, setQuery] = useState('');
  const router = useRouter();

  if (!isCmdOpen) return null;

  const actions = [
    { name: 'View Active Incidents', href: '/incidents', icon: AlertTriangle, category: 'Navigation' },
    { name: 'Explore Telemetry Events', href: '/events', icon: Activity, category: 'Navigation' },
    { name: 'Open Simulation Lab', href: '/simulation', icon: Play, category: 'Simulation' },
    { name: 'Check Recovery Readiness', href: '/recovery', icon: RotateCcw, category: 'Recovery' },
    { name: 'AI Investigation Studio', href: '/ai-investigator', icon: Sparkles, category: 'AI' },
    { name: 'System Settings & Correlation Window', href: '/settings', icon: Sliders, category: 'Settings' },
    {
      name: `Switch to ${viewMode === 'analyst' ? 'Executive' : 'Analyst'} View`,
      action: () => setViewMode(viewMode === 'analyst' ? 'executive' : 'analyst'),
      icon: Sliders,
      category: 'View'
    },
    {
      name: 'Toggle Dark / Light Theme',
      action: () => toggleTheme(),
      icon: Moon,
      category: 'Appearance'
    }
  ];

  const filtered = actions.filter(a => a.name.toLowerCase().includes(query.toLowerCase()));

  const handleSelect = (item: typeof actions[0]) => {
    setIsCmdOpen(false);
    if (item.href) {
      router.push(item.href);
    } else if (item.action) {
      item.action();
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex items-start justify-center pt-24 p-4">
      <div className="w-full max-w-xl bg-editorial-surface border border-editorial-border rounded-lg shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <div className="p-3 border-b border-editorial-border flex items-center gap-3">
          <Search className="w-4 h-4 text-editorial-muted" />
          <input
            type="text"
            placeholder="Type a command or jump to page..."
            value={query}
            onChange={e => setQuery(e.target.value)}
            className="w-full bg-transparent text-sm text-editorial-text focus:outline-none"
            autoFocus
          />
          <button
            onClick={() => setIsCmdOpen(false)}
            className="p-1 text-editorial-muted hover:text-editorial-text rounded"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="max-h-72 overflow-y-auto p-2 space-y-1">
          {filtered.length === 0 ? (
            <div className="p-4 text-center text-xs text-editorial-muted">No commands matching '{query}'</div>
          ) : (
            filtered.map((item, idx) => {
              const Icon = item.icon;
              return (
                <button
                  key={idx}
                  onClick={() => handleSelect(item)}
                  className="w-full flex items-center justify-between p-2.5 rounded text-left hover:bg-editorial-panel text-xs text-editorial-text group transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-4 h-4 text-editorial-accent group-hover:scale-110 transition-transform" />
                    <span className="font-medium">{item.name}</span>
                  </div>
                  <span className="text-[10px] font-mono text-editorial-muted uppercase">{item.category}</span>
                </button>
              );
            })
          )}
        </div>

        <div className="p-2 border-t border-editorial-border bg-editorial-panel/40 flex items-center justify-between text-[11px] text-editorial-muted px-4">
          <span>Use <strong>ESC</strong> to close</span>
          <span className="font-mono">SentinelEdge Command Engine</span>
        </div>
      </div>
    </div>
  );
}
