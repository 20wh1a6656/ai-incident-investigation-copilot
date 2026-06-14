import React, { useState, useEffect } from 'react';
import { Database, Plus, Search, BookOpen } from 'lucide-react';
import { listKBDocs, addKBDoc } from '../services/api';

export default function KBManagement({ onActionToast }) {
  const [docs, setDocs] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [source, setSource] = useState('Confluence Runbooks');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchDocs = async () => {
    try {
      const data = await listKBDocs();
      setDocs(data);
    } catch (err) {
      console.error(err);
      onActionToast("Failed to fetch knowledge base documents.");
    }
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;

    setIsSubmitting(true);
    try {
      await addKBDoc({ title, content, source });
      onActionToast("Runbook indexed successfully into Vector RAG DB.");
      setTitle('');
      setContent('');
      fetchDocs();
    } catch (err) {
      console.error(err);
      onActionToast("Error indexing document.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const filteredDocs = docs.filter(doc => 
    doc.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
    doc.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-8 fade-in-up">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-neutral-900 pb-6">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold tracking-tight text-white mb-1">Knowledge Base Management</h1>
          <p className="text-sm text-neutral-400">Index reference documentation, SOP manuals, and historic post-mortems into the Chroma RAG pipeline.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Form to add runbooks */}
        <div className="lg:col-span-1 space-y-6">
          <section className="glass-card p-6 relative overflow-hidden group">
            <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-[#7C5CFF]/40 to-transparent"></div>
            
            <div className="flex items-center space-x-2.5 mb-6">
              <Plus className="w-4 h-4 text-[#7C5CFF]" />
              <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-200 font-sans">Index New Reference</h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-neutral-400 mb-1.5">Document Title</label>
                <input 
                  type="text" 
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  placeholder="e.g., SOP-200: Kafka Broker Tuning"
                  className="w-full bg-neutral-950/60 border border-neutral-800 rounded-xl px-3.5 py-2.5 text-xs text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-[#7C5CFF]/50 transition-colors"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-neutral-400 mb-1.5">Source Provider</label>
                <select 
                  value={source}
                  onChange={(e) => setSource(e.target.value)}
                  className="w-full bg-neutral-950/60 border border-neutral-800 rounded-xl px-3.5 py-2.5 text-xs text-neutral-200 focus:outline-none focus:border-[#7C5CFF]/50 transition-colors"
                >
                  <option value="Confluence Runbooks">Confluence Runbooks</option>
                  <option value="Internal Architecture Guides">Internal Architecture Guides</option>
                  <option value="Kubernetes On-Call Manuals">Kubernetes On-Call Manuals</option>
                  <option value="Post-Mortem Analysis">Post-Mortem Analysis</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-neutral-400 mb-1.5">SOP Content / Runbook Markdown</label>
                <textarea 
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  required
                  rows="8"
                  placeholder="Paste details of troubleshooting metrics, parameters, steps, and threshold rules..."
                  className="w-full bg-neutral-950/60 border border-neutral-800 rounded-xl px-3.5 py-2.5 text-xs text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-[#7C5CFF]/50 transition-colors resize-none"
                />
              </div>

              <button 
                type="submit" 
                disabled={isSubmitting || !title.trim() || !content.trim()}
                className="w-full py-2.5 rounded-xl bg-gradient-to-r from-[#7C5CFF] to-[#4F8CFF] text-white text-xs font-semibold hover:opacity-90 transition-all shadow-lg shadow-indigo-500/10 cursor-pointer disabled:opacity-50"
              >
                {isSubmitting ? 'Embedding & Saving...' : 'Index Runbook'}
              </button>
            </form>
          </section>
        </div>

        {/* List of indexed runbooks */}
        <div className="lg:col-span-2 space-y-6">
          <div className="glass-card p-6 space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-neutral-900 pb-4">
              <div className="flex items-center space-x-2.5">
                <Database className="w-4 h-4 text-[#4F8CFF]" />
                <h3 className="text-sm font-semibold text-white">Indexed RAG References ({filteredDocs.length})</h3>
              </div>
              <div className="relative max-w-xs w-full">
                <Search className="w-3.5 h-3.5 text-neutral-500 absolute left-3 top-1/2 -translate-y-1/2" />
                <input 
                  type="text" 
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search index..."
                  className="w-full bg-neutral-950/60 border border-neutral-800 rounded-xl pl-9 pr-3.5 py-1.5 text-xs text-neutral-200 placeholder-neutral-600 focus:outline-none focus:border-[#4F8CFF]/50 transition-colors"
                />
              </div>
            </div>

            <div className="space-y-4 max-h-[550px] overflow-y-auto no-scrollbar pr-1">
              {filteredDocs.length > 0 ? (
                filteredDocs.map((doc) => (
                  <div key={doc.id} className="p-4 bg-neutral-950/60 border border-neutral-900 rounded-xl space-y-3 hover:border-neutral-800 transition-colors">
                    <div className="flex justify-between items-start">
                      <div className="flex items-center gap-2">
                        <BookOpen className="w-3.5 h-3.5 text-[#7C5CFF]" />
                        <span className="text-xs font-semibold text-white">{doc.title}</span>
                      </div>
                      <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-500/10 text-[#4F8CFF] font-medium uppercase">
                        {doc.source}
                      </span>
                    </div>
                    <p className="text-[11px] text-neutral-400 font-mono leading-relaxed bg-[#050505] p-3 rounded border border-neutral-900/40">
                      {doc.content}
                    </p>
                  </div>
                ))
              ) : (
                <div className="text-center py-20 text-neutral-500 text-xs">
                  No documents found in the database. Add one to test the ingestion pipeline!
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
