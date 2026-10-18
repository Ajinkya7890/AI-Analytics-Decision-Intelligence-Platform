export interface HealthResponse {
  status: 'healthy' | 'degraded' | string;
  database: 'connected' | 'disconnected' | string;
  version: string;
  timestamp: string;
}

export interface QueryRequest {
  question: string;
}

export interface QueryResponse {
  question: string;
  success: boolean;
  sql: string;
  columns: string[];
  rows: (string | number | boolean | null)[][];
  row_count: number;
  statistics?: Record<string, number | null> | null;
  execution_time_ms: number;
  intent?: string | null;
  target_entity?: string | null;
  metrics?: string[] | null;
  dimensions?: string[] | null;
  validation?: string | null;
}

export interface HistoryEntry {
  id: string;
  question: string;
  timestamp: string;
  success: boolean;
  row_count?: number | null;
  execution_time_ms?: number | null;
  error_message?: string | null;
}

export interface HistoryResponse {
  total: number;
  entries: HistoryEntry[];
}
