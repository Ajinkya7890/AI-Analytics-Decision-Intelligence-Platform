import React from 'react';
import { History, CheckCircle2, AlertCircle, Clock, Rows, ArrowUpRight, Info } from 'lucide-react';
import { HistoryEntry } from '../types/api';

interface QueryHistoryViewProps {
  history: HistoryEntry[];
  loading: boolean;
  onSelectQuestion: (question: string) => void;
  onRefresh: () => void;
}

function formatTimestamp(isoStr: string): string {
  try {
    const d = new Date(isoStr);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  } catch {
    return isoStr;
  }
}

export const QueryHistoryView: React.FC<QueryHistoryViewProps> = ({
  history,
  loading,
  onSelectQuestion,
}) => {
  return (
    <div className="bg-background-card border border-border-subtle rounded-xl p-5 shadow-panel space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border-subtle pb-4">
        <div>
          <div className="flex items-center space-x-2">
            <History className="w-4 h-4 text-accent" />
            <h2 className="text-sm font-semibold text-content-primary tracking-tight">
              Session Query History
            </h2>
          </div>
          <p className="text-xs text-content-secondary mt-0.5">
            Past analyses executed during the current active backend session (newest first).
          </p>
        </div>

        <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-background-surface border border-border-subtle text-[11px] text-content-muted">
          <Info className="w-3.5 h-3.5" />
          <span>Resets on server restart</span>
        </div>
      </div>

      {loading && history.length === 0 ? (
        <div className="py-12 text-center text-xs text-content-muted">
          Loading query history...
        </div>
      ) : history.length === 0 ? (
        <div className="py-12 text-center space-y-2">
          <History className="w-8 h-8 text-content-muted/40 mx-auto" />
          <p className="text-xs text-content-secondary font-medium">No queries executed yet in this session.</p>
          <p className="text-[11px] text-content-muted">
            Ask a business question in the composer above to begin tracking history.
          </p>
        </div>
      ) : (
        <div className="space-y-2 divide-y divide-border-subtle/40">
          {history.map((entry) => (
            <div
              key={entry.id}
              onClick={() => onSelectQuestion(entry.question)}
              className="pt-2.5 first:pt-0 flex items-start justify-between gap-3 p-2.5 hover:bg-background-hover/70 rounded-lg cursor-pointer transition-colors group"
            >
              <div className="flex items-start space-x-3">
                <div className="mt-0.5">
                  {entry.success ? (
                    <CheckCircle2 className="w-4 h-4 text-status-success flex-shrink-0" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-status-error flex-shrink-0" />
                  )}
                </div>
                <div className="space-y-1">
                  <p className="text-xs font-medium text-content-primary group-hover:text-white transition-colors">
                    {entry.question}
                  </p>
                  {entry.error_message && (
                    <p className="text-[11px] text-status-error font-mono">
                      Error: {entry.error_message}
                    </p>
                  )}
                  <div className="flex items-center space-x-3 text-[10px] text-content-muted font-mono">
                    <span className="flex items-center space-x-1">
                      <Clock className="w-3 h-3 text-content-muted" />
                      <span>{formatTimestamp(entry.timestamp)}</span>
                    </span>
                    {entry.execution_time_ms !== null && entry.execution_time_ms !== undefined && (
                      <span>{entry.execution_time_ms} ms</span>
                    )}
                    {entry.row_count !== null && entry.row_count !== undefined && (
                      <span className="flex items-center space-x-1">
                        <Rows className="w-3 h-3 text-content-muted" />
                        <span>{entry.row_count} rows</span>
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <button
                className="opacity-0 group-hover:opacity-100 p-1.5 rounded bg-background-surface hover:bg-accent hover:text-white text-content-secondary transition-all"
                title="Rerun query"
              >
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
