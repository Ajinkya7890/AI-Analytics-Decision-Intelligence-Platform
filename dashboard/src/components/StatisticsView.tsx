import React from 'react';
import { Sigma } from 'lucide-react';

interface StatisticsViewProps {
  statistics?: Record<string, number | null> | null;
}

export const StatisticsView: React.FC<StatisticsViewProps> = ({ statistics }) => {
  if (!statistics) return null;

  const statEntries = [
    { label: 'Sample Count', value: statistics.count, format: (v: number) => v.toString() },
    { label: 'Mean', value: statistics.mean, format: (v: number) => v.toFixed(2) },
    { label: 'Median', value: statistics.median, format: (v: number) => v.toFixed(2) },
    { label: 'Std. Deviation', value: statistics.standard_deviation, format: (v: number) => v.toFixed(2) },
    { label: 'Variance', value: statistics.variance, format: (v: number) => v.toFixed(2) },
    { label: 'Minimum', value: statistics.minimum, format: (v: number) => v.toFixed(2) },
    { label: 'Maximum', value: statistics.maximum, format: (v: number) => v.toFixed(2) },
    { label: '25th Percentile', value: statistics.percentile_25, format: (v: number) => v.toFixed(2) },
    { label: '75th Percentile', value: statistics.percentile_75, format: (v: number) => v.toFixed(2) },
  ].filter(item => item.value !== null && item.value !== undefined && !isNaN(item.value));

  if (statEntries.length === 0) return null;

  return (
    <div className="bg-background-card border border-border-subtle rounded-xl p-4 shadow-panel space-y-3">
      <div className="flex items-center space-x-2">
        <Sigma className="w-4 h-4 text-accent" />
        <h3 className="text-xs font-semibold text-content-primary tracking-tight">
          Descriptive Statistical Distribution
        </h3>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5">
        {statEntries.map((stat, idx) => (
          <div
            key={idx}
            className="p-2.5 bg-background-surface/80 rounded-lg border border-border-subtle/60"
          >
            <div className="text-[10px] text-content-muted font-medium truncate uppercase">
              {stat.label}
            </div>
            <div className="text-sm font-semibold font-mono text-content-primary mt-0.5">
              {stat.format(stat.value!)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
