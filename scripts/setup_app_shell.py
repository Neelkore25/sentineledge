import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 1. App Store Context (apps/web/lib/store.tsx)
write_file("apps/web/lib/store.tsx", """'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

type ViewMode = 'analyst' | 'executive';
type UserRole = 'Analyst' | 'Manager' | 'Viewer';
type ThemeMode = 'dark' | 'light';

interface AppContextType {
  theme: ThemeMode;
  setTheme: (t: ThemeMode) => void;
  toggleTheme: () => void;
  viewMode: ViewMode;
  setViewMode: (v: ViewMode) => void;
  userRole: UserRole;
  setUserRole: (r: UserRole) => void;
  isCmdOpen: boolean;
  setIsCmdOpen: (o: boolean) => void;
  refreshTrigger: number;
  triggerRefresh: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<ThemeMode>('dark');
  const [viewMode, setViewMode] = useState<ViewMode>('analyst');
  const [userRole, setUserRole] = useState<UserRole>('Analyst');
  const [isCmdOpen, setIsCmdOpen] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  const triggerRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [theme]);

  // Global Ctrl/Cmd + K shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsCmdOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <AppContext.Provider
      value={{
        theme,
        setTheme,
        toggleTheme,
        viewMode,
        setViewMode,
        userRole,
        setUserRole,
        isCmdOpen,
        setIsCmdOpen,
        refreshTrigger,
        triggerRefresh
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
""")

# 2. Sidebar Navigation (apps/web/components/Sidebar.tsx)
write_file("apps/web/components/Sidebar.tsx", """'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Shield,
  AlertTriangle,
  Activity,
  GitCommit,
  FlaskConical,
  Binary,
  UserCheck,
  RotateCcw,
  Sparkles,
  FileText,
  History,
  BookOpen,
  Settings,
  Flame,
  Layers
} from 'lucide-react';
import { useApp } from '@/lib/store';

const navItems = [
  { name: 'Overview', href: '/dashboard', icon: Activity, section: 'Core' },
  { name: 'Incidents', href: '/incidents', icon: AlertTriangle, section: 'Core' },
  { name: 'Events', href: '/events', icon: Layers, section: 'Core' },
  { name: 'Attack Stories', href: '/attack-stories', icon: GitCommit, section: 'Core' },
  { name: 'Simulation Lab', href: '/simulation', icon: FlaskConical, badge: 'Interactive', section: 'Operations' },
  { name: 'Detection Rules', href: '/detections', icon: Binary, section: 'Operations' },
  { name: 'Behavior', href: '/behavior', icon: UserCheck, section: 'Operations' },
  { name: 'Recovery', href: '/recovery', icon: RotateCcw, section: 'Resilience' },
  { name: 'AI Investigator', href: '/ai-investigator', icon: Sparkles, badge: 'Grounded', section: 'Intelligence' },
  { name: 'Reports', href: '/reports', icon: FileText, section: 'Intelligence' },
  { name: 'Audit Log', href: '/audit', icon: History, section: 'Governance' },
  { name: 'Research Hub', href: '/research', icon: BookOpen, section: 'Research' },
  { name: 'Settings', href: '/settings', icon: Settings, section: 'System' },
];

export function Sidebar() {
  const pathname = usePathname();
  const { userRole, viewMode } = useApp();

  return (
    <aside className="w-64 border-r border-editorial-border bg-editorial-surface flex flex-col justify-between h-screen sticky top-0 select-none z-20">
      <div>
        {/* Brand Header */}
        <div className="p-4 border-b border-editorial-border flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded bg-editorial-accent text-white flex items-center justify-center font-bold tracking-tight shadow-sm group-hover:scale-105 transition-transform">
              <Shield className="w-4 h-4" />
            </div>
            <div>
              <div className="font-bold text-sm tracking-tight text-editorial-text flex items-center gap-1.5">
                SentinelEdge
                <span className="text-[10px] uppercase font-mono px-1 py-0.2 rounded bg-editorial-panel text-editorial-muted border border-editorial-border">v1.0</span>
              </div>
              <div className="text-[11px] text-editorial-muted leading-none">Cyber-Resilience Lab</div>
            </div>
          </Link>
        </div>

        {/* View Mode Tag */}
        <div className="px-4 py-2 bg-editorial-panel/50 border-b border-editorial-border flex items-center justify-between text-[11px]">
          <span className="text-editorial-muted">MODE</span>
          <span className="font-mono font-medium text-editorial-accent uppercase tracking-wider">
            {viewMode}
          </span>
        </div>

        {/* Navigation List */}
        <nav className="p-2 space-y-0.5 overflow-y-auto max-h-[calc(100vh-210px)]">
          {navItems.map((item) => {
            const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center justify-between px-3 py-2 rounded text-xs font-medium transition-colors ${
                  isActive
                    ? 'bg-editorial-panel text-editorial-text font-semibold border border-editorial-border shadow-xs'
                    : 'text-editorial-muted hover:text-editorial-text hover:bg-editorial-panel/40'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-editorial-accent' : 'text-editorial-muted'}`} />
                  <span>{item.name}</span>
                </div>
                {item.badge && (
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-editorial-panel border border-editorial-border text-editorial-accent">
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Role and Status Footer */}
      <div className="p-3 border-t border-editorial-border bg-editorial-surface text-xs">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-status-healthy animate-pulse" />
            <span className="text-editorial-muted">Role:</span>
            <span className="font-mono font-medium text-editorial-text">{userRole}</span>
          </div>
          <span className="text-[10px] font-mono text-editorial-muted bg-editorial-panel px-1.5 py-0.5 rounded border border-editorial-border">
            PROTOTYPE
          </span>
        </div>
      </div>
    </aside>
  );
}
""")

# 3. Top System Status Header (apps/web/components/Header.tsx)
write_file("apps/web/components/Header.tsx", """'use client';

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
""")

# 4. Command Palette (apps/web/components/CommandPalette.tsx)
write_file("apps/web/components/CommandPalette.tsx", """'use client';

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
""")

# 5. Root Layout (apps/web/app/layout.tsx)
write_file("apps/web/app/layout.tsx", """import type { Metadata } from 'next';
import './globals.css';
import { AppProvider } from '@/lib/store';
import { Sidebar } from '@/components/Sidebar';
import { Header } from '@/components/Header';
import { CommandPalette } from '@/components/CommandPalette';

export const metadata: Metadata = {
  title: 'SentinelEdge — Explainable AI-Assisted Cyber Resilience',
  description: 'Research prototype for lightweight security monitoring, incident investigation, business-impact assessment, and recovery readiness.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-editorial-bg text-editorial-text flex antialiased">
        <AppProvider>
          <Sidebar />
          <div className="flex-1 flex flex-col min-w-0">
            <Header />
            <main className="flex-1 p-6 overflow-y-auto">
              {children}
            </main>
          </div>
          <CommandPalette />
        </AppProvider>
      </body>
    </html>
  );
}
""")

print("Phase 3 App Shell components created!")
