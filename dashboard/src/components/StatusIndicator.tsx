import React from 'react';
import { Database, RefreshCw } from 'lucide-react';
import { HealthResponse } from '../types/api';

interface StatusIndicatorProps {
  health: HealthResponse | null;
  loading: boolean;
  onRefresh: () => void;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({ health, loading, onRefresh }) => {
  const isConnected = health?.database === 'connected' && health?.status === 'healthy';

  return (
    <div className="p-3 bg-background-card rounded-lg border border-border-subtle flex items-center justify-between text-xs">
      <div className="flex items-center space-x-2.5">
        <div className="relative flex items-center justify-center">
          <div
            className={`w-2 h-2 rounded-full ${
              isConnected ? 'bg-status-success' : 'bg-status-error'
            }`}
          />
          {isConnected && (
            <div className="absolute w-2 h-2 rounded-full bg-status-success animate-ping opacity-75" />
          )}
        </div>
        <div>
          <div className="flex items-center space-x-1.5 font-medium text-content-primary">
            <Database className="w-3.5 h-3.5 text-content-secondary" />
            <span>PostgreSQL</span>
          </div>
          <div className="text-[11px] text-content-secondary">
            {loading ? 'Checking...' : isConnected ? 'Connected & Verified' : 'Disconnected'}
          </div>
        </div>
      </div>
      <button
        onClick={onRefresh}
        disabled={loading}
        title="Check database connection"
        className="p-1 text-content-secondary hover:text-content-primary hover:bg-background-hover rounded transition-colors disabled:opacity-50"
      >
        <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
      </button>
    </div>
  );
};
