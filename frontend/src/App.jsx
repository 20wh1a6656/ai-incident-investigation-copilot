import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import KBManagement from './pages/KBManagement';
import HistoryModal from './components/HistoryModal';
import SettingsModal from './components/SettingsModal';
import { getSystemHealth, getIncidentHistory, getIncidentDetails } from './services/api';
import { Info } from 'lucide-react';

export default function App() {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  
  // Modals
  const [historyOpen, setHistoryOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  
  // Settings
  const [settings, setSettings] = useState({
    activeProvider: 'mock',
  });

  // Backend statuses
  const [systemStatus, setSystemStatus] = useState(null);
  const [historyItems, setHistoryItems] = useState([]);
  
  // Toast notifications
  const [toastText, setToastText] = useState('');
  const [toastVisible, setToastVisible] = useState(false);

  // Poll system health
  const checkHealth = async () => {
    try {
      const data = await getSystemHealth();
      setSystemStatus(data);
    } catch (err) {
      console.error(err);
      setSystemStatus({ status: 'degraded' });
    }
  };

  const loadHistory = async () => {
    try {
      const list = await getIncidentHistory();
      setHistoryItems(list);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    checkHealth();
    loadHistory();
    // Poll health every 15s
    const timer = setInterval(checkHealth, 15000);
    return () => clearInterval(timer);
  }, []);

  const triggerToast = (text) => {
    setToastText(text);
    setToastVisible(true);
    setTimeout(() => {
      setToastVisible(false);
    }, 2500);
  };

  const handleUpdateSettings = (updates) => {
    setSettings(prev => ({ ...prev, ...updates }));
    triggerToast(`Configuration updated: ${Object.keys(updates).join(', ')}`);
  };

  const handleSelectRecord = async (recordId) => {
    try {
      triggerToast(`Loading incident recordINC-${recordId.slice(0, 4)}...`);
      // Simulating loading by triggering a reload of data from detail endpoint
      const detailed = await getIncidentDetails(recordId);
      
      // If there's results, we want to broadcast them to the dashboard
      // Note: We can send this record into Dashboard. To do this simply, we will mock click
      // or set triageResult state in the dashboard by saving details in a custom event or shared state.
      // We'll create a custom event that Dashboard can listen to.
      const event = new CustomEvent('loadIncidentRecord', { detail: detailed });
      window.dispatchEvent(event);
    } catch (err) {
      console.error(err);
      triggerToast("Error loading historical record.");
    }
  };

  return (
    <div className="antialiased min-h-screen flex flex-col bg-[#0A0A0A] text-white">
      {/* Top Navbar */}
      <Navbar 
        isSidebarCollapsed={isSidebarCollapsed}
        toggleSidebar={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        openSettings={() => setSettingsOpen(true)}
        openHistory={() => setHistoryOpen(true)}
        systemStatus={systemStatus}
      />

      <div className="flex flex-1 pt-16 min-h-screen relative w-full items-stretch">
        {/* Collapsible Sidebar */}
        <Sidebar 
          isCollapsed={isSidebarCollapsed}
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          onNewInvestigation={() => {
            setActiveTab('dashboard');
            window.dispatchEvent(new CustomEvent('resetDashboard'));
            triggerToast("Triage board reset.");
          }}
          openHistory={() => setHistoryOpen(true)}
          openSettings={() => setSettingsOpen(true)}
        />

        {/* Main Workspace Frame */}
        <main className="flex-1 bg-[#0A0A0A] p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full mb-20 z-10 fade-in-up overflow-y-auto">
          {activeTab === 'dashboard' ? (
            <>
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-neutral-900 pb-6">
                <div>
                  <h1 className="text-2xl lg:text-3xl font-bold tracking-tight text-white mb-1">AI Incident Investigation Copilot</h1>
                  <p className="text-sm text-neutral-400">Transform raw telemetry, ambiguous log trails, and outage alerts into deterministic triage roadmaps instantly.</p>
                </div>
              </div>
              <Dashboard 
                onActionToast={triggerToast}
                refreshHistory={loadHistory}
              />
            </>
          ) : (
            <KBManagement onActionToast={triggerToast} />
          )}
        </main>
      </div>

      {/* Dynamic Toast Notification Panel */}
      <div 
        id="toastNotification" 
        className={`fixed bottom-6 right-6 z-50 transform transition-all duration-300 pointer-events-none ${
          toastVisible ? 'translate-y-0 opacity-100' : 'translate-y-24 opacity-0'
        }`}
      >
        <div className="bg-neutral-900/90 border border-neutral-800 backdrop-blur-md px-4 py-3 rounded-xl shadow-2xl flex items-center space-x-3">
          <div className="w-5 h-5 rounded-full bg-[#4F8CFF]/20 flex items-center justify-center text-[#4F8CFF]">
            <Info className="w-3.5 h-3.5" />
          </div>
          <p id="toastText" className="text-xs text-neutral-200 font-medium">{toastText}</p>
        </div>
      </div>

      {/* History Modal */}
      <HistoryModal 
        isOpen={historyOpen}
        onClose={() => setHistoryOpen(false)}
        historyItems={historyItems}
        onSelectRecord={handleSelectRecord}
      />

      {/* Settings Modal */}
      <SettingsModal 
        isOpen={settingsOpen}
        onClose={() => setSettingsOpen(false)}
        systemStatus={systemStatus}
        settings={settings}
        onUpdateSettings={handleUpdateSettings}
      />
    </div>
  );
}
