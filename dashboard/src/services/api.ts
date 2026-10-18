import { HealthResponse, QueryRequest, QueryResponse, HistoryResponse } from '../types/api';

const API_BASE = '/api';

export async function checkHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch(`${API_BASE}/health`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    if (!response.ok) {
      throw new Error(`Health check returned status ${response.status}`);
    }
    return await response.json();
  } catch (err: any) {
    return {
      status: 'degraded',
      database: 'disconnected',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
    };
  }
}

export async function submitQuery(question: string): Promise<QueryResponse> {
  const payload: QueryRequest = { question };
  
  let response: Response;
  try {
    response = await fetch(`${API_BASE}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
    });
  } catch (networkErr: any) {
    throw new Error('Unable to connect to the analytics backend service. Please check that Uvicorn is running on 127.0.0.1:8000.');
  }

  const data = await response.json();

  if (!response.ok) {
    // Check detail message from FastAPI
    const errorDetail = data?.detail || 'An unexpected error occurred while executing the analytical query.';
    if (typeof errorDetail === 'string') {
      throw new Error(errorDetail);
    } else if (Array.isArray(errorDetail)) {
      // Pydantic validation errors
      const msg = errorDetail.map((item: any) => item.msg || JSON.stringify(item)).join('; ');
      throw new Error(msg);
    }
    throw new Error(JSON.stringify(errorDetail));
  }

  return data as QueryResponse;
}

export async function getQueryHistory(): Promise<HistoryResponse> {
  try {
    const response = await fetch(`${API_BASE}/history`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    if (!response.ok) {
      throw new Error(`History returned status ${response.status}`);
    }
    return await response.json();
  } catch (err: any) {
    return { total: 0, entries: [] };
  }
}
