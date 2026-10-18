import React, { useState, useEffect, useCallback } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { QueryComposer } from './components/QueryComposer';
import { SuggestedQuestions } from './components/SuggestedQuestions';
import { ResultSummary } from './components/ResultSummary';
import { MetricCards } from './components/MetricCards';
import { ChartView } from './components/ChartView';
import { DataTable } from './components/DataTable';
import { SqlInspector } from './components/SqlInspector';
import { StatisticsView } from './components/StatisticsView';
import { QueryHistoryView } from './components/QueryHistoryView';
import { checkHealth, submitQuery, getQueryHistory } from './services/api';
import { HealthResponse, QueryResponse, HistoryEntry } from './types/api';
import { Sparkles, Layers, ShieldCheck, Database, Server, RefreshCw } from 'lucide-react';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<'ask' | 'history' | 'overview' | 'settings'>('ask');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Health state
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState(false);

  // History state
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  // Query state
  const [question, setQuestion] = useState('');
  const [queryLoading, setQueryLoading] = useState(false);
  const [queryError, setQueryError] = useState<string | null>(null);
  const [result, setResult] = useState<QueryResponse | null>(null);

  // Health fetch
  const refreshHealth = useCallback(async () => {
    setHealthLoading(true);
    const data = await checkHealth();
    setHealth(data);
    setHealthLoading(false);
  }, []);

  // History fetch
  const refreshHistory = useCallback(async () => {
    setHistoryLoading(true);
    const res = await getQueryHistory();
    setHistory(res.entries);
    setHistoryLoading(false);
  }, []);

  useEffect(() => {
    refreshHealth();
    refreshHistory();
  }, [refreshHealth, refreshHistory]);

  // Execute query handler
  const handleRunQuery = async (queryText?: string) => {
    const q = (queryText || question).trim();
    if (!q || queryLoading) return;

    setQuestion(q);
    setQueryLoading(true);
    setQueryError(null);

    try {
      const data = await submitQuery(q);
      setResult(data);
      setCurrentTab('ask');
      // Refresh history in background
      refreshHistory();
    } catch (err: any) {
      setQueryError(err.message || 'Failed to execute query.');
      refreshHistory();
    } finally {
      setQueryLoading(false);
    }
  };

  const handleNewAnalysis = () => {
    setQuestion('');
    setResult(null);
    setQueryError(null);
    setCurrentTab('ask');
  };

  return (
    <div className="min-h-screen bg-background text-content-primary flex flex-col md:flex-row font-sans">
      {/* Sidebar */}
      <Sidebar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        onNewAnalysis={handleNewAnalysis}
        health={health}
        healthLoading={healthLoading}
        onRefreshHealth={refreshHealth}
        historyCount={history.length}
        isOpen={mobileMenuOpen}
        onCloseMobile={() => setMobileMenuOpen(false)}
      />

      {/* Main Content Area */}
      <div className="flex-1 md:pl-64 flex flex-col min-h-screen">
        <Header
          onOpenMobileMenu={() => setMobileMenuOpen(true)}
          health={health}
        />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto space-y-6">
          {currentTab === 'ask' && (
            <div className="space-y-6">
              {/* Query Composer Box */}
              <QueryComposer
                question={question}
                setQuestion={setQuestion}
                onSubmit={() => handleRunQuery()}
                loading={queryLoading}
                error={queryError}
                onClearError={() => setQueryError(null)}
              />

              {/* Suggestions */}
              {!result && !queryLoading && (
                <SuggestedQuestions
                  onSelectQuestion={(q) => handleRunQuery(q)}
                  disabled={queryLoading}
                />
              )}

              {/* Loading Skeleton */}
              {queryLoading && (
                <div className="p-8 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-4 animate-pulse">
                  <div className="h-4 bg-background-surface rounded w-1/3" />
                  <div className="h-8 bg-background-surface rounded w-2/3" />
                  <div className="grid grid-cols-3 gap-3 pt-4">
                    <div className="h-20 bg-background-surface rounded" />
                    <div className="h-20 bg-background-surface rounded" />
                    <div className="h-20 bg-background-surface rounded" />
                  </div>
                </div>
              )}

              {/* Result Presentation */}
              {result && !queryLoading && (
                <div className="space-y-6 animate-fadeIn">
                  {/* Summary & KPI Cards */}
                  <ResultSummary result={result} />
                  <MetricCards result={result} />

                  {/* Visual Chart */}
                  <ChartView result={result} />

                  {/* Raw Interactive Data Table */}
                  <DataTable result={result} />

                  {/* Descriptive Statistical Distribution if present */}
                  {result.statistics && <StatisticsView statistics={result.statistics} />}

                  {/* Expandable Monospace SQL Inspector */}
                  <SqlInspector sql={result.sql} validation={result.validation} />
                </div>
              )}
            </div>
          )}

          {currentTab === 'history' && (
            <QueryHistoryView
              history={history}
              loading={historyLoading}
              onSelectQuestion={(q) => {
                setQuestion(q);
                setCurrentTab('ask');
                handleRunQuery(q);
              }}
              onRefresh={refreshHistory}
            />
          )}

          {currentTab === 'overview' && (
            <div className="bg-background-card border border-border-subtle rounded-xl p-6 shadow-panel space-y-6">
              <div>
                <h2 className="text-base font-bold text-content-primary tracking-tight">
                  Platform Architecture Overview
                </h2>
                <p className="text-xs text-content-secondary mt-1">
                  AI Analytics & Decision Intelligence combines deterministic analytical planning with high-performance PostgreSQL execution.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-background-surface border border-border-subtle rounded-lg space-y-2">
                  <div className="w-8 h-8 rounded bg-accent-muted border border-accent/30 flex items-center justify-center text-accent">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <h3 className="text-xs font-semibold text-content-primary">
                    Natural-Language Analyzer
                  </h3>
                  <p className="text-xs text-content-secondary leading-relaxed">
                    Classifies business intent, resolves target dimensions (Product, Category, Seller, Time), and extracts ranking limits deterministically.
                  </p>
                </div>

                <div className="p-4 bg-background-surface border border-border-subtle rounded-lg space-y-2">
                  <div className="w-8 h-8 rounded bg-status-success-bg border border-status-success/30 flex items-center justify-center text-status-success">
                    <ShieldCheck className="w-4 h-4" />
                  </div>
                  <h3 className="text-xs font-semibold text-content-primary">
                    SQL Guardrails & Verification
                  </h3>
                  <p className="text-xs text-content-secondary leading-relaxed">
                    Strict read-only verification ensures all generated queries are SELECT/WITH statements without mutations, multiple statements, or comments.
                  </p>
                </div>

                <div className="p-4 bg-background-surface border border-border-subtle rounded-lg space-y-2">
                  <div className="w-8 h-8 rounded bg-accent-muted border border-accent/30 flex items-center justify-center text-accent">
                    <Database className="w-4 h-4" />
                  </div>
                  <h3 className="text-xs font-semibold text-content-primary">
                    PostgreSQL Star Schema
                  </h3>
                  <p className="text-xs text-content-secondary leading-relaxed">
                    Queries execute against optimized analytics marts and fact tables across 100k+ enterprise orders and dimension hierarchies.
                  </p>
                </div>
              </div>

              <div className="pt-2 border-t border-border-subtle flex items-center justify-between">
                <button
                  onClick={() => setCurrentTab('ask')}
                  className="px-4 py-2 bg-accent hover:bg-accent-hover text-white text-xs font-semibold rounded-lg transition-colors flex items-center space-x-2"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Start Asking Data</span>
                </button>
              </div>
            </div>
          )}

          {currentTab === 'settings' && (
            <div className="bg-background-card border border-border-subtle rounded-xl p-6 shadow-panel space-y-6">
              <div>
                <h2 className="text-base font-bold text-content-primary tracking-tight">
                  System Settings & Connectivity
                </h2>
                <p className="text-xs text-content-secondary mt-1">
                  Active environment runtime status and configurations.
                </p>
              </div>

              <div className="space-y-3 font-mono text-xs">
                <div className="p-3 bg-background-surface rounded-lg border border-border-subtle flex items-center justify-between">
                  <div className="flex items-center space-x-2 font-sans text-content-secondary">
                    <Server className="w-4 h-4 text-accent" />
                    <span>FastAPI Backend Gateway</span>
                  </div>
                  <span className="text-accent font-semibold">http://127.0.0.1:8000</span>
                </div>

                <div className="p-3 bg-background-surface rounded-lg border border-border-subtle flex items-center justify-between">
                  <div className="flex items-center space-x-2 font-sans text-content-secondary">
                    <Database className="w-4 h-4 text-status-success" />
                    <span>PostgreSQL Database Connectivity</span>
                  </div>
                  <span className={health?.database === 'connected' ? 'text-status-success' : 'text-status-error'}>
                    {health?.database === 'connected' ? 'Connected (Verified)' : 'Disconnected'}
                  </span>
                </div>

                <div className="p-3 bg-background-surface rounded-lg border border-border-subtle flex items-center justify-between">
                  <div className="flex items-center space-x-2 font-sans text-content-secondary">
                    <Layers className="w-4 h-4 text-content-muted" />
                    <span>API Version</span>
                  </div>
                  <span className="text-content-primary">{health?.version || '1.0.0'}</span>
                </div>
              </div>

              <div className="pt-2 border-t border-border-subtle flex items-center space-x-3">
                <button
                  onClick={refreshHealth}
                  disabled={healthLoading}
                  className="px-3.5 py-2 bg-background-surface hover:bg-background-hover border border-border-subtle text-content-primary text-xs font-medium rounded-lg transition-colors flex items-center space-x-2 disabled:opacity-50"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${healthLoading ? 'animate-spin' : ''}`} />
                  <span>Test Backend Ping</span>
                </button>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};
