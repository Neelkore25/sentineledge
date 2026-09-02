'use client';

import React, { useEffect, useState } from 'react';
import { Layers, Search, Filter, ArrowUpDown, Eye, Code, X } from 'lucide-react';
import { api } from '@/lib/api';
import { SecurityEvent } from '@/lib/types';
import { useApp } from '@/lib/store';

export default function EventsPage() {
  const { refreshTrigger } = useApp();
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [selectedEvent, setSelectedEvent] = useState<SecurityEvent | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const res = await api.getEvents({ limit: 50 });
        setEvents(res.items);
        setTotal(res.total);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [refreshTrigger]);

  const filtered = events.filter(e => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      e.id.toLowerCase().includes(q) ||
      e.event_type.toLowerCase().includes(q) ||
      (e.user_id && e.user_id.toLowerCase().includes(q)) ||
      (e.source_ip && e.source_ip.toLowerCase().includes(q)) ||
      (e.endpoint && e.endpoint.toLowerCase().includes(q))
    );
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-editorial-border pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Security Telemetry Explorer</h1>
          <p className="text-xs text-editorial-muted font-mono mt-0.5">
            Normalized raw and simulated telemetry streams ({total} indexed records)
          </p>
        </div>
      </div>

      <div className="p-3 rounded-lg border border-editorial-border bg-editorial-surface flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 flex-1">
          <Search className="w-4 h-4 text-editorial-muted" />
          <input
            type="text"
            placeholder="Search by event ID, IP, user, endpoint, or event type..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-transparent text-editorial-text focus:outline-none text-xs"
          />
        </div>
        <span className="text-[11px] font-mono text-editorial-muted">Showing {filtered.length} of {total} events</span>
      </div>

      <div className="border border-editorial-border rounded-lg bg-editorial-surface shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-editorial-panel/60 border-b border-editorial-border text-[10px] text-editorial-muted uppercase">
              <tr>
                <th className="p-3">EVENT ID</th>
                <th className="p-3">TIMESTAMP</th>
                <th className="p-3">SOURCE & TYPE</th>
                <th className="p-3">SOURCE IP / LOCATION</th>
                <th className="p-3">USER / IDENTITY</th>
                <th className="p-3">STATUS</th>
                <th className="p-3 text-right">PAYLOAD</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-editorial-border text-[11px]">
              {filtered.map(e => (
                <tr key={e.id} className="hover:bg-editorial-panel/40 transition-colors">
                  <td className="p-3 font-bold text-editorial-text">{e.id}</td>
                  <td className="p-3 text-editorial-muted">{e.timestamp.slice(11, 19)}</td>
                  <td className="p-3">
                    <span className="font-bold text-editorial-accent">{e.event_type}</span>
                    <div className="text-[10px] text-editorial-muted">{e.source}</div>
                  </td>
                  <td className="p-3">
                    <div>{e.source_ip || '—'}</div>
                    <div className="text-[10px] text-editorial-muted">{e.location || 'Internal'}</div>
                  </td>
                  <td className="p-3 text-editorial-text">{e.user_id || 'system'}</td>
                  <td className="p-3">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                      e.status === 'FAILURE' || e.status === 'BLOCKED' ? 'bg-status-critical/15 text-status-critical' :
                      e.status === 'ANOMALOUS' ? 'bg-status-warning/15 text-status-warning' :
                      'bg-status-healthy/15 text-status-healthy'
                    }`}>
                      {e.status}
                    </span>
                  </td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => setSelectedEvent(e)}
                      className="px-2 py-1 rounded bg-editorial-panel border border-editorial-border text-editorial-text hover:bg-editorial-panel/80"
                    >
                      <Code className="w-3.5 h-3.5 inline mr-1" /> JSON
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* JSON Modal */}
      {selectedEvent && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-2xl bg-editorial-surface border border-editorial-border rounded-lg shadow-2xl overflow-hidden animate-in fade-in">
            <div className="p-4 border-b border-editorial-border flex items-center justify-between">
              <span className="font-mono font-bold text-sm text-editorial-text">Event Payload: {selectedEvent.id}</span>
              <button onClick={() => setSelectedEvent(null)} className="p-1 text-editorial-muted hover:text-editorial-text">
                <X className="w-4 h-4" />
              </button>
            </div>
            <pre className="p-4 font-mono text-xs text-editorial-text bg-editorial-panel/50 overflow-x-auto max-h-96">
              {JSON.stringify(selectedEvent, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
