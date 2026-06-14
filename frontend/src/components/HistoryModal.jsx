import React from 'react';
import { History, X } from 'lucide-react';

export default function HistoryModal({ isOpen, onClose, historyItems, onSelectRecord }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm transition-all flex items-center justify-center p-4">
      <div className="bg-neutral-950 border border-neutral-800 w-full max-w-lg rounded-2xl p-6 space-y-4 shadow-2xl relative fade-in-up">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <History className="w-4 h-4 text-[#4F8CFF]" /> Historic Audits
          </h3>
          <button 
            onClick={onClose} 
            className="text-neutral-500 hover:text-white text-xs cursor-pointer p-1"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="space-y-2 max-h-[300px] overflow-y-auto no-scrollbar">
          {historyItems && historyItems.length > 0 ? (
            historyItems.map((item) => (
              <div 
                key={item.id}
                onClick={() => {
                  onSelectRecord(item.id);
                  onClose();
                }}
                className="p-3 bg-neutral-900/40 rounded-xl border border-neutral-800 hover:border-neutral-700 cursor-pointer transition-all flex justify-between items-center group"
              >
                <div className="space-y-1">
                  <div className="text-xs font-medium text-white group-hover:text-[#4F8CFF] transition-colors">
                    {item.classification || 'Unclassified Outage'}
                  </div>
                  <div className="text-[10px] text-neutral-500 line-clamp-1 max-w-[320px]">
                    {item.description}
                  </div>
                </div>
                <div className="flex flex-col items-end space-y-1">
                  <span className={`px-1.5 py-0.5 rounded text-[8px] font-bold ${
                    item.severity === 'P1' ? 'bg-red-500/10 text-rose-400 border border-red-500/20' : 
                    item.severity === 'P2' ? 'bg-orange-500/10 text-orange-400 border border-orange-500/20' :
                    'bg-neutral-800 text-neutral-400'
                  }`}>
                    {item.severity}
                  </span>
                  <span className="text-[9px] text-neutral-600">
                    {new Date(item.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))
          ) : (
            <p className="text-xs text-neutral-500 text-center py-6">No historical records found.</p>
          )}
        </div>
      </div>
    </div>
  );
}
