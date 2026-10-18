import React from 'react';
import { Clock, Rows, Target, Zap } from 'lucide-react';
import { QueryResponse } from '../types/api';

interface ResultSummaryProps {
  result: QueryResponse;
}

export const ResultSummary: React.FC<ResultSummaryProps> = ({ result }) => {
  return (
    <div className="p-4 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-3">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div>
          <span className="text-[10px] font-semibold tracking-wider text-accent uppercase block mb-1">
            Active Query Result
          </span>
          <h2 className="text-base font-semibold text-content-primary tracking-tight">
            "{result.question}"
          </h2>
        </div>

        <div className="flex items-center flex-wrap gap-2 text-xs">
          <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-background-surface border border-border-subtle text-content-secondary font-mono text-[11px]">
            <Rows className="w-3.5 h-3.5 text-accent" />
            <span>{result.row_count} {result.row_count === 1 ? 'row' : 'rows'}</span>
          </div>

          <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-background-surface border border-border-subtle text-content-secondary font-mono text-[11px]">
            <Clock className="w-3.5 h-3.5 text-accent" />
            <span>{result.execution_time_ms} ms</span>
          </div>

          {result.intent && (
            <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-accent-muted border border-accent/25 text-accent font-medium text-[11px] capitalize">
              <Zap className="w-3 h-3" />
              <span>{result.intent.replace('_', ' ')}</span>
            </div>
          )}

          {result.target_entity && (
            <div className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-md bg-background-surface border border-border-subtle text-content-secondary text-[11px] capitalize">
              <Target className="w-3 h-3 text-content-muted" />
              <span>{result.target_entity}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
