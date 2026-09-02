'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Shield, UserCheck, Briefcase, Eye, ArrowRight } from 'lucide-react';
import { useApp } from '@/lib/store';

export default function DemoLauncherPage() {
  const router = useRouter();
  const { setUserRole, setViewMode } = useApp();

  const handleLaunch = (role: 'Analyst' | 'Manager' | 'Viewer', mode: 'analyst' | 'executive') => {
    setUserRole(role);
    setViewMode(mode);
    router.push('/dashboard');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-editorial-text tracking-tight">Interactive Demo Environment</h1>
        <p className="text-xs text-editorial-muted max-w-xl mx-auto">
          Choose an operational persona to explore SentinelEdge. Pre-seeded with realistic enterprise assets, users, and attack scenarios.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-5">
        <div className="p-5 rounded-xl border border-editorial-border bg-editorial-surface space-y-4 hover:border-editorial-accent transition-all flex flex-col justify-between shadow-xs">
          <div className="space-y-3">
            <div className="w-9 h-9 rounded bg-editorial-panel flex items-center justify-center text-editorial-accent">
              <UserCheck className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-editorial-text">Analyst Demo</h3>
            <p className="text-xs text-editorial-muted leading-relaxed">
              Full technical access: inspect raw telemetry logs, trigger simulations, run AI investigations, and simulate containment actions.
            </p>
          </div>
          <button
            onClick={() => handleLaunch('Analyst', 'analyst')}
            className="w-full py-2.5 rounded bg-editorial-accent text-white font-bold text-xs flex items-center justify-center gap-2 hover:opacity-90 transition-opacity"
          >
            Launch as Analyst <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="p-5 rounded-xl border border-editorial-border bg-editorial-surface space-y-4 hover:border-editorial-accent transition-all flex flex-col justify-between shadow-xs">
          <div className="space-y-3">
            <div className="w-9 h-9 rounded bg-editorial-panel flex items-center justify-center text-editorial-accent">
              <Briefcase className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-editorial-text">Executive Demo</h3>
            <p className="text-xs text-editorial-muted leading-relaxed">
              Strategic overview: focus on business impact, dollar exposure risk, recovery SLAs, and executive report exports.
            </p>
          </div>
          <button
            onClick={() => handleLaunch('Manager', 'executive')}
            className="w-full py-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text font-bold text-xs flex items-center justify-center gap-2 hover:bg-editorial-panel/80 transition-colors"
          >
            Launch as Executive <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="p-5 rounded-xl border border-editorial-border bg-editorial-surface space-y-4 hover:border-editorial-accent transition-all flex flex-col justify-between shadow-xs">
          <div className="space-y-3">
            <div className="w-9 h-9 rounded bg-editorial-panel flex items-center justify-center text-editorial-muted">
              <Eye className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-editorial-text">Viewer Demo</h3>
            <p className="text-xs text-editorial-muted leading-relaxed">
              Read-only perspective: browse incidents, attack stories, and research evaluation methodology.
            </p>
          </div>
          <button
            onClick={() => handleLaunch('Viewer', 'analyst')}
            className="w-full py-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-muted font-bold text-xs flex items-center justify-center gap-2 hover:bg-editorial-panel/80 transition-colors"
          >
            Launch as Viewer <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
