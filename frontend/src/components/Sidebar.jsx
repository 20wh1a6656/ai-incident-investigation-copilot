import React from 'react';
import { 
  LayoutDashboard, 
  PlusCircle, 
  Archive, 
  Database, 
  Cpu, 
  FileText, 
  Sliders 
} from 'lucide-react';

export default function Sidebar({ 
  isCollapsed, 
  activeTab, 
  setActiveTab, 
  onNewInvestigation, 
  openHistory, 
  openSettings 
}) {
  return (
    <aside 
      id="sidebar" 
      className={`${
        isCollapsed ? 'w-[72px]' : 'w-64'
      } shrink-0 bg-[#0A0A0A] border-r border-neutral-900 p-4 space-y-6 hidden md:flex flex-col sticky top-16 h-[calc(100vh-16px)] overflow-x-hidden z-40`}
    >
      <div className="space-y-1">
        {!isCollapsed && (
          <p className="px-3 text-[10px] font-medium text-neutral-500 uppercase tracking-widest mb-2 transition-opacity duration-300">
            Workspace
          </p>
        )}
        
        <button
          onClick={() => setActiveTab('dashboard')}
          className={`flex items-center space-x-3 px-3 py-2 rounded-lg border w-full text-left text-xs font-medium transition-all group cursor-pointer ${
            activeTab === 'dashboard' 
              ? 'bg-white/5 border-white/5 text-white' 
              : 'border-transparent text-neutral-400 hover:text-white hover:bg-white/5'
          }`}
        >
          <LayoutDashboard className={`w-4 h-4 shrink-0 ${activeTab === 'dashboard' ? 'text-[#4F8CFF]' : ''}`} />
          {!isCollapsed && <span className="sidebar-text transition-opacity duration-300">Dashboard</span>}
        </button>

        <button 
          onClick={onNewInvestigation}
          className="flex items-center space-x-3 px-3 py-2 rounded-lg text-neutral-400 hover:text-white hover:bg-white/5 text-xs font-medium transition-all border border-transparent w-full text-left cursor-pointer"
        >
          <PlusCircle className="w-4 h-4 shrink-0" />
          {!isCollapsed && <span className="sidebar-text transition-opacity duration-300">New Investigation</span>}
        </button>

        <button 
          onClick={openHistory}
          className="flex items-center space-x-3 px-3 py-2 rounded-lg text-neutral-400 hover:text-white hover:bg-white/5 text-xs font-medium transition-all border border-transparent w-full text-left cursor-pointer"
        >
          <Archive className="w-4 h-4 shrink-0" />
          {!isCollapsed && <span className="sidebar-text transition-opacity duration-300">Investigation History</span>}
        </button>
      </div>

      <div className="space-y-1">
        {!isCollapsed && (
          <p className="px-3 text-[10px] font-medium text-neutral-500 uppercase tracking-widest mb-2 transition-opacity duration-300">
            Systems
          </p>
        )}

        <button
          onClick={() => setActiveTab('kb')}
          className={`flex items-center space-x-3 px-3 py-2 rounded-lg border w-full text-left text-xs font-medium transition-all group cursor-pointer ${
            activeTab === 'kb' 
              ? 'bg-white/5 border-white/5 text-white' 
              : 'border-transparent text-neutral-400 hover:text-white hover:bg-white/5'
          }`}
        >
          <Database className={`w-4 h-4 shrink-0 ${activeTab === 'kb' ? 'text-[#7C5CFF]' : ''}`} />
          {!isCollapsed && <span className="sidebar-text transition-opacity duration-300">Knowledge Base</span>}
        </button>

        <div className="flex items-center space-x-3 px-3 py-2 rounded-lg text-neutral-400 hover:text-white hover:bg-white/5 text-xs font-medium transition-all group select-none">
          <Cpu className="w-4 h-4 shrink-0" />
          {!isCollapsed && (
            <span className="sidebar-text flex items-center justify-between w-full">
              <span>Agent Activity</span>
              <span className="w-2 h-2 rounded-full bg-[#7C5CFF]"></span>
            </span>
          )}
        </div>

        <div className="flex items-center space-x-3 px-3 py-2 rounded-lg text-neutral-400 hover:text-white hover:bg-white/5 text-xs font-medium transition-all group select-none">
          <FileText className="w-4 h-4 shrink-0" />
          {!isCollapsed && <span className="sidebar-text">Reports</span>}
        </div>
      </div>

      <div className="mt-auto pt-4 border-t border-neutral-900">
        <button 
          onClick={openSettings}
          className="flex items-center space-x-3 px-3 py-2 rounded-lg text-neutral-400 hover:text-white hover:bg-white/5 text-xs font-medium transition-all border border-transparent w-full text-left cursor-pointer"
        >
          <Sliders className="w-4 h-4 shrink-0" />
          {!isCollapsed && <span className="sidebar-text transition-opacity duration-300">Settings</span>}
        </button>
      </div>
    </aside>
  );
}
