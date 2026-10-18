import React, { useState, useMemo } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown, Search } from 'lucide-react';
import { QueryResponse } from '../types/api';
import { formatDateLabel, formatCurrency, formatPercentage, formatDays, formatNumber, isIsoDateString } from '../utils/formatters';

interface DataTableProps {
  result: QueryResponse;
}

function formatCellValue(val: any, colName: string): { formatted: string; isNumber: boolean; rawVal: any } {
  if (val === null || val === undefined) {
    return { formatted: '—', isNumber: false, rawVal: val };
  }
  if (typeof val === 'number') {
    const colLower = colName.toLowerCase();
    if (colLower.includes('rate') || colLower.includes('percentage') || colLower.includes('percent')) {
      return { formatted: formatPercentage(val), isNumber: true, rawVal: val };
    }
    if (colLower.includes('revenue') || colLower.includes('sales') || colLower.includes('price') || colLower.includes('spend') || colLower.includes('value')) {
      return {
        formatted: formatCurrency(val),
        isNumber: true,
        rawVal: val,
      };
    }
    if (colLower.includes('days') || colLower.includes('time')) {
      return { formatted: formatDays(val), isNumber: true, rawVal: val };
    }
    return {
      formatted: formatNumber(val),
      isNumber: true,
      rawVal: val,
    };
  }
  if (isIsoDateString(val)) {
    return { formatted: formatDateLabel(val, 'shortMonthYear'), isNumber: false, rawVal: val };
  }
  return { formatted: String(val), isNumber: false, rawVal: val };
}

export const DataTable: React.FC<DataTableProps> = ({ result }) => {
  const { columns, rows } = result;
  const [sortCol, setSortCol] = useState<number | null>(null);
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc');
  const [filterText, setFilterText] = useState('');

  const handleSort = (colIdx: number) => {
    if (sortCol === colIdx) {
      if (sortDir === 'asc') setSortDir('desc');
      else {
        // Return to natural default order as returned by backend
        setSortCol(null);
        setSortDir('asc');
      }
    } else {
      setSortCol(colIdx);
      setSortDir('asc');
    }
  };

  // Preserve natural row order unless explicitly sorted
  const filteredAndSortedRows = useMemo(() => {
    let output = [...rows];

    // Filter
    if (filterText.trim()) {
      const q = filterText.toLowerCase();
      output = output.filter(row =>
        row.some(cell => String(cell ?? '').toLowerCase().includes(q))
      );
    }

    // Sort
    if (sortCol !== null) {
      output.sort((a, b) => {
        const valA = a[sortCol];
        const valB = b[sortCol];
        if (valA === valB) return 0;
        if (valA === null || valA === undefined) return 1;
        if (valB === null || valB === undefined) return -1;

        if (typeof valA === 'number' && typeof valB === 'number') {
          return sortDir === 'asc' ? valA - valB : valB - valA;
        }
        return sortDir === 'asc'
          ? String(valA).localeCompare(String(valB))
          : String(valB).localeCompare(String(valA));
      });
    }

    return output;
  }, [rows, filterText, sortCol, sortDir]);

  if (!columns || columns.length === 0) {
    return (
      <div className="p-8 text-center text-content-muted text-xs">
        No columns returned for this query.
      </div>
    );
  }

  return (
    <div className="bg-background-card border border-border-subtle rounded-xl shadow-panel overflow-hidden">
      {/* Table Toolbar */}
      <div className="p-3 border-b border-border-subtle flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 bg-background-card/60">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-semibold text-content-primary tracking-tight">
            Raw Results Table
          </span>
          <span className="text-[11px] px-2 py-0.5 rounded-full bg-background-surface border border-border-subtle text-content-secondary font-mono">
            {filteredAndSortedRows.length} of {rows.length} rows
          </span>
        </div>

        {rows.length > 3 && (
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-content-muted absolute left-2.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={filterText}
              onChange={(e) => setFilterText(e.target.value)}
              placeholder="Filter results..."
              className="bg-background-surface border border-border-subtle rounded-lg text-xs text-content-primary pl-8 pr-3 py-1.5 focus:outline-none focus:border-accent w-full sm:w-48 placeholder-content-muted"
            />
          </div>
        )}
      </div>

      {/* Table Content */}
      <div className="overflow-x-auto max-h-[460px] overflow-y-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead className="bg-background-surface sticky top-0 z-10 border-b border-border-subtle">
            <tr>
              <th className="py-2.5 px-3 text-[11px] font-semibold text-content-muted uppercase tracking-wider w-12 text-center">
                #
              </th>
              {columns.map((col, idx) => (
                <th
                  key={idx}
                  onClick={() => handleSort(idx)}
                  className="py-2.5 px-3 text-[11px] font-semibold text-content-secondary uppercase tracking-wider cursor-pointer hover:text-content-primary transition-colors select-none"
                >
                  <div className="flex items-center space-x-1.5">
                    <span className="capitalize">{col.replace(/_/g, ' ')}</span>
                    <span className="text-content-muted">
                      {sortCol === idx ? (
                        sortDir === 'asc' ? (
                          <ArrowUp className="w-3 h-3 text-accent" />
                        ) : (
                          <ArrowDown className="w-3 h-3 text-accent" />
                        )
                      ) : (
                        <ArrowUpDown className="w-3 h-3 opacity-30 hover:opacity-100" />
                      )}
                    </span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle/40 font-mono text-[12px]">
            {filteredAndSortedRows.length === 0 ? (
              <tr>
                <td colSpan={columns.length + 1} className="py-8 text-center text-content-muted text-xs">
                  No matching rows found.
                </td>
              </tr>
            ) : (
              filteredAndSortedRows.map((row, rIdx) => (
                <tr
                  key={rIdx}
                  className="hover:bg-background-hover/70 transition-colors group"
                >
                  <td className="py-2.5 px-3 text-content-muted text-center text-[10px] select-none font-sans">
                    {rIdx + 1}
                  </td>
                  {columns.map((col, cIdx) => {
                    const { formatted, isNumber, rawVal } = formatCellValue(row[cIdx], col);
                    return (
                      <td
                        key={cIdx}
                        className={`py-2.5 px-3 text-content-primary font-sans text-xs ${
                          isNumber ? 'font-mono text-content-primary font-medium' : ''
                        }`}
                      >
                        <div className="truncate max-w-xs" title={String(rawVal ?? '')}>
                          {formatted}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
