import React from 'react';
import { Award, TrendingUp, BarChart2, Activity, Calendar } from 'lucide-react';
import { QueryResponse } from '../types/api';
import { formatDateLabel, formatCurrency, formatPercentage, formatDays, formatNumber, isIsoDateString } from '../utils/formatters';

interface MetricCardsProps {
  result: QueryResponse;
}

function formatMetricValue(value: any, columnName: string): string {
  if (value === null || value === undefined) return 'N/A';
  if (typeof value === 'number') {
    const colLower = columnName.toLowerCase();
    if (colLower.includes('rate') || colLower.includes('percentage') || colLower.includes('percent')) {
      return formatPercentage(value);
    }
    if (colLower.includes('revenue') || colLower.includes('sales') || colLower.includes('price') || colLower.includes('spend') || colLower.includes('value')) {
      return formatCurrency(value);
    }
    if (colLower.includes('days') || colLower.includes('time')) {
      return formatDays(value);
    }
    return formatNumber(value);
  }
  if (isIsoDateString(value)) {
    return formatDateLabel(value, 'shortMonthYear');
  }
  return String(value);
}

export const MetricCards: React.FC<MetricCardsProps> = ({ result }) => {
  const { columns, rows, statistics } = result;

  if (!rows || rows.length === 0 || !columns || columns.length === 0) return null;

  // -------------------------------------------------------------
  // Scenario A: Single row result (e.g. Total Revenue in 2017, Average Delivery Days)
  // -------------------------------------------------------------
  if (rows.length === 1) {
    const singleRow = rows[0];
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {columns.map((col, idx) => (
          <div
            key={idx}
            className="p-4 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-1"
          >
            <div className="flex items-center justify-between text-content-secondary text-xs">
              <span className="font-medium capitalize">{col.replace(/_/g, ' ')}</span>
              <Activity className="w-4 h-4 text-accent" />
            </div>
            <div className="text-2xl font-bold tracking-tight text-content-primary">
              {formatMetricValue(singleRow[idx], col)}
            </div>
            <p className="text-[11px] text-content-muted">Aggregated business metric</p>
          </div>
        ))}

        {statistics && statistics.mean !== null && statistics.mean !== undefined && (
          <div className="p-4 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-1">
            <div className="flex items-center justify-between text-content-secondary text-xs">
              <span className="font-medium">Population Mean</span>
              <TrendingUp className="w-4 h-4 text-status-success" />
            </div>
            <div className="text-2xl font-bold tracking-tight text-content-primary">
              {formatMetricValue(statistics.mean, columns[0])}
            </div>
            <p className="text-[11px] text-content-muted">Descriptive distribution mean</p>
          </div>
        )}

        {statistics && statistics.median !== null && statistics.median !== undefined && (
          <div className="p-4 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-1">
            <div className="flex items-center justify-between text-content-secondary text-xs">
              <span className="font-medium">Population Median</span>
              <BarChart2 className="w-4 h-4 text-accent" />
            </div>
            <div className="text-2xl font-bold tracking-tight text-content-primary">
              {formatMetricValue(statistics.median, columns[0])}
            </div>
            <p className="text-[11px] text-content-muted">50th percentile distribution</p>
          </div>
        )}
      </div>
    );
  }

  // -------------------------------------------------------------
  // Determine Column Roles for Multi-Row Datasets
  // -------------------------------------------------------------
  // Find numeric column with highest frequency of valid numbers
  let metricColIdx = -1;
  let maxNumericCount = 0;
  columns.forEach((_, colIdx) => {
    const numCount = rows.filter(r => typeof r[colIdx] === 'number').length;
    if (numCount > maxNumericCount) {
      maxNumericCount = numCount;
      metricColIdx = colIdx;
    }
  });

  if (metricColIdx === -1) {
    // No numeric column available for analytical metrics
    return null;
  }

  // Find date / time column or label column
  const dateColIdx = columns.findIndex((col, idx) => {
    if (idx === metricColIdx) return false;
    const colLower = col.toLowerCase();
    const isNamedDate = colLower.includes('month') || colLower.includes('date') || colLower.includes('year') || colLower.includes('period');
    const hasIsoSample = rows.some(r => isIsoDateString(r[idx]));
    return isNamedDate || hasIsoSample;
  });

  const isTimeSeries = dateColIdx !== -1;
  const metricColName = columns[metricColIdx];

  // -------------------------------------------------------------
  // Scenario B: Time-Series Dataset (e.g. Monthly Revenue, Revenue Trends)
  // -------------------------------------------------------------
  if (isTimeSeries) {
    const validRows = rows.filter(r => typeof r[metricColIdx] === 'number');
    if (validRows.length === 0) return null;

    // Sort descending by metric value to identify actual top-performing months
    const sortedByMetric = [...validRows].sort(
      (a, b) => (b[metricColIdx] as number) - (a[metricColIdx] as number)
    );

    const topMonthRow = sortedByMetric[0];
    const secondMonthRow = sortedByMetric.length > 1 ? sortedByMetric[1] : null;

    // Total revenue across the returned period (ignoring nulls, sum actual numbers)
    const totalPeriodRevenue = validRows.reduce(
      (acc, r) => acc + (r[metricColIdx] as number),
      0
    );

    const topMonthLabel = formatDateLabel(topMonthRow[dateColIdx], 'shortMonthYear');
    const secondMonthLabel = secondMonthRow ? formatDateLabel(secondMonthRow[dateColIdx], 'shortMonthYear') : null;

    return (
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {/* KPI 1: Highest-revenue month */}
        <div className="p-4 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-1">
          <div className="flex items-center justify-between text-content-secondary text-xs">
            <span className="font-medium">Highest-Revenue Month</span>
            <Award className="w-4 h-4 text-accent" />
          </div>
          <div className="text-xl font-bold tracking-tight text-content-primary truncate">
            {topMonthLabel}
          </div>
          <div className="text-sm font-semibold text-accent">
            {formatMetricValue(topMonthRow[metricColIdx], metricColName)}
          </div>
        </div>

        {/* KPI 2: Second-highest-revenue month */}
        {secondMonthRow && (
          <div className="p-4 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-1">
            <div className="flex items-center justify-between text-content-secondary text-xs">
              <span className="font-medium">Second-Highest Month</span>
              <TrendingUp className="w-4 h-4 text-content-muted" />
            </div>
            <div className="text-xl font-bold tracking-tight text-content-primary truncate">
              {secondMonthLabel}
            </div>
            <div className="text-sm font-semibold text-content-secondary">
              {formatMetricValue(secondMonthRow[metricColIdx], metricColName)}
            </div>
          </div>
        )}

        {/* KPI 3: Total Revenue across returned period */}
        <div className="p-4 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-1">
          <div className="flex items-center justify-between text-content-secondary text-xs">
            <span className="font-medium">Total Revenue</span>
            <Calendar className="w-4 h-4 text-accent" />
          </div>
          <div className="text-xl font-bold tracking-tight text-content-primary">
            {formatMetricValue(totalPeriodRevenue, metricColName)}
          </div>
          <p className="text-[11px] text-content-muted">
            Across {rows.length} returned period{rows.length === 1 ? '' : 's'}
          </p>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------
  // Scenario C: Categorical Ranking Dataset (e.g. Categories, Products, Sellers)
  // -------------------------------------------------------------
  const isRanking = result.intent === 'ranking' || columns.some(c => c.toLowerCase().includes('revenue'));
  
  if (isRanking && rows.length > 1) {
    const labelColIndex = columns.findIndex((_, i) => i !== metricColIdx);
    if (labelColIndex === -1) return null;

    const topRow = rows[0];
    const runnerUpRow = rows[1];
    const sumTotal = rows.reduce(
      (acc, r) => acc + (typeof r[metricColIdx] === 'number' ? (r[metricColIdx] as number) : 0),
      0
    );

    const isRevenueMetric = metricColName.toLowerCase().includes('revenue');
    const combinedTotalLabel = isRevenueMetric
      ? `Top ${rows.length} Combined Revenue`
      : `Top ${rows.length} Total`;

    return (
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="p-4 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-1">
          <div className="flex items-center justify-between text-content-secondary text-xs">
            <span className="font-medium">#1 Ranked Leader</span>
            <Award className="w-4 h-4 text-accent" />
          </div>
          <div className="text-xl font-bold tracking-tight text-content-primary truncate" title={String(topRow[labelColIndex])}>
            {String(topRow[labelColIndex])}
          </div>
          <div className="text-sm font-semibold text-accent">
            {formatMetricValue(topRow[metricColIdx], metricColName)}
          </div>
        </div>

        <div className="p-4 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-1">
          <div className="flex items-center justify-between text-content-secondary text-xs">
            <span className="font-medium">#2 Runner-Up</span>
            <TrendingUp className="w-4 h-4 text-content-muted" />
          </div>
          <div className="text-xl font-bold tracking-tight text-content-primary truncate" title={String(runnerUpRow[labelColIndex])}>
            {String(runnerUpRow[labelColIndex])}
          </div>
          <div className="text-sm font-semibold text-content-secondary">
            {formatMetricValue(runnerUpRow[metricColIdx], metricColName)}
          </div>
        </div>

        <div className="p-4 bg-background-card border border-border-subtle rounded-xl shadow-panel space-y-1">
          <div className="flex items-center justify-between text-content-secondary text-xs">
            <span className="font-medium">{combinedTotalLabel}</span>
            <BarChart2 className="w-4 h-4 text-accent" />
          </div>
          <div className="text-xl font-bold tracking-tight text-content-primary">
            {formatMetricValue(sumTotal, metricColName)}
          </div>
          <p className="text-[11px] text-content-muted">Combined cohort sum</p>
        </div>
      </div>
    );
  }

  // For other datasets that do not cleanly match, return null to avoid misleading cards
  return null;
};
