import React, { useState } from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import { BarChart3, LineChart as LineIcon } from 'lucide-react';
import { QueryResponse } from '../types/api';
import { formatDateLabel, formatCurrency, formatPercentage, formatDays, formatNumber, isIsoDateString } from '../utils/formatters';

interface ChartViewProps {
  result: QueryResponse;
}

export const ChartView: React.FC<ChartViewProps> = ({ result }) => {
  const { columns, rows } = result;

  // Visualizations require at least 2 rows and 2 columns
  if (!rows || rows.length <= 1 || columns.length < 2) {
    return null;
  }

  // Find numeric metric column
  let metricColIndex = -1;
  let maxNumericCount = 0;
  columns.forEach((_, colIdx) => {
    const numCount = rows.filter(r => typeof r[colIdx] === 'number').length;
    if (numCount > maxNumericCount) {
      maxNumericCount = numCount;
      metricColIndex = colIdx;
    }
  });

  // Find label column (or date column)
  const dateColIndex = columns.findIndex((col, idx) => {
    if (idx === metricColIndex) return false;
    const colLower = col.toLowerCase();
    const isNamedDate = colLower.includes('month') || colLower.includes('date') || colLower.includes('year') || colLower.includes('period');
    const hasIsoSample = rows.some(r => isIsoDateString(r[idx]));
    return isNamedDate || hasIsoSample;
  });

  const isTimeSeries = dateColIndex !== -1;
  const labelColIndex = isTimeSeries ? dateColIndex : columns.findIndex((_, idx) => idx !== metricColIndex);

  if (metricColIndex === -1 || labelColIndex === -1) {
    return null;
  }

  const labelCol = columns[labelColIndex];
  const metricCol = columns[metricColIndex];

  const [chartType, setChartType] = useState<'auto' | 'bar' | 'line'>('auto');
  const activeMode = chartType === 'auto' ? (isTimeSeries ? 'line' : 'bar') : chartType;

  // Process rows: For time-series, ensure chronological sort
  let processedRows = [...rows];
  if (isTimeSeries) {
    processedRows.sort((a, b) => {
      const valA = String(a[labelColIndex] ?? '');
      const valB = String(b[labelColIndex] ?? '');
      return valA.localeCompare(valB);
    });
  }

  // Format data for Recharts, strictly preserving null/undefined without defaulting to 0
  const chartData = processedRows.map((r, i) => {
    const rawLabel = r[labelColIndex];
    let displayLabel = String(rawLabel ?? `Row ${i + 1}`);
    let fullTooltipLabel = String(rawLabel ?? `Row ${i + 1}`);

    if (isTimeSeries && isIsoDateString(rawLabel)) {
      displayLabel = formatDateLabel(rawLabel, 'shortMonthYear');
      fullTooltipLabel = formatDateLabel(rawLabel, 'fullMonthYear');
    } else if (displayLabel.length > 20) {
      displayLabel = `${displayLabel.substring(0, 10)}...`;
    }

    // Preserve exact numeric value or null (never convert null to 0!)
    const rawVal = r[metricColIndex];
    const numericVal = typeof rawVal === 'number' && !isNaN(rawVal) ? rawVal : null;

    return {
      name: displayLabel,
      fullName: fullTooltipLabel,
      value: numericVal,
    };
  });

  const formatTooltipValue = (val: any) => {
    if (val === null || val === undefined) {
      return 'No data available';
    }
    if (typeof val === 'number') {
      const colLower = metricCol.toLowerCase();
      if (colLower.includes('revenue') || colLower.includes('sales') || colLower.includes('price') || colLower.includes('spend') || colLower.includes('value')) {
        return formatCurrency(val);
      }
      if (colLower.includes('rate') || colLower.includes('percentage') || colLower.includes('percent')) {
        return formatPercentage(val);
      }
      if (colLower.includes('days') || colLower.includes('time')) {
        return formatDays(val);
      }
      return formatNumber(val);
    }
    return String(val);
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-[#18181F] border border-[#2A2A35] shadow-elevated p-3 rounded-lg text-xs space-y-1">
          <p className="text-content-secondary font-medium">{data.fullName}</p>
          <p className="text-sm font-bold text-accent">
            {formatTooltipValue(data.value)}
          </p>
          <p className="text-[10px] text-content-muted capitalize">
            {metricCol.replace(/_/g, ' ')}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-background-card border border-border-subtle rounded-xl p-4 shadow-panel space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xs font-semibold text-content-primary capitalize tracking-tight">
            Visual Analysis: {metricCol.replace(/_/g, ' ')} by {labelCol.replace(/_/g, ' ')}
          </h3>
          <p className="text-[11px] text-content-muted">
            {activeMode === 'bar' ? 'Comparative distribution' : 'Chronological trend evolution'}
          </p>
        </div>

        <div className="flex items-center space-x-1 bg-background-surface p-1 rounded-lg border border-border-subtle text-xs">
          <button
            onClick={() => setChartType('bar')}
            className={`p-1.5 rounded flex items-center space-x-1 text-[11px] transition-colors ${
              activeMode === 'bar'
                ? 'bg-accent text-white font-medium'
                : 'text-content-secondary hover:text-content-primary'
            }`}
            title="Bar Chart"
          >
            <BarChart3 className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Bar</span>
          </button>
          <button
            onClick={() => setChartType('line')}
            className={`p-1.5 rounded flex items-center space-x-1 text-[11px] transition-colors ${
              activeMode === 'line'
                ? 'bg-accent text-white font-medium'
                : 'text-content-secondary hover:text-content-primary'
            }`}
            title="Line/Area Trend Chart"
          >
            <LineIcon className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Trend</span>
          </button>
        </div>
      </div>

      <div className="h-64 sm:h-72 w-full pt-2">
        <ResponsiveContainer width="100%" height="100%">
          {activeMode === 'bar' ? (
            <BarChart
              data={chartData}
              layout={!isTimeSeries && chartData.length > 5 ? 'vertical' : 'horizontal'}
              margin={{ top: 10, right: 20, left: 20, bottom: 20 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#22222C" horizontal={true} vertical={false} />
              {!isTimeSeries && chartData.length > 5 ? (
                <>
                  <XAxis
                    type="number"
                    stroke="#6C6C78"
                    fontSize={11}
                    tickFormatter={(v) => (v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v)}
                  />
                  <YAxis
                    dataKey="name"
                    type="category"
                    stroke="#6C6C78"
                    fontSize={11}
                    width={110}
                    tickLine={false}
                  />
                </>
              ) : (
                <>
                  <XAxis
                    dataKey="name"
                    stroke="#6C6C78"
                    fontSize={11}
                    tickLine={false}
                    interval={isTimeSeries && chartData.length > 12 ? Math.ceil(chartData.length / 8) : 0}
                  />
                  <YAxis
                    stroke="#6C6C78"
                    fontSize={11}
                    tickFormatter={(v) => (v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v)}
                  />
                </>
              )}
              <Tooltip content={<CustomTooltip />} />
              <Bar
                dataKey="value"
                fill="#8B7CFF"
                radius={!isTimeSeries && chartData.length > 5 ? [0, 4, 4, 0] : [4, 4, 0, 0]}
                maxBarSize={32}
              />
            </BarChart>
          ) : (
            <AreaChart data={chartData} margin={{ top: 10, right: 20, left: 10, bottom: 20 }}>
              <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8B7CFF" stopOpacity={0.35} />
                  <stop offset="95%" stopColor="#8B7CFF" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#22222C" vertical={false} />
              <XAxis
                dataKey="name"
                stroke="#6C6C78"
                fontSize={11}
                tickLine={false}
                interval={chartData.length > 12 ? Math.ceil(chartData.length / 8) : 0}
              />
              <YAxis
                stroke="#6C6C78"
                fontSize={11}
                tickFormatter={(v) => (v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v)}
              />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#8B7CFF"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorValue)"
                connectNulls={false}
              />
            </AreaChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
};
