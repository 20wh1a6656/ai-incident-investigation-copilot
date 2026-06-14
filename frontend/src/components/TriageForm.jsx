import React, { useState } from 'react';
import { SearchCode, UploadCloud, Sparkles, Terminal } from 'lucide-react';

export default function TriageForm({ onSubmit, onLoadSample, isSubmitting }) {
  const [description, setDescription] = useState('');
  const [alarms, setAlarms] = useState('');
  const [logs, setLogs] = useState('');
  const [env, setEnv] = useState('');
  const [severity, setSeverity] = useState('P3');

  const handleAutofill = () => {
    const sample = onLoadSample();
    setDescription(sample.desc);
    setAlarms(sample.alarms);
    setLogs(sample.logs);
    setEnv(sample.env);
    setSeverity('P1');
  };

  const handleReset = () => {
    setDescription('');
    setAlarms('');
    setLogs('');
    setEnv('');
    setSeverity('P3');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!description.trim()) return;
    onSubmit({
      description,
      alarms: alarms || null,
      logs: logs || null,
      env: env || null,
      severity
    });
  };

  return (
    <section className="glass-card p-6 relative overflow-hidden group fade-in-up">
      <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-[#4F8CFF]/40 to-transparent"></div>
      
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2.5">
          <SearchCode className="w-4 h-4 text-[#4F8CFF]" />
          <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-200">Incident Triage Ingestion Engine</h2>
        </div>
        <button 
          type="button"
          onClick={handleAutofill}
          className="px-3 py-1.5 rounded-lg border border-neutral-800 bg-neutral-900 text-neutral-300 hover:text-white text-xs font-medium transition-all flex items-center gap-1.5 cursor-pointer"
        >
          <Terminal className="w-3.5 h-3.5" /> Load Sample Outage
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            <div>
              <label className="block text-xs font-medium text-neutral-400 mb-1.5">
                Core Incident Description <span className="text-red-400">*</span>
              </label>
              <textarea 
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows="4" 
                required
                className="w-full bg-neutral-950/60 border border-neutral-800 rounded-xl px-3.5 py-2.5 text-xs text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-[#4F8CFF]/50 transition-colors resize-none" 
                placeholder="Paste downstream alert symptoms, broken endpoints, or observed latency spikes..."
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-neutral-400 mb-1.5">Active Monitoring Alarms</label>
                <input 
                  type="text" 
                  value={alarms}
                  onChange={(e) => setAlarms(e.target.value)}
                  className="w-full bg-neutral-950/60 border border-neutral-800 rounded-xl px-3.5 py-2.5 text-xs text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-[#4F8CFF]/50 transition-colors" 
                  placeholder="e.g., Datadog: PagerDuty #2819"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-400 mb-1.5">Environment Context</label>
                <input 
                  type="text" 
                  value={env}
                  onChange={(e) => setEnv(e.target.value)}
                  className="w-full bg-neutral-950/60 border border-neutral-800 rounded-xl px-3.5 py-2.5 text-xs text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-[#4F8CFF]/50 transition-colors" 
                  placeholder="e.g., k8s-us-east-1-prod, cluster-b"
                />
              </div>
            </div>
          </div>

          <div className="flex flex-col justify-between space-y-4">
            <div>
              <label className="block text-xs font-medium text-neutral-400 mb-1.5">Raw Log Payload / Stack Trace</label>
              <textarea 
                value={logs}
                onChange={(e) => setLogs(e.target.value)}
                rows="4" 
                className="w-full bg-neutral-950/60 border border-neutral-800 rounded-xl px-3.5 py-2.5 font-mono text-[11px] text-neutral-300 placeholder-neutral-600 focus:outline-none focus:border-[#4F8CFF]/50 transition-colors resize-none" 
                placeholder="Paste application trace records here..."
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-neutral-400 mb-1.5">Blast Radius Severity</label>
              <select 
                value={severity}
                onChange={(e) => setSeverity(e.target.value)}
                className="w-full bg-neutral-950/60 border border-neutral-800 rounded-xl px-3.5 py-2.5 text-xs text-neutral-200 focus:outline-none focus:border-[#4F8CFF]/50 transition-colors"
              >
                <option value="P1">P1 Critical — Production Outage</option>
                <option value="P2">P2 High — Major Functionality Degraded</option>
                <option value="P3">P3 Medium — Isolated Tenant Impact</option>
                <option value="P4">P4 Low — Performance Variance</option>
              </select>
            </div>
          </div>
        </div>

        <div className="mt-6 pt-4 border-t border-neutral-900 flex flex-wrap items-center justify-between gap-4">
          <button 
            type="button"
            className="px-3.5 py-2 rounded-xl border border-neutral-800 text-neutral-400 hover:text-white hover:bg-white/5 text-xs font-medium transition-all flex items-center gap-2 cursor-pointer"
          >
            <UploadCloud className="w-3.5 h-3.5" /> Attach Diagnostics File
          </button>
          
          <div className="flex items-center gap-3">
            <button 
              type="button" 
              onClick={handleReset} 
              className="px-4 py-2 rounded-xl text-neutral-400 hover:text-white text-xs font-medium transition-all cursor-pointer"
            >
              Reset Form
            </button>
            <button 
              type="submit" 
              disabled={isSubmitting || !description.trim()}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#4F8CFF] to-[#7C5CFF] text-white text-xs font-medium hover:opacity-90 transition-all shadow-lg shadow-indigo-500/10 flex items-center gap-2 cursor-pointer disabled:opacity-50"
            >
              <Sparkles className="w-3.5 h-3.5" /> {isSubmitting ? 'Diagnosing...' : 'Run AI Diagnosis'}
            </button>
          </div>
        </div>
      </form>
    </section>
  );
}
