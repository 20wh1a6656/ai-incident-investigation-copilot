import React, { useState, useEffect } from 'react';
import TriageForm from '../components/TriageForm';
import ResultsDashboard from '../components/ResultsDashboard';
import { Fingerprint } from 'lucide-react';
import { runInvestigation } from '../services/api';

export default function Dashboard({ onActionToast, refreshHistory }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [triageResult, setTriageResult] = useState(null);
  const [loadingStep, setLoadingStep] = useState(0); // 0=None, 2=Diagnosing

  const sampleOutageInput = {
    desc: "Critical transactional connection dropping across checkout service endpoints. High latency spikes observed on database connection pool acquisition blocks.",
    alarms: "Datadog Alert: APM Checkout Service Latency P99 > 4500ms",
    logs: "org.postgresql.util.PSQLException: FATAL: remaining connection slots are reserved...",
    env: "k8s-prod-cluster-us-east"
  };

  useEffect(() => {
    const handleLoadRecord = (e) => {
      const detailed = e.detail;
      if (detailed && detailed.incident) {
        setTriageResult({
          incident_id: detailed.incident.id,
          duration: detailed.incident.duration,
          classification: detailed.incident.classification,
          confidence: detailed.incident.confidence,
          severity: detailed.incident.severity,
          results: detailed.result
        });
      }
    };

    const handleReset = () => {
      setTriageResult(null);
      setLoadingStep(0);
    };

    window.addEventListener('loadIncidentRecord', handleLoadRecord);
    window.addEventListener('resetDashboard', handleReset);
    return () => {
      window.removeEventListener('loadIncidentRecord', handleLoadRecord);
      window.removeEventListener('resetDashboard', handleReset);
    };
  }, []);

  const handleLoadSample = () => {
    onActionToast("Production sample context loaded.");
    return sampleOutageInput;
  };

  const handleTriageSubmit = async (formData) => {
    setIsSubmitting(true);
    setTriageResult(null);
    setLoadingStep(2); // Set loading progress active

    try {
      // Direct call to single-stage investigation endpoint
      const response = await runInvestigation(formData);
      
      setTriageResult({
        incident_id: response.incident_id,
        duration: response.duration,
        classification: response.classification,
        confidence: response.confidence,
        severity: response.severity,
        results: response.results
      });
      
      onActionToast("AI diagnosis complete. Triage plan generated.");
      refreshHistory();
    } catch (err) {
      console.error(err);
      onActionToast("Diagnosis execution failed. Please verify configurations.");
    } finally {
      setIsSubmitting(false);
      setLoadingStep(0);
    }
  };

  return (
    <div className="space-y-8">
      {/* Triage Ingestion Form */}
      <TriageForm 
        onSubmit={handleTriageSubmit}
        onLoadSample={handleLoadSample}
        isSubmitting={isSubmitting}
      />

      {/* Loading Skeleton */}
      {loadingStep > 0 && (
        <div className="space-y-6 fade-in-up">
          <div className="h-16 w-full rounded-2xl shimmer-bg"></div>
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <div className="lg:col-span-1 space-y-6">
              <div className="h-44 rounded-2xl shimmer-bg"></div>
              <div className="h-64 rounded-2xl shimmer-bg"></div>
            </div>
            <div className="lg:col-span-3 space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="h-24 rounded-xl shimmer-bg"></div>
                <div className="h-24 rounded-xl shimmer-bg"></div>
                <div className="h-24 rounded-xl shimmer-bg"></div>
                <div className="h-24 rounded-xl shimmer-bg"></div>
              </div>
              <div className="h-96 rounded-2xl shimmer-bg"></div>
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!triageResult && loadingStep === 0 && (
        <div id="emptyState" className="glass-card py-20 px-4 text-center max-w-xl mx-auto flex flex-col items-center justify-center fade-in-up">
          <div className="w-12 h-12 rounded-2xl bg-neutral-900 border border-neutral-800 flex items-center justify-center mb-4 text-neutral-500">
            <Fingerprint className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-semibold text-white mb-1">Awaiting Investigation Sequence</h3>
          <p className="text-xs text-neutral-400 max-w-sm mx-auto mb-6">
            Populate the ingestion criteria engine above or load a standardized production sample script to generate your dynamic RAG execution pipeline.
          </p>
          <button 
            onClick={() => {
              const data = sampleOutageInput;
              handleTriageSubmit({
                description: data.desc,
                alarms: data.alarms,
                logs: data.logs,
                env: data.env,
                severity: 'P1'
              });
            }}
            className="px-4 py-2 rounded-xl bg-neutral-900 border border-neutral-800 hover:border-neutral-700 text-xs font-medium text-neutral-200 transition-all cursor-pointer"
          >
            Instant Auto-Fill Demo
          </button>
        </div>
      )}

      {/* Results State */}
      {triageResult && loadingStep === 0 && (
        <ResultsDashboard 
          resultData={triageResult}
          onActionToast={onActionToast}
        />
      )}
    </div>
  );
}
