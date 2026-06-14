import React from 'react';
import { 
  ChevronLeft, 
  ChevronRight, 
  ShieldAlert, 
  HelpCircle, 
  History, 
  Settings 
} from 'lucide-react';

export default function Navbar({ 
  isSidebarCollapsed, 
  toggleSidebar, 
  openSettings, 
  openHistory, 
  systemStatus 
}) {
  const isHealthy = systemStatus?.status === 'healthy';

  return (
    <nav className="glass-nav fixed top-0 left-0 right-0 h-16 z-50 px-6 flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <button 
          onClick={toggleSidebar} 
          className="text-neutral-400 hover:text-white transition-colors p-1.5 rounded-lg hover:bg-white/5 mr-1 cursor-pointer"
        >
          {isSidebarCollapsed ? (
            <ChevronRight className="w-4 h-4" />
          ) : (
            <ChevronLeft className="w-4 h-4" />
          )}
        </button>
        
        <div className="flex items-center space-x-2.5">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-[#4F8CFF] to-[#7C5CFF] flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <ShieldAlert className="w-4 h-4 text-white" />
          </div>
          <span className="font-semibold text-sm tracking-tight bg-gradient-to-r from-white via-neutral-200 to-neutral-400 bg-clip-text text-transparent">
            AI Incident Investigation Copilot
          </span>
        </div>
        
        <div className="h-4 w-px bg-neutral-800"></div>
        
        <div className={`flex items-center space-x-2 px-2.5 py-1 rounded-full ${
          isHealthy ? 'bg-emerald-500/10 border border-emerald-500/20' : 'bg-rose-500/10 border border-rose-500/20'
        }`}>
          <span className={`w-1.5 h-1.5 rounded-full ${
            isHealthy ? 'bg-[#2ECC71] animate-pulse' : 'bg-rose-500 animate-pulse'
          }`}></span>
          <span className={`text-[11px] font-medium uppercase tracking-wider ${
            isHealthy ? 'text-[#2ECC71]' : 'text-rose-500'
          }`}>
            {isHealthy ? 'System Healthy' : 'System Degraded'}
          </span>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <button 
          onClick={openSettings} 
          className="text-neutral-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-white/5 cursor-pointer"
          title="Documentation & SOPs"
        >
          <HelpCircle className="w-4 h-4" />
        </button>
        <button 
          onClick={openHistory} 
          className="text-neutral-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-white/5 cursor-pointer"
          title="Triage History"
        >
          <History className="w-4 h-4" />
        </button>
        <button 
          onClick={openSettings} 
          className="text-neutral-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-white/5 cursor-pointer"
          title="Configure System"
        >
          <Settings className="w-4 h-4" />
        </button>
        
        <div className="h-4 w-px bg-neutral-800"></div>
        
        <div className="flex items-center space-x-2 pl-2">
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-neutral-700 to-neutral-900 border border-neutral-700 flex items-center justify-center text-[11px] font-medium tracking-wider text-neutral-300">
            DX
          </div>
        </div>
      </div>
    </nav>
  );
}
