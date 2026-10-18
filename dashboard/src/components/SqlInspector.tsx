import React, { useState } from 'react';
import { Code2, ChevronDown, ChevronUp, Copy, Check, ShieldCheck } from 'lucide-react';

interface SqlInspectorProps {
  sql: string;
  validation?: string | null;
}

export const SqlInspector: React.FC<SqlInspectorProps> = ({ sql, validation }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(sql);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy SQL', err);
    }
  };

  if (!sql) return null;

  return (
    <div className="bg-background-card border border-border-subtle rounded-xl shadow-panel overflow-hidden transition-all">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-3.5 flex items-center justify-between text-left hover:bg-background-hover/50 transition-colors"
      >
        <div className="flex items-center space-x-2.5">
          <div className="w-6 h-6 rounded bg-background-surface flex items-center justify-center text-accent">
            <Code2 className="w-3.5 h-3.5" />
          </div>
          <div>
            <span className="text-xs font-semibold text-content-primary">
              Generated SQL Query
            </span>
            <span className="text-[11px] text-content-muted ml-2">
              (Deterministic PostgreSQL template)
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          {validation && (
            <div className="hidden sm:inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] font-medium bg-status-success-bg text-status-success border border-status-success/20">
              <ShieldCheck className="w-3 h-3" />
              <span>{validation}</span>
            </div>
          )}
          <span className="text-content-secondary">
            {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </span>
        </div>
      </button>

      {isOpen && (
        <div className="p-4 pt-1 border-t border-border-subtle/60 bg-[#0E0E12] space-y-3">
          <div className="flex items-center justify-between text-xs text-content-secondary">
            <span className="text-[11px] text-content-muted font-mono">
              PostgreSQL Read-Only Dialect
            </span>
            <button
              onClick={handleCopy}
              className="px-2.5 py-1 rounded bg-background-surface hover:bg-background-hover border border-border-subtle text-content-primary flex items-center space-x-1.5 transition-colors text-[11px]"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-status-success" />
                  <span className="text-status-success font-medium">Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>Copy SQL</span>
                </>
              )}
            </button>
          </div>

          <pre className="p-3 bg-background-card rounded-lg border border-border-subtle/80 overflow-x-auto text-[12px] font-mono leading-relaxed text-[#D4D4DE] selection:bg-accent/30">
            <code>{sql}</code>
          </pre>
        </div>
      )}
    </div>
  );
};
