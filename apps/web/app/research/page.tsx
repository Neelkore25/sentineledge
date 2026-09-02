import React from 'react';
import { BookOpen, Layers, CheckCircle2, AlertTriangle, Cpu } from 'lucide-react';

export default function ResearchPage() {
  return (
    <div className="space-y-8 max-w-4xl mx-auto py-4">
      <div className="border-b border-editorial-border pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-editorial-text">Research Methodology & Evaluation</h1>
        <p className="text-xs text-editorial-muted font-mono mt-0.5">
          Academic foundations, hypotheses testing framework, and comparative benchmarking for SME cyber resilience
        </p>
      </div>

      {/* Core Research Question */}
      <section className="p-6 rounded-xl border border-editorial-accent bg-editorial-surface shadow-xs space-y-3">
        <span className="text-[10px] font-mono uppercase text-editorial-accent font-bold">CORE RESEARCH QUESTION</span>
        <blockquote className="text-base font-semibold text-editorial-text italic">
          "Can a lightweight, explainable AI-assisted cybersecurity platform improve incident prioritization
          and recovery readiness for resource-constrained SMEs compared with conventional rule-based detection?"
        </blockquote>
      </section>

      {/* Formal Hypotheses */}
      <section className="space-y-4">
        <h2 className="text-sm font-bold font-mono text-editorial-text uppercase">Evaluation Hypotheses</h2>
        <div className="grid gap-4">
          <div className="p-5 rounded-lg border border-editorial-border bg-editorial-surface space-y-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-editorial-accent bg-editorial-panel px-2 py-0.5 rounded border border-editorial-border">H1</span>
              <h3 className="font-bold text-sm text-editorial-text">Hybrid Multi-Layer Detection Superiority</h3>
            </div>
            <p className="text-xs text-editorial-muted leading-relaxed">
              Combining deterministic rules, statistical Robust Z-Score (MAD) behavioral baselines, and temporal event correlation
              significantly reduces false-positive alert fatigue compared to isolated rule-only alerting.
            </p>
          </div>

          <div className="p-5 rounded-lg border border-editorial-border bg-editorial-surface space-y-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-editorial-accent bg-editorial-panel px-2 py-0.5 rounded border border-editorial-border">H2</span>
              <h3 className="font-bold text-sm text-editorial-text">Comprehension via Evidence-Grounded AI</h3>
            </div>
            <p className="text-xs text-editorial-muted leading-relaxed">
              Enforcing strict evidence packaging (citable telemetry IDs, baseline deviations, and explicit uncertainty boundaries)
              accelerates incident comprehension without hallucinated technical artifacts.
            </p>
          </div>

          <div className="p-5 rounded-lg border border-editorial-border bg-editorial-surface space-y-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-editorial-accent bg-editorial-panel px-2 py-0.5 rounded border border-editorial-border">H3</span>
              <h3 className="font-bold text-sm text-editorial-text">Coupled Recovery & Business Impact Prioritization</h3>
            </div>
            <p className="text-xs text-editorial-muted leading-relaxed">
              Evaluating technical threat severity alongside asset downtime costs and RPO/RTO disaster recovery compliance
              produces more actionable business prioritization than technical CVE severity alone.
            </p>
          </div>
        </div>
      </section>

      {/* Comparative Model Architecture */}
      <section className="border border-editorial-border rounded-xl bg-editorial-surface p-6 space-y-4">
        <h2 className="text-sm font-bold font-mono text-editorial-text uppercase">Architectural Comparison</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-editorial-panel/60 border-b border-editorial-border text-[10px] text-editorial-muted uppercase">
              <tr>
                <th className="p-2.5">DIMENSION</th>
                <th className="p-2.5">RULE-ONLY BASELINE</th>
                <th className="p-2.5">GENERIC SIEM CLONE</th>
                <th className="p-2.5 text-editorial-accent">SENTINELEDGE PLATFORM</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-editorial-border text-[11px]">
              <tr>
                <td className="p-2.5 font-bold">Detection</td>
                <td className="p-2.5 text-editorial-muted">Static thresholds</td>
                <td className="p-2.5 text-editorial-muted">Heavy queries</td>
                <td className="p-2.5 font-bold text-editorial-text">Rules + Robust Z-Score MAD + Sliding Correlation</td>
              </tr>
              <tr>
                <td className="p-2.5 font-bold">Explainability</td>
                <td className="p-2.5 text-editorial-muted">None (Boolean flag)</td>
                <td className="p-2.5 text-editorial-muted">Opaque logs</td>
                <td className="p-2.5 font-bold text-editorial-text">Evidence Rail + 5-Factor Risk Stack</td>
              </tr>
              <tr>
                <td className="p-2.5 font-bold">Recovery Integration</td>
                <td className="p-2.5 text-editorial-muted">Disconnected</td>
                <td className="p-2.5 text-editorial-muted">Disconnected</td>
                <td className="p-2.5 font-bold text-editorial-accent">Integrated Recovery Window (RPO/RTO SLA)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
