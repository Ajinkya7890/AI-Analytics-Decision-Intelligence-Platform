import React from 'react';
import {
  Sparkles,
  PlusCircle,
  History,
  LayoutDashboard,
  Settings,
  BookmarkCheck,
  X,
  Layers,
} from 'lucide-react';
import { HealthResponse } from '../types/api';
import { StatusIndicator } from './StatusIndicator';

interface SidebarProps {
  currentTab: 'ask' | 'history' | 'overview' | 'settings';
  setCurrentTab: (tab: 'ask' | 'history' | 'overview' | 'settings') => void;
  onNewAnalysis: () => void;
  health: HealthResponse | null;
  healthLoading: boolean;
  onRefreshHealth: () => void;
  historyCount: number;
  isOpen: boolean;
  onCloseMobile: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  setCurrentTab,
  onNewAnalysis,
  health,
  healthLoading,
  onRefreshHealth,
  historyCount,
  isOpen,
  onCloseMobile,
}) => {
  const navItems = [
    { id: 'ask', label: 'Ask Data', icon: Sparkles },
    { id: 'history', label: 'Query History', icon: History, badge: historyCount > 0 ? historyCount : undefined },
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/70 z-40 md:hidden backdrop-blur-sm transition-opacity"
          onClick={onCloseMobile}
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-background-sidebar border-r border-border-subtle flex flex-col justify-between transition-transform duration-200 ease-in-out md:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand Header */}
        <div className="p-5 border-b border-border-subtle">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-lg bg-accent/15 border border-accent/30 flex items-center justify-center text-accent shadow-sm">
                <Layers className="w-4 h-4" />
              </div>
              <div>
                <h1 className="text-sm font-semibold tracking-tight text-content-primary">
                  AI Analytics
                </h1>
                <p className="text-[11px] font-medium text-accent tracking-wide uppercase">
                  Decision Intelligence
                </p>
              </div>
            </div>
            <button
              onClick={onCloseMobile}
              className="p-1 text-content-secondary hover:text-content-primary md:hidden rounded hover:bg-background-hover"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* New Analysis Action */}
          <button
            onClick={() => {
              onNewAnalysis();
              setCurrentTab('ask');
              onCloseMobile();
            }}
            className="w-full mt-4 py-2 px-3 bg-accent text-white font-medium text-xs rounded-lg hover:bg-accent-hover transition-colors flex items-center justify-center space-x-2 shadow-sm"
          >
            <PlusCircle className="w-4 h-4" />
            <span>New Analysis</span>
          </button>
        </div>

        {/* Navigation Items */}
        <div className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          <div className="px-3 pb-2 text-[10px] font-semibold tracking-wider text-content-muted uppercase">
            Platform Navigation
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  setCurrentTab(item.id as any);
                  onCloseMobile();
                }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                  isActive
                    ? 'bg-accent-muted text-accent font-semibold border border-accent/25'
                    : 'text-content-secondary hover:text-content-primary hover:bg-background-hover'
                }`}
              >
                <div className="flex items-center space-x-2.5">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-accent' : 'text-content-secondary'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge !== undefined && (
                  <span className="px-1.5 py-0.5 rounded-full text-[10px] bg-background-surface text-content-secondary border border-border-subtle font-mono">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}

          <div className="pt-4 px-3 pb-2 text-[10px] font-semibold tracking-wider text-content-muted uppercase">
            Workspaces
          </div>
          <div className="px-3 py-2 text-xs text-content-muted flex items-center space-x-2 cursor-not-allowed">
            <BookmarkCheck className="w-4 h-4 opacity-40" />
            <span>Saved Insights</span>
            <span className="ml-auto text-[9px] px-1.5 py-0.5 rounded bg-background-surface border border-border-subtle text-content-muted">
              v1.1
            </span>
          </div>
        </div>

        {/* Database Status Footer */}
        <div className="p-4 border-t border-border-subtle bg-background-sidebar">
          <StatusIndicator
            health={health}
            loading={healthLoading}
            onRefresh={onRefreshHealth}
          />
        </div>
      </aside>
    </>
  );
};
