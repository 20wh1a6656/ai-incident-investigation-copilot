import React from 'react';
import { 
  ChevronRight, 
  Layers, 
  ListOrdered, 
  FileDown, 
  Code, 
  ExternalLink,
  CheckCircle2,
  AlertCircle,
  TrendingUp,
  FileText,
  XCircle,
  Info,
  ShieldAlert
} from 'lucide-react';

export default function ResultsDashboard({ resultData, onActionToast }) {
  if (!resultData) return null;

  const {
    incident_id,
    duration,
    classification,
    confidence,
    severity,
    results
  } = resultData;

  const {
    root_causes = [],
    evidence = {},
    runbook = [],
    actions = [],
    escalation = {},
    checklist = [],
    audit = []
  } = results || {};

  // Formulate stages based on the new sequential agent pipeline
  const stages = [
    { num: 1, name: 'Knowledge Retrieval Agent', status: results ? 'Done' : 'Processing' },
    { num: 2, name: 'Evidence Correlation Agent', status: results ? 'Done' : 'Pending' },
    { num: 3, name: 'Classification Agent', status: results ? 'Done' : 'Pending' },
    { num: 4, name: 'Root Cause Agent', status: results ? 'Done' : 'Pending' },
    { num: 5, name: 'Investigation Planner Agent', status: results ? 'Done' : 'Pending' }
  ];

  const handleCopyJSON = () => {
    navigator.clipboard.writeText(JSON.stringify(resultData, null, 2));
    onActionToast('Copied JSON trace payload to clipboard');
  };

  const handleExportPDF = () => {
    onActionToast('PDF Generation initiated successfully');
  };

  const handleBroadcast = () => {
    onActionToast('Corporate incident ticket broadcasted');
  };

  return (
    <div className="space-y-8 fade-in-up">
      {/* Pipeline Agent Stage Tracker */}
      <div className="glass-card p-4 overflow-x-auto no-scrollbar">
        <div className="flex items-center justify-between min-w-[900px] gap-4">
          {stages.map((st, index) => (
            <React.Fragment key={st.num}>
              <div className="flex items-center space-x-3 flex-1 px-2">
                <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                  st.status === 'Done' 
                    ? 'bg-[#2ECC71]/20 border border-[#2ECC71]/40 text-[#2ECC71]' 
                    : st.status === 'Processing' 
                    ? 'bg-indigo-500/20 border border-indigo-500/40 text-[#4F8CFF] animate-pulse' 
                    : 'bg-neutral-900 border border-neutral-800 text-neutral-500'
                }`}>
                  {st.num}
                </div>
                <div>
                  <p className={`text-xs font-semibold whitespace-nowrap ${
                    st.status === 'Done' ? 'text-white' : 'text-neutral-400'
                  }`}>
                    {st.name}
                  </p>
                  <p className={`text-[10px] ${
                    st.status === 'Done' ? 'text-[#2ECC71]' : st.status === 'Processing' ? 'text-[#4F8CFF]' : 'text-neutral-600'
                  }`}>
                    {st.status}
                  </p>
                </div>
              </div>
              {index < stages.length - 1 && (
                <ChevronRight className="w-4 h-4 text-neutral-800 flex-shrink-0" />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Sidebar Metrics Panel */}
        <div className="space-y-6 lg:col-span-1">
          <div className="glass-card p-5 space-y-4">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-400">Triage Metrics</h3>
            <div className="space-y-3">
              <div className="p-3 bg-neutral-950 rounded-xl border border-neutral-900">
                <p className="text-[11px] text-neutral-500">Investigation Duration</p>
                <p id="metric-duration" className="text-lg font-semibold text-white mt-0.5">{duration || '0.0s'}</p>
              </div>
              
              <div className="p-3 bg-neutral-950 rounded-xl border border-neutral-900">
                <p className="text-[11px] text-neutral-500">AI Confidence Core Index</p>
                <div className="flex items-center justify-between mt-0.5">
                  <p id="metric-confidence" className="text-lg font-semibold text-white">{confidence || 0}%</p>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                    confidence >= 80 ? 'bg-[#2ECC71]/10 text-[#2ECC71]' : 
                    confidence >= 50 ? 'bg-amber-500/10 text-amber-400' :
                    'bg-rose-500/10 text-rose-450'
                  }`}>
                    {confidence >= 80 ? 'High' : (confidence >= 50 ? 'Medium' : 'Low')}
                  </span>
                </div>
              </div>

              <div className="p-3 bg-neutral-950 rounded-xl border border-neutral-900">
                <p className="text-[11px] text-neutral-500">Knowledge Sources Parsed</p>
                <p id="metric-sources" className="text-lg font-semibold text-white mt-0.5">
                  {evidence?.retrieved_chunks ? `${evidence.retrieved_chunks.length} Chunks` : (evidence?.sopName ? '1 Document' : '0 Documents')}
                </p>
              </div>
            </div>
          </div>

          {/* Console Audit Logs */}
          <div className="glass-card p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-400">Agent Activity</h3>
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-[#7C5CFF]"></span>
              </span>
            </div>
            <div id="agentConsole" className="space-y-2 max-h-[350px] overflow-y-auto no-scrollbar font-mono text-[10px] text-neutral-400 bg-neutral-950 p-3 rounded-xl border border-neutral-900">
              {audit && audit.length > 0 ? (
                audit.map((log, idx) => (
                  <div key={idx} className="border-b border-neutral-900/50 pb-1 last:border-0 leading-relaxed">
                    <span className="text-neutral-600 mr-1">&gt;</span>
                    {log}
                  </div>
                ))
              ) : (
                <div className="text-neutral-500">// Interfacing with pipeline agents...</div>
              )}
            </div>
          </div>
        </div>

        {/* Core Results Block */}
        <div className="space-y-6 lg:col-span-3">
          {/* Classification Banner */}
          <div className="glass-card p-6 space-y-4">
            <div className="flex flex-wrap items-start justify-between gap-4 border-b border-neutral-900 pb-4">
              <div>
                <span className="text-[10px] uppercase font-bold tracking-widest text-[#4F8CFF]">AI Classification</span>
                <h3 className="text-lg font-bold text-white mt-0.5">{classification || 'Analyzing Incident...'}</h3>
              </div>
              <div className="flex gap-2">
                <span className={`px-2 py-0.5 text-[10px] rounded font-bold border ${
                  severity === 'P1' ? 'bg-red-500/10 text-[#FF5C5C] border-red-500/25' :
                  severity === 'P2' ? 'bg-amber-500/10 text-amber-400 border-amber-500/25' :
                  'bg-neutral-800 text-neutral-350 border-neutral-700'
                }`}>
                  {severity || 'P3'} SEVERITY
                </span>
              </div>
            </div>

            {/* Unknown Incident Warning Banner */}
            {classification === "Unknown Incident" && (
              <div className="p-4 bg-yellow-500/10 border border-yellow-500/35 text-yellow-450 rounded-2xl flex items-start gap-3 shadow-lg">
                <ShieldAlert className="w-5 h-5 shrink-0 text-yellow-500 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-yellow-450">Unknown Incident Diagnostic Fallback Protocol</h4>
                  <p className="text-xs text-neutral-350 mt-1 leading-relaxed">
                    {evidence?.classification_reasoning || "Insufficient evidence or similarity metrics to match a specific SOP. The AI has triggered the default diagnostic collection playbook (system metrics, socket dumps, replication validation) and routed this alert as an Unknown Incident to the L1 Triage support queue."}
                  </p>
                </div>
              </div>
            )}

            {/* Primary & Secondary Root Cause bars */}
            <div>
              <h4 className="text-xs font-semibold text-neutral-400 uppercase tracking-wider mb-3">Probable Core Root Causes</h4>
              <div className="space-y-3">
                {root_causes.length > 0 ? (
                  root_causes.map((rc, idx) => (
                    <div key={idx} className={`p-3 border rounded-xl space-y-1 ${
                      idx === 0 ? 'bg-neutral-950/40 border-neutral-800' : 'bg-neutral-950/20 border-neutral-900/60'
                    }`}>
                      <div className="flex justify-between text-xs items-center">
                        <div className="flex items-center space-x-2">
                          <span className={`text-[9px] px-1.5 py-0.5 rounded font-bold ${
                            idx === 0 ? 'bg-[#FF5C5C]/15 text-[#FF5C5C]' : 'bg-amber-500/15 text-amber-400'
                          }`}>
                            {idx === 0 ? 'PRIMARY' : 'SECONDARY'}
                          </span>
                          <span className="text-white font-medium">{rc.title}</span>
                        </div>
                        <span className="text-neutral-400 font-mono">{rc.percentage}% Probability</span>
                      </div>
                      <div className="w-full bg-neutral-900 h-1.5 rounded-full overflow-hidden">
                        <div 
                          className={`h-full ${rc.design || 'bg-indigo-500'}`} 
                          style={{ width: `${rc.percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-xs text-neutral-500 italic">No root cause probabilities determined.</div>
                )}
              </div>
            </div>
          </div>

          {/* Confidence Distribution Panel */}
          <div className="glass-card p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4 text-[#4F8CFF]" />
                <h3 className="text-sm font-semibold text-white">Confidence Distribution</h3>
              </div>
              <span className="text-[10px] text-neutral-500 font-mono">Relative Agent Scores</span>
            </div>
            {evidence?.candidates?.length > 0 ? (
              <div className="space-y-3">
                {evidence.candidates.map((cand, idx) => {
                  const isSelected = cand.name === classification;
                  return (
                    <div key={idx} className={`p-3 rounded-xl border ${
                      isSelected 
                        ? 'bg-indigo-950/20 border-indigo-500/30' 
                        : 'bg-neutral-950/40 border-neutral-900'
                    }`}>
                      <div className="flex justify-between text-xs mb-1.5 items-center">
                        <div className="flex items-center space-x-2">
                          <span className={`w-2 h-2 rounded-full ${isSelected ? 'bg-indigo-400' : 'bg-neutral-600'}`}></span>
                          <span className={`font-medium ${isSelected ? 'text-white' : 'text-neutral-400'}`}>
                            {cand.name}
                          </span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="text-neutral-400 font-mono">{cand.percentage}%</span>
                          {isSelected && (
                            <span className="text-[9px] bg-indigo-500/25 text-indigo-300 px-1.5 py-0.5 rounded font-semibold border border-indigo-500/20 uppercase tracking-wider">
                              Selected
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="w-full bg-neutral-900 h-2 rounded-full overflow-hidden">
                        <div 
                          className={`h-full transition-all duration-500 ${isSelected ? 'bg-gradient-to-r from-indigo-500 to-[#4F8CFF]' : 'bg-neutral-700'}`} 
                          style={{ width: `${cand.percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-xs text-neutral-500 text-center py-6 border border-dashed border-neutral-800 rounded-xl">
                No matching candidate distributions calculated.
              </div>
            )}
          </div>

          {/* Retrieved Evidence Panel */}
          <div className="glass-card p-6">
            <div className="flex items-center space-x-2 mb-4">
              <FileText className="w-4 h-4 text-[#4F8CFF]" />
              <h3 className="text-sm font-semibold text-white">Retrieved SOP Reference Chunks (RAG)</h3>
            </div>
            
            {evidence?.retrieved_chunks?.length > 0 ? (
              <div className="space-y-4 max-h-[400px] overflow-y-auto pr-1 no-scrollbar">
                {evidence.retrieved_chunks.map((chunk, idx) => {
                  const score = chunk.confidence_score || 0;
                  const scoreColor = score >= 80 ? 'text-[#2ECC71] bg-[#2ECC71]/15 border-[#2ECC71]/20' : 
                                     score >= 50 ? 'text-[#FFC72C] bg-[#FFC72C]/15 border-[#FFC72C]/20' : 
                                     'text-neutral-400 bg-neutral-900 border-neutral-850';
                  return (
                    <div key={idx} className="bg-neutral-950 border border-neutral-900 rounded-xl p-4 space-y-2">
                      <div className="flex justify-between items-center text-[10px]">
                        <span className="text-neutral-300 font-semibold flex items-center gap-1.5">
                          <span className="text-neutral-500 bg-neutral-900 px-1.5 py-0.5 rounded font-mono">#{idx+1}</span>
                          {chunk.title}
                        </span>
                        <div className="flex items-center gap-2">
                          <span className={`text-[9px] px-1.5 py-0.5 rounded font-bold border ${scoreColor}`}>
                            {score}% Similarity
                          </span>
                          <span className="text-neutral-500 italic">Source: {chunk.source || 'Local Document'}</span>
                        </div>
                      </div>
                      <p className="text-xs text-neutral-350 font-mono leading-relaxed bg-[#0A0A0A] p-3 rounded-xl border border-neutral-900/60 overflow-x-auto whitespace-pre-wrap">
                        {chunk.content}
                      </p>
                    </div>
                  );
                })}
              </div>
            ) : evidence?.sopName ? (
              <div className="bg-neutral-950 border border-neutral-900 rounded-xl p-4 space-y-3">
                <div className="flex justify-between items-center text-[10px] border-b border-neutral-900 pb-2">
                  <span className="text-neutral-400 font-semibold">{evidence.sopName}</span>
                  <span className="text-neutral-500 italic">Source: {evidence.source} ({evidence.strength})</span>
                </div>
                <p className="text-xs text-neutral-300 font-mono leading-relaxed bg-[#0E0E0E] p-3 rounded-xl border border-neutral-900/80">
                  {evidence.snippet}
                </p>
              </div>
            ) : (
              <p className="text-xs text-neutral-500 text-center py-4 border border-dashed border-neutral-800 rounded-xl">
                No matching reference runbooks discovered.
              </p>
            )}
          </div>

          {/* Why This Classification? Panel */}
          <div className="glass-card p-6">
            <div className="flex items-center space-x-2 mb-4 border-b border-neutral-900 pb-3">
              <Layers className="w-4 h-4 text-[#7C5CFF]" />
              <h3 className="text-sm font-semibold text-white">Why This Classification?</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Supporting Evidence */}
              <div className="p-4 bg-emerald-950/10 border border-emerald-500/20 rounded-xl space-y-3">
                <div className="flex items-center space-x-2 text-emerald-450 font-bold text-[10px] uppercase tracking-wider">
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0 text-emerald-400" />
                  <span>Supporting Evidence</span>
                </div>
                {evidence?.supporting_evidence?.length > 0 ? (
                  <ul className="space-y-1.5">
                    {evidence.supporting_evidence.map((sig, idx) => (
                      <li key={idx} className="text-[11px] text-neutral-300 flex items-start gap-1.5">
                        <span className="text-emerald-400 mt-0.5">•</span>
                        <span>Telemetry signal: <strong className="font-mono text-emerald-300">{sig}</strong></span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-[11px] text-neutral-550 italic">No supporting signals correlated.</p>
                )}
              </div>

              {/* Contradictory Evidence */}
              <div className="p-4 bg-rose-950/10 border border-rose-500/20 rounded-xl space-y-3">
                <div className="flex items-center space-x-2 text-rose-405 font-bold text-[10px] uppercase tracking-wider">
                  <XCircle className="w-3.5 h-3.5 shrink-0 text-rose-450" />
                  <span>Contradictory Evidence</span>
                </div>
                {evidence?.contradictory_evidence?.length > 0 ? (
                  <ul className="space-y-1.5">
                    {evidence.contradictory_evidence.map((con, idx) => (
                      <li key={idx} className="text-[11px] text-neutral-300 flex items-start gap-1.5">
                        <span className="text-rose-400 mt-0.5">•</span>
                        <span>{con}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-[11px] text-neutral-550 italic">No conflicting signals detected.</p>
                )}
              </div>

              {/* Missing Evidence */}
              <div className="p-4 bg-neutral-900/40 border border-neutral-850 rounded-xl space-y-3">
                <div className="flex items-center space-x-2 text-neutral-450 font-bold text-[10px] uppercase tracking-wider">
                  <Info className="w-3.5 h-3.5 shrink-0 text-neutral-450" />
                  <span>Missing Signals</span>
                </div>
                {evidence?.evidence_summary?.categories?.[classification]?.missing_evidence?.length > 0 ? (
                  <ul className="space-y-1.5">
                    {evidence.evidence_summary.categories[classification].missing_evidence.map((mis, idx) => (
                      <li key={idx} className="text-[11px] text-neutral-400 flex items-start gap-1.5">
                        <span className="text-neutral-500 mt-0.5">•</span>
                        <span>Expected term not seen: <span className="font-mono text-neutral-500">{mis}</span></span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-[11px] text-neutral-550 italic">All expected diagnostics matched.</p>
                )}
              </div>
            </div>
          </div>

          {/* Investigation Runbook steps */}
          <div className="glass-card p-6">
            <div className="flex items-center space-x-2 mb-4">
              <ListOrdered className="w-4 h-4 text-[#2ECC71]" />
              <h3 className="text-sm font-semibold text-white">Recommended Investigation Runbook Plan</h3>
            </div>
            <div className="space-y-2">
              {runbook.length > 0 ? (
                runbook.map((rb, idx) => (
                  <div key={idx} className="p-3 bg-neutral-950 border border-neutral-900 rounded-xl flex items-start gap-3">
                    <span className="text-xs font-semibold text-[#2ECC71] bg-[#2ECC71]/10 px-2 py-0.5 rounded">
                      Step {idx + 1}
                    </span>
                    <div className="space-y-1">
                      <p className="text-xs font-medium text-white">{rb.step}</p>
                      <p className="text-[11px] text-neutral-400 leading-relaxed">{rb.detail}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-xs text-neutral-500 italic">No investigation steps designed.</div>
              )}
            </div>
          </div>

          {/* Remediation & Escalation side-by-side */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-5">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-400 mb-3">
                Prioritized Remediation Actions
              </h3>
              <div className="space-y-2.5">
                {actions.length > 0 ? (
                  actions.map((act, idx) => (
                    <div 
                      key={idx} 
                      className="text-xs p-3 rounded-xl bg-neutral-950 border border-neutral-900 flex justify-between items-center"
                    >
                      <span className="text-neutral-200 font-medium">{act.title}</span>
                      <span className={`px-2 py-0.5 text-[9px] rounded font-bold uppercase ${act.style}`}>
                        {act.priority}
                      </span>
                    </div>
                  ))
                ) : (
                  <div className="text-xs text-neutral-500 italic">No prioritized remediation actions defined.</div>
                )}
              </div>
            </div>

            <div className="glass-card p-5">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-400 mb-3">
                Incident Escalation Routing
              </h3>
              {escalation?.team ? (
                <div className="p-3 bg-neutral-950 border border-neutral-900 rounded-xl space-y-3 text-xs">
                  <div className="flex justify-between border-b border-neutral-900 pb-1.5">
                    <span className="text-neutral-500">Escalation Group:</span>
                    <span className="text-[#4F8CFF] font-semibold">{escalation.team}</span>
                  </div>
                  <div className="flex justify-between border-b border-neutral-900 pb-1.5">
                    <span className="text-neutral-500">Specialist Tier:</span>
                    <span className="text-white font-medium">{escalation.level}</span>
                  </div>
                  <div className="flex justify-between border-b border-neutral-900 pb-1.5">
                    <span className="text-neutral-500">Assigned Pod:</span>
                    <span className="text-neutral-300">{escalation.group}</span>
                  </div>
                  <div className="text-[11px] text-neutral-400 leading-relaxed italic bg-[#0A0A0A] p-2 rounded border border-neutral-900">
                    Reason: {escalation.reason}
                  </div>
                </div>
              ) : (
                <p className="text-xs text-neutral-500">No escalation trigger required.</p>
              )}
            </div>
          </div>

          {/* Verification Checklist */}
          <div className="glass-card p-5">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-400 mb-3">
              Post-Remediation Verification Checklist
            </h3>
            <div className="space-y-2 bg-neutral-950 p-4 rounded-xl border border-neutral-900">
              {checklist.length > 0 ? (
                checklist.map((ch, idx) => (
                  <div key={idx} className="flex items-center gap-2.5 text-xs">
                    <CheckCircle2 className="w-4 h-4 text-[#2ECC71] shrink-0" />
                    <span className="text-neutral-350 font-medium">{ch}</span>
                  </div>
                ))
              ) : (
                <div className="text-xs text-neutral-500 italic">No verification checklist items defined.</div>
              )}
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
            <div className="flex items-center gap-2">
              <button 
                onClick={handleExportPDF}
                className="px-3.5 py-2 rounded-xl bg-neutral-900 border border-neutral-800 text-neutral-350 hover:text-white text-xs font-medium transition-all flex items-center gap-1.5 cursor-pointer hover:border-neutral-700"
              >
                <FileDown className="w-3.5 h-3.5" /> PDF Report
              </button>
              <button 
                onClick={handleCopyJSON}
                className="px-3.5 py-2 rounded-xl bg-neutral-900 border border-neutral-800 text-neutral-350 hover:text-white text-xs font-medium transition-all flex items-center gap-1.5 cursor-pointer hover:border-neutral-700"
              >
                <Code className="w-3.5 h-3.5" /> Copy Data JSON
              </button>
            </div>
            
            <button 
              onClick={handleBroadcast}
              className="px-4 py-2 rounded-xl bg-white text-black font-semibold text-xs transition-all hover:bg-neutral-200 flex items-center gap-1.5 cursor-pointer shadow-lg hover:shadow-white/5"
            >
              <ExternalLink className="w-3.5 h-3.5" /> Broadcast Corporate Ticket
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

