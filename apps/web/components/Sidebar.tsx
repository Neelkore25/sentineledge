'use client';

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
