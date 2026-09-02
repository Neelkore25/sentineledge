'use client';

import React, { useEffect, useState } from 'react';
import { History, ShieldCheck, Lock, UserX, RefreshCw } from 'lucide-react';
import { api } from '@/lib/api';
import { AuditLogItem } from '@/lib/types';
import { useApp } from '@/lib/store';

export default function AuditPage() {
  const { refreshTrigger } = useApp();
  const [logs, setLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await api.getAuditLogs();
        setLogs(data);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [refreshTrigger]);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Immutable Audit Ledger</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Tamper-evident log of all human-in-the-loop response actions, status transitions, and system events
        </p>
      </div>

      <div className="border border-editorial-border rounded-lg bg-editorial-surface shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-editorial-panel/60 border-b border-editorial-border text-[10px] text-editorial-muted uppercase">
              <tr>
                <th className="p-3">LOG ID</th>
                <th className="p-3">TIMESTAMP</th>
                <th className="p-3">ACTOR & ROLE</th>
                <th className="p-3">ACTION</th>
                <th className="p-3">TARGET RESOURCE</th>
                <th className="p-3">REASON / JUSTIFICATION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-editorial-border text-[11px]">
              {logs.map(log => (
                <tr key={log.id} className="hover:bg-editorial-panel/40 transition-colors">
                  <td className="p-3 font-bold text-editorial-text">{log.id}</td>
                  <td className="p-3 text-editorial-muted">{log.timestamp.slice(11, 19)}</td>
                  <td className="p-3">
                    <span className="font-bold text-editorial-text">{log.actor}</span>
                    <div className="text-[10px] text-editorial-muted">({log.role})</div>
                  </td>
                  <td className="p-3">
                    <span className="font-bold text-editorial-accent bg-editorial-panel px-1.5 py-0.5 rounded border border-editorial-border">
                      {log.action}
                    </span>
                  </td>
                  <td className="p-3 text-editorial-text max-w-[200px] truncate">{log.resource}</td>
                  <td className="p-3 text-editorial-muted max-w-[250px] truncate font-sans text-xs">{log.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
