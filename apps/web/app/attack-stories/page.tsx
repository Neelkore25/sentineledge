'use client';

import React from 'react';
import Link from 'next/link';
import { GitCommit, ShieldAlert, ArrowDown, Play, ExternalLink } from 'lucide-react';

const attackStories = [
  {
    title: 'Too Many Doors (Credential Stuffing → Account Hijack)',
    category: 'Credential Access & Initial Access',
    target: 'Admin Identity & Auth Gateway',
    duration: '6 minutes',
    steps: [
      { time: '09:41:02', title: 'Repeated Authentication Failures', desc: '12 rapid failed login attempts from Romanian IP 194.26.29.114 targeting user finance_admin.', type: 'AUTH_BURST' },
      { time: '09:43:18', title: 'Successful Session Authentication', desc: 'Valid credential accepted on Admin Portal without MFA challenge from same external IP.', type: 'INITIAL_ACCESS' },
      { time: '09:44:05', title: 'Administrative User Query', desc: 'Accessed administrative endpoint /api/v1/admin/users and queried all corporate accounts.', type: 'RECON' },
      { time: '09:45:30', title: 'Correlated Incident Triggered', desc: 'SentinelEdge detection engine correlated burst into Incident #INC-1042 (Risk 82/100, CRITICAL).', type: 'ALERT' }
    ]
  },
  {
    title: 'The Privilege Jump (Intern Role Elevation)',
    category: 'Privilege Escalation',
    target: 'Internal IAM / Active Directory',
    duration: '2 minutes',
    steps: [
      { time: '14:10:11', title: 'IAM Roles Enumeration', desc: 'Junior engineer account dev_intern queried administrative role definitions.', type: 'RECON' },
      { time: '14:11:45', title: 'Unauthorized Super-Admin Role Assigned', desc: 'Direct privilege assignment to SuperAdministrator role without associated IT change ticket.', type: 'PRIV_ESC' },
      { time: '14:12:00', title: 'Deterministic Rule Triggered', desc: 'RULE_PRIV_ESCALATION_003 flagged unauthorized privilege mutation.', type: 'ALERT' }
    ]
  },
  {
    title: 'The Large Download (Data Exfiltration Spike)',
    category: 'Exfiltration',
    target: 'Customer Financial Database',
    duration: '4 minutes',
    steps: [
      { time: '03:15:00', title: 'Off-Hours Database SQL Dump', desc: 'Full database export executed against customer financial records (450,000 rows).', type: 'COLLECTION' },
      { time: '03:17:22', title: 'High-Volume Network Egress', desc: 'Outbound transfer of 2.8 GB compressed archive to external file hosting endpoint.', type: 'EXFIL' },
      { time: '03:18:00', title: 'Robust Z-Score MAD Deviation Spike', desc: 'Behavioral engine flagged 62x deviation over rolling daily baseline (45 MB).', type: 'ANOMALY' }
    ]
  }
];

export default function AttackStoriesPage() {
  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Attack Storyboards</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Progressive vertical timeline representations of multi-stage security compromise scenarios
        </p>
      </div>

      <div className="space-y-8">
        {attackStories.map((story, idx) => (
          <div key={idx} className="border border-editorial-border rounded-xl bg-editorial-surface p-6 shadow-xs space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-editorial-border pb-4">
              <div>
                <span className="text-[10px] font-mono uppercase text-editorial-accent font-semibold">{story.category}</span>
                <h3 className="font-bold text-lg text-editorial-text mt-0.5">{story.title}</h3>
                <div className="text-xs text-editorial-muted font-mono mt-1">Target Asset: {story.target} | Span: {story.duration}</div>
              </div>
              <Link
                href="/simulation"
                className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded bg-editorial-panel border border-editorial-border text-xs font-semibold text-editorial-text hover:bg-editorial-panel/80 transition-colors"
              >
                <Play className="w-3.5 h-3.5 text-editorial-accent" /> Run Scenario
              </Link>
            </div>

            {/* Vertical Progressive Timeline */}
            <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-editorial-border">
              {story.steps.map((step, stepIdx) => (
                <div key={stepIdx} className="relative group">
                  <div className="absolute -left-6 top-1 w-5 h-5 rounded-full bg-editorial-surface border-2 border-editorial-accent flex items-center justify-center text-[10px] font-mono text-editorial-accent">
                    {stepIdx + 1}
                  </div>
                  <div className="p-3.5 rounded bg-editorial-panel/70 border border-editorial-border space-y-1">
                    <div className="flex items-center justify-between font-mono text-[11px]">
                      <span className="font-bold text-editorial-text">{step.title}</span>
                      <span className="text-editorial-muted">{step.time}</span>
                    </div>
                    <p className="text-xs text-editorial-muted">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
