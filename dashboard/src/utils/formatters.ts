// Shared utility functions for date and currency formatting across the dashboard

/**
 * Checks if a string or value matches an ISO date pattern (YYYY-MM-DD or YYYY-MM)
 */
export function isIsoDateString(val: any): boolean {
  if (typeof val !== 'string') return false;
  return /^\d{4}-\d{2}(-\d{2})?$/.test(val.trim());
}

/**
 * Formats a date string (e.g. "2018-09-01" or "2018-09") into a human-readable format.
 * Defaults to "MMM YYYY" (e.g. "Sep 2018") if day is 01 or not provided.
 */
export function formatDateLabel(val: any, format: 'shortMonthYear' | 'fullMonthYear' | 'fullDate' = 'shortMonthYear'): string {
  if (!val) return '—';
  const str = String(val).trim();
  
  // Parse year, month, day manually to prevent timezone offset shifts
  const match = str.match(/^(\d{4})-(\d{2})(?:-(\d{2}))?/);
  if (!match) return str;

  const year = parseInt(match[1], 10);
  const month = parseInt(match[2], 10) - 1; // 0-indexed
  const day = match[3] ? parseInt(match[3], 10) : undefined;

  const monthNamesShort = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const monthNamesFull = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  if (month < 0 || month > 11) return str;

  if (format === 'shortMonthYear') {
    return `${monthNamesShort[month]} ${year}`;
  }
  if (format === 'fullMonthYear') {
    return `${monthNamesFull[month]} ${year}`;
  }
  if (format === 'fullDate' && day !== undefined) {
    return `${monthNamesShort[month]} ${day}, ${year}`;
  }
  return `${monthNamesShort[month]} ${year}`;
}

/**
 * Formats a numeric currency value consistently with 2 decimal places.
 */
export function formatCurrency(val: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(val);
}

/**
 * Formats a numeric percentage with 2 decimal places.
 */
export function formatPercentage(val: number): string {
  return `${val.toFixed(2)}%`;
}

/**
 * Formats days/time values with 2 decimal places.
 */
export function formatDays(val: number): string {
  return `${val.toFixed(2)} days`;
}

/**
 * Formats general numbers with standard thousands separators and up to 2 decimal places.
 */
export function formatNumber(val: number): string {
  return new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 2,
  }).format(val);
}
