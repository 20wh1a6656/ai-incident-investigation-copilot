import React from 'react';
import { Settings, X, Cpu, Server, Check } from 'lucide-react';

export default function SettingsModal({ isOpen, onClose, systemStatus, settings, onUpdateSettings }) {
  if (!isOpen) return null;

  const providers = [
    { id: 'mock', name: 'Mock Engine (Local Offline)' },
    { id: 'openai', name: 'OpenAI GPT Models (Cloud API)' },
    { id: 'github', name: 'GitHub Models (Enterprise API)' },
  ];

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm transition-all flex items-center justify-center p-4">
      <div className="bg-neutral-950 border border-neutral-800 w-full max-w-md rounded-2xl p-6 space-y-5 shadow-2xl relative fade-in-up">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <Settings className="w-4 h-4 text-[#7C5CFF]" /> Parameter Controls
          </h3>
          <button 
            onClick={onClose} 
            className="text-neutral-500 hover:text-white text-xs cursor-pointer p-1"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="space-y-4">
          <div className="space-y-2">
            <label className="text-xs font-semibold text-neutral-400 flex items-center gap-1.5">
              <Cpu className="w-3.5 h-3.5 text-[#4F8CFF]" /> Active Intelligence Provider
            </label>
            <div className="space-y-1.5">
              {providers.map((p) => (
                <button
                  key={p.id}
                  onClick={() => onUpdateSettings({ activeProvider: p.id })}
                  className={`w-full p-2.5 rounded-xl border text-xs font-medium flex items-center justify-between transition-all cursor-pointer ${
                    settings.activeProvider === p.id
                      ? 'bg-neutral-900 border-[#7C5CFF] text-white'
                      : 'bg-neutral-950 border-neutral-800 text-neutral-400 hover:text-neutral-200 hover:border-neutral-700'
                  }`}
                >
                  <span>{p.name}</span>
                  {settings.activeProvider === p.id && (
                    <Check className="w-3.5 h-3.5 text-[#7C5CFF]" />
                  )}
                </button>
              ))}
            </div>
          </div>

          <div className="border-t border-neutral-900 pt-4 space-y-2">
            <label className="text-xs font-semibold text-neutral-400 flex items-center gap-1.5">
              <Server className="w-3.5 h-3.5 text-[#2ECC71]" /> Integration Vector Health
            </label>
            <div className="p-3 bg-neutral-950 border border-neutral-900 rounded-xl space-y-2 text-[10px] text-neutral-400 font-mono">
              <div className="flex justify-between">
                <span>Database Connectivity:</span>
                <span className={systemStatus?.database?.status === 'connected' ? 'text-emerald-400' : 'text-rose-400'}>
                  {systemStatus?.database?.status || 'checking'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>ChromaDB Loaded:</span>
                <span className={systemStatus?.rag?.chroma_connected ? 'text-emerald-400' : 'text-amber-400'}>
                  {systemStatus?.rag?.chroma_connected ? 'Active' : 'Missing (Offline)'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>SentenceTransformers:</span>
                <span className={systemStatus?.rag?.library_loaded ? 'text-emerald-400' : 'text-amber-400'}>
                  {systemStatus?.rag?.library_loaded ? 'Available' : 'Disabled'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Vector Folder:</span>
                <span className="text-neutral-500 overflow-x-hidden text-right max-w-[160px] truncate">
                  {systemStatus?.rag?.storage_path || '../data/chroma_db'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
