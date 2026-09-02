'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { AlertTriangle, Search } from 'lucide-react';
import { api } from '@/lib/api';
import { Incident } from '@/lib/types';
import { useApp } from '@/lib/store';

export default function IncidentsPage() {
  const { refreshTrigger } = useApp();
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [search, setSearch] = useState('');
  const [severityFilter, setSeverityFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getIncidents({
          severity: severityFilter !== 'ALL' ? severityFilter : undefined,
          status: statusFilter !== 'ALL' ? statusFilter : undefined,
          search: search || undefined
        });
        setIncidents(data);
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, [search, severityFilter, statusFilter, refreshTrigger]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-editorial-border pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Incident Registry</h1>
          <p className="text-xs text-editorial-muted font-mono mt-0.5">
            Correlated multi-stage security events with explainable risk scores
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link
            href="/simulation"
            className="px-3.5 py-2 rounded bg-editorial-accent text-white font-bold text-xs shadow-xs hover:opacity-90 transition-opacity"
          >
            + Run Scenario in Lab
          </Link>
        </div>
      </div>

      <div className="p-3 rounded-lg border border-editorial-border bg-editorial-surface flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 flex-1 min-w-[200px]">
          <Search className="w-4 h-4 text-editorial-muted" />
          <input
            type="text"
            placeholder="Search by ID, title, user, or asset..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-transparent text-editorial-text focus:outline-none text-xs"
          />
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 font-mono text-[11px]">
            <span className="text-editorial-muted">SEVERITY:</span>
            <select
              value={severityFilter}
              onChange={e => setSeverityFilter(e.target.value)}
              className="bg-editorial-panel border border-editorial-border rounded px-2 py-1 text-editorial-text focus:outline-none"
            >
              <option value="ALL">ALL</option>
              <option value="CRITICAL">CRITICAL</option>
              <option value="HIGH">HIGH</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="LOW">LOW</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5 font-mono text-[11px]">
            <span className="text-editorial-muted">STATUS:</span>
            <select
              value={statusFilter}
              onChange={e => setStatusFilter(e.target.value)}
              className="bg-editorial-panel border border-editorial-border rounded px-2 py-1 text-editorial-text focus:outline-none"
            >
              <option value="ALL">ALL</option>
              <option value="OPEN">OPEN</option>
              <option value="INVESTIGATING">INVESTIGATING</option>
              <option value="MITIGATED">MITIGATED</option>
            </select>
          </div>
        </div>
      </div>

      <div className="border border-editorial-border rounded-lg bg-editorial-surface shadow-xs overflow-hidden">
        {incidents.length === 0 ? (
          <div className="p-12 text-center text-xs text-editorial-muted space-y-2">
            <AlertTriangle className="w-6 h-6 text-editorial-muted mx-auto" />
            <p className="font-medium text-editorial-text">No security incidents match the filter criteria.</p>
            <p>Generate simulated telemetry in the Simulation Lab to trigger new detections.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-editorial-panel/60 border-b border-editorial-border font-mono text-[10px] text-editorial-muted uppercase">
                <tr>
                  <th className="p-3">INCIDENT ID</th>
                  <th className="p-3">SEVERITY</th>
                  <th className="p-3">TITLE / CATEGORY</th>
                  <th className="p-3">AFFECTED ASSET & USER</th>
                  <th className="p-3">RISK</th>
                  <th className="p-3">STATUS</th>
                  <th className="p-3 text-right">ACTION</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-editorial-border">
                {incidents.map(inc => (
                  <tr key={inc.id} className="hover:bg-editorial-panel/40 transition-colors">
                    <td className="p-3 font-mono font-bold text-editorial-text">
                      <Link href={`/incidents/${inc.id}`} className="hover:text-editorial-accent">
                        #{inc.id}
                      </Link>
                    </td>
                    <td className="p-3">
                      <span className={`font-mono text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                        inc.severity === 'CRITICAL' ? 'bg-status-critical/15 text-status-critical border border-status-critical/30' :
                        inc.severity === 'HIGH' ? 'bg-status-warning/15 text-status-warning border border-status-warning/30' :
                        'bg-status-info/15 text-status-info border border-status-info/30'
                      }`}>
                        {inc.severity}
                      </span>
                    </td>
                    <td className="p-3">
                      <div className="font-semibold text-editorial-text">
                        <Link href={`/incidents/${inc.id}`} className="hover:underline">
                          {inc.title}
                        </Link>
                      </div>
                      <div className="text-[10px] font-mono text-editorial-muted">{inc.attack_category}</div>
                    </td>
                    <td className="p-3 font-mono text-[11px]">
                      <div className="text-editorial-text">{inc.affected_asset}</div>
                      <div className="text-editorial-muted">{inc.affected_user || '—'}</div>
                    </td>
                    <td className="p-3 font-mono font-bold text-base text-editorial-accent">
                      {inc.risk_score.toFixed(0)}
                    </td>
                    <td className="p-3">
                      <span className={`font-mono text-[10px] px-1.5 py-0.5 rounded font-medium ${
                        inc.status === 'MITIGATED' ? 'bg-status-healthy/15 text-status-healthy' :
                        inc.status === 'INVESTIGATING' ? 'bg-editorial-accent/15 text-editorial-accent' :
                        'bg-status-warning/15 text-status-warning'
                      }`}>
                        {inc.status}
                      </span>
                    </td>
                    <td className="p-3 text-right">
                      <Link
                        href={`/incidents/${inc.id}`}
                        className="px-3 py-1.5 rounded bg-editorial-panel border border-editorial-border font-semibold text-editorial-text hover:bg-editorial-panel/80 transition-colors"
                      >
                        Investigate
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
