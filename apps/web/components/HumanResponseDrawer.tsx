'use client';

import React, { useState } from 'react';
import { ShieldCheck, Lock, UserX, RefreshCw, X, AlertCircle } from 'lucide-react';
import { api } from '@/lib/api';
import { useApp } from '@/lib/store';

interface HumanResponseDrawerProps {
  incidentId: string;
  target: string;
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

const actionOptions = [
  { id: 'SIMULATE_ACCOUNT_LOCK', name: 'Lock User Account', icon: UserX, desc: 'Temporarily disable authentication session and mandate password reset.' },
  { id: 'SIMULATE_SESSION_REVOCATION', name: 'Revoke All Active Sessions', icon: Lock, desc: 'Invalidate OAuth2 bearer tokens and force immediate re-authentication.' },
  { id: 'SIMULATE_IP_BLOCK', name: 'Block Inbound Source IP', icon: ShieldCheck, desc: 'Apply edge firewall drop rule for offending IP address.' },
  { id: 'INITIATE_BACKUP_RESTORE_DRILL', name: 'Initiate Restore Simulation', icon: RefreshCw, desc: 'Trigger sandbox restore drill on affected database asset.' }
];

export function HumanResponseDrawer({ incidentId, target, isOpen, onClose, onSuccess }: HumanResponseDrawerProps) {
  const { userRole, triggerRefresh } = useApp();
  const [selectedAction, setSelectedAction] = useState(actionOptions[0].id);
  const [reason, setReason] = useState('Correlated security anomaly confirmed by security analyst.');
  const [submitting, setSubmitting] = useState(false);
  const [confirmed, setConfirmed] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      await api.respondToIncident(incidentId, selectedAction, reason, target);
      setConfirmed(true);
      triggerRefresh();
      setTimeout(() => {
        onSuccess();
        onClose();
      }, 1200);
    } catch (err) {
      alert(`Action failed: ${err}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
      <div className="w-full max-w-lg bg-editorial-surface border border-editorial-border rounded-lg shadow-2xl overflow-hidden animate-in fade-in zoom-in-95">
        <div className="p-4 border-b border-editorial-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-editorial-accent" />
            <h3 className="font-bold text-sm text-editorial-text">Human-in-the-Loop Response Action</h3>
          </div>
          <button onClick={onClose} className="p-1 text-editorial-muted hover:text-editorial-text rounded">
            <X className="w-4 h-4" />
          </button>
        </div>

        {confirmed ? (
          <div className="p-8 text-center space-y-3">
            <div className="w-12 h-12 rounded-full bg-status-healthy/20 border border-status-healthy text-status-healthy flex items-center justify-center mx-auto">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h4 className="font-bold text-base text-editorial-text">Action Executed & Logged</h4>
            <p className="text-xs text-editorial-muted">Incident status updated to MITIGATED. Tamper-evident record committed to Audit Trail.</p>
          </div>
        ) : (
          <div className="p-5 space-y-4 text-xs">
            <div className="p-3 rounded bg-editorial-panel border border-editorial-border space-y-1">
              <div className="flex justify-between text-editorial-muted font-mono">
                <span>INCIDENT: <strong>#{incidentId}</strong></span>
                <span>ACTOR: <strong>{userRole}</strong></span>
              </div>
              <div className="text-editorial-text font-medium">Target Resource: <span className="font-mono text-editorial-accent">{target}</span></div>
            </div>

            <div className="space-y-2">
              <label className="font-semibold text-editorial-text">Select Remediation Action:</label>
              <div className="space-y-1.5">
                {actionOptions.map(opt => {
                  const Icon = opt.icon;
                  return (
                    <button
                      key={opt.id}
                      type="button"
                      onClick={() => setSelectedAction(opt.id)}
                      className={`w-full p-2.5 rounded border text-left flex items-start gap-3 transition-colors ${
                        selectedAction === opt.id
                          ? 'border-editorial-accent bg-editorial-panel text-editorial-text shadow-xs'
                          : 'border-editorial-border bg-editorial-surface text-editorial-muted hover:bg-editorial-panel/50'
                      }`}
                    >
                      <Icon className="w-4 h-4 text-editorial-accent mt-0.5 shrink-0" />
                      <div>
                        <div className="font-bold text-editorial-text">{opt.name}</div>
                        <div className="text-[11px] text-editorial-muted">{opt.desc}</div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="font-semibold text-editorial-text">Operational Justification / Reason:</label>
              <textarea
                value={reason}
                onChange={e => setReason(e.target.value)}
                rows={2}
                className="w-full p-2.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text text-xs focus:outline-none focus:border-editorial-accent"
              />
            </div>

            <div className="p-2.5 rounded bg-editorial-panel/60 border border-editorial-border text-[11px] text-editorial-muted flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-editorial-accent shrink-0" />
              <span>Simulated response changes incident status and permanently writes state changes to <strong>/audit</strong>.</span>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-editorial-border">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded text-editorial-muted hover:bg-editorial-panel border border-editorial-border transition-colors font-medium"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSubmit}
                disabled={submitting}
                className="px-4 py-2 rounded bg-editorial-accent text-white font-bold hover:opacity-90 transition-opacity shadow-xs"
              >
                {submitting ? 'Executing...' : 'Confirm Response Action'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
