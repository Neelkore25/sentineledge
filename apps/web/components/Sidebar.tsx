'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Shield,
  AlertTriangle,
  Activity,
  Sparkles,
  Binary,
  RotateCcw,
  FileText,
  History,
  Settings
} from 'lucide-react';
import { useApp } from '@/lib/store';

const navItems = [
  { name: 'Overview', href: '/dashboard', icon: Activity },
  { name: 'Analyze Data', href: '/analyze', icon: Sparkles, badge: 'Analyze' },
  { name: 'Incidents', href: '/incidents', icon: AlertTriangle },
  { name: 'AI Investigator', href: '/ai-investigator', icon: Binary },
  { name: 'Recovery Posture', href: '/recovery', icon: RotateCcw },
  { name: 'Incident Reports', href: '/reports', icon: FileText },
  { name: 'Audit Ledger', href: '/audit', icon: History },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const { userRole, viewMode } = useApp();

  return (
    <aside className="w-64 border-r border-editorial-border bg-editorial-surface flex flex-col justify-between h-screen sticky top-0 select-none z-20">
      <div>
        {/* Brand Header */}
        <div className="p-4 border-b border-editorial-border flex items-center justify-between">
          <Link href="/dashboard" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded bg-editorial-accent text-white flex items-center justify-center font-bold tracking-tight shadow-sm group-hover:scale-105 transition-transform">
              <Shield className="w-4 h-4" />
            </div>
            <div>
              <div className="font-bold text-sm tracking-tight text-editorial-text flex items-center gap-1.5">
                SentinelEdge
                <span className="text-[10px] uppercase font-mono px-1 py-0.2 rounded bg-editorial-panel text-editorial-muted border border-editorial-border">v1.0</span>
              </div>
              <div className="text-[11px] text-editorial-muted leading-none">Security Telemetry & Investigation</div>
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
        <nav className="p-2 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center justify-between px-3 py-2.5 rounded text-xs font-medium transition-colors ${
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
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-editorial-panel border border-editorial-border text-editorial-accent font-semibold">
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
            <div className="w-2 h-2 rounded-full bg-status-healthy" />
            <span className="text-editorial-muted">Role:</span>
            <span className="font-mono font-medium text-editorial-text">{userRole}</span>
          </div>
          <span className="text-[10px] font-mono text-editorial-muted bg-editorial-panel px-1.5 py-0.5 rounded border border-editorial-border">
            ENGINE ACTIVE
          </span>
        </div>
      </div>
    </aside>
  );
}
