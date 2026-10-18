import React from 'react';
import { Menu, Sparkles, Database } from 'lucide-react';
import { HealthResponse } from '../types/api';

interface HeaderProps {
  onOpenMobileMenu: () => void;
  health: HealthResponse | null;
}

export const Header: React.FC<HeaderProps> = ({ onOpenMobileMenu, health }) => {
  const isConnected = health?.database === 'connected' && health?.status === 'healthy';

  return (
    <header className="border-b border-border-subtle bg-background-card/40 backdrop-blur-md sticky top-0 z-30 px-4 sm:px-6 py-3.5 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <button
          onClick={onOpenMobileMenu}
          className="p-1.5 rounded-lg text-content-secondary hover:text-content-primary hover:bg-background-hover md:hidden transition-colors"
          title="Open Menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-sm sm:text-base font-bold text-content-primary tracking-tight">
              Ask your data. Discover the why.
            </h1>
            <span className="hidden sm:inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] font-semibold bg-accent-muted text-accent border border-accent/25">
              <Sparkles className="w-3 h-3" />
              <span>v1.0 Production</span>
            </span>
          </div>
          <p className="text-xs text-content-secondary hidden sm:block">
            Explore business performance using natural language and trusted analytical results.
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <div className="flex items-center space-x-2 px-2.5 py-1 rounded-full bg-background-surface border border-border-subtle text-[11px] font-medium text-content-secondary">
          <div
            className={`w-2 h-2 rounded-full ${
              isConnected ? 'bg-status-success' : 'bg-status-error'
            }`}
          />
          <Database className="w-3 h-3 text-content-muted" />
          <span className="hidden sm:inline">PostgreSQL:</span>
          <span className={isConnected ? 'text-status-success' : 'text-status-error'}>
            {isConnected ? 'Online' : 'Offline'}
          </span>
        </div>
      </div>
    </header>
  );
};
