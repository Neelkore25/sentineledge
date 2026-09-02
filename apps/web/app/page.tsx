import React from 'react';
import Link from 'next/link';
import {
  Shield,
  ArrowRight,
  Activity,
  Layers,
  Sparkles,
  RotateCcw,
  AlertTriangle,
  Play,
  BookOpen
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="max-w-5xl mx-auto space-y-16 py-8">
      <section className="space-y-6 text-center pt-8 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-editorial-panel border border-editorial-border text-xs font-mono text-editorial-accent">
          <Shield className="w-3.5 h-3.5" />
          <span>RESEARCH PROTOTYPE — SME CYBER RESILIENCE</span>
        </div>

        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-editorial-text leading-tight">
          Detect clearly. Respond deliberately. <br className="hidden sm:inline" />
          <span className="text-editorial-accent">Recover ready.</span>
        </h1>

        <p className="max-w-2xl mx-auto text-base sm:text-lg text-editorial-muted leading-relaxed">
          SentinelEdge is an explainable AI-assisted cybersecurity and recovery readiness platform
          engineered for resource-constrained small and medium enterprises.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <Link
            href="/demo"
            className="flex items-center gap-2 px-6 py-3 rounded-lg bg-editorial-accent text-white font-bold text-sm shadow-md hover:opacity-90 transition-all hover:scale-102"
          >
            <Play className="w-4 h-4" />
            Open Live Interactive Demo
          </Link>
          <Link
            href="/research"
            className="flex items-center gap-2 px-6 py-3 rounded-lg bg-editorial-panel border border-editorial-border text-editorial-text font-semibold text-sm hover:bg-editorial-panel/80 transition-colors"
          >
            <BookOpen className="w-4 h-4" />
            Explore Research & Hypotheses
          </Link>
        </div>
      </section>

      <section className="border border-editorial-border rounded-xl bg-editorial-surface p-6 shadow-sm">
        <h2 className="text-xs font-mono uppercase text-editorial-muted tracking-wider mb-4 text-center">
          COMPLETE EXPLAINABLE WORKFLOW
        </h2>
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-mono">
          {['Telemetry', 'Normalization', 'Hybrid Detection', 'Risk Scoring', 'Business Impact', 'Recovery Readiness', 'AI Investigation', 'Human Action', 'Audit Trail'].map((step, idx, arr) => (
            <React.Fragment key={idx}>
              <span className="px-2.5 py-1.5 rounded bg-editorial-panel border border-editorial-border text-editorial-text font-semibold">
                {step}
              </span>
              {idx < arr.length - 1 && <span className="text-editorial-muted hidden sm:inline">→</span>}
            </React.Fragment>
          ))}
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-6">
        <div className="p-6 rounded-xl border border-editorial-border bg-editorial-surface space-y-3">
          <div className="w-10 h-10 rounded bg-editorial-panel flex items-center justify-center text-editorial-accent">
            <Layers className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-editorial-text">1. Multi-Layer Detection</h3>
          <p className="text-xs text-editorial-muted leading-relaxed">
            Combines deterministic threshold rules, statistical Robust Z-Score (MAD) behavioral baselines,
            and configurable sliding-window event correlation into a unified risk model.
          </p>
        </div>

        <div className="p-6 rounded-xl border border-editorial-border bg-editorial-surface space-y-3">
          <div className="w-10 h-10 rounded bg-editorial-panel flex items-center justify-center text-editorial-accent">
            <Sparkles className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-editorial-text">2. Evidence-Grounded AI</h3>
          <p className="text-xs text-editorial-muted leading-relaxed">
            Strict evidence contract: the AI assistant receives only observed telemetry IDs and baseline deviations,
            never invents logs, and cites exact event references.
          </p>
        </div>

        <div className="p-6 rounded-xl border border-editorial-border bg-editorial-surface space-y-3">
          <div className="w-10 h-10 rounded bg-editorial-panel flex items-center justify-center text-editorial-accent">
            <RotateCcw className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-editorial-text">3. Recovery Readiness</h3>
          <p className="text-xs text-editorial-muted leading-relaxed">
            Couples technical threat severity with business impact, asset downtime costs, and backup RPO/RTO
            disaster recovery SLA compliance.
          </p>
        </div>
      </section>

      <section className="p-6 rounded-xl border border-editorial-border bg-editorial-panel/60 space-y-3 text-xs">
        <div className="flex items-center gap-2 font-bold text-editorial-text">
          <AlertTriangle className="w-4 h-4 text-editorial-accent" />
          <span>Research Integrity & Limitations Disclosure</span>
        </div>
        <p className="text-editorial-muted leading-relaxed">
          SentinelEdge is a prototype built for academic evaluation and demonstration. All telemetry streams are
          generated synthetically using realistic attack scenarios without real malicious traffic. AI investigation outputs
          are advisory decision-support recommendations requiring human verification before execution.
        </p>
      </section>
    </div>
  );
}
