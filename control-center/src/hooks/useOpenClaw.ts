import { useState, useEffect, useCallback } from 'react';
import { openclawAPI } from '../api/openclaw';
import type { Agent, Session, Task, MemoryEntry, Document, UsageStats, SystemStats, GatewayStatus } from '../types';

// Generic hook for API data fetching
export function useOpenClawData<T>(
  fetcher: () => Promise<T>,
  initialData: T,
  refreshInterval?: number
) {
  const [data, setData] = useState<T>(initialData);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetch = useCallback(async () => {
    try {
      setLoading(true);
      const result = await fetcher();
      setData(result);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [fetcher]);

  useEffect(() => {
    fetch();
    
    if (refreshInterval) {
      const interval = setInterval(fetch, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetch, refreshInterval]);

  return { data, loading, error, refetch: fetch };
}

// Specific hooks
export function useAgents(refreshInterval?: number) {
  return useOpenClawData<Agent[]>(
    () => openclawAPI.getAgents(),
    [],
    refreshInterval
  );
}

export function useSessions(refreshInterval?: number) {
  return useOpenClawData<Session[]>(
    () => openclawAPI.getSessions(),
    [],
    refreshInterval
  );
}

export function useTasks(refreshInterval?: number) {
  return useOpenClawData<Task[]>(
    () => openclawAPI.getTasks(),
    [],
    refreshInterval
  );
}

export function useMemory(refreshInterval?: number) {
  return useOpenClawData<MemoryEntry[]>(
    () => openclawAPI.getMemoryEntries(),
    [],
    refreshInterval
  );
}

export function useDocuments(refreshInterval?: number) {
  return useOpenClawData<Document[]>(
    () => openclawAPI.getDocuments(),
    [],
    refreshInterval
  );
}

export function useUsageStats(days: number = 7) {
  return useOpenClawData<UsageStats[]>(
    () => openclawAPI.getUsageStats(days),
    [],
    30000 // Refresh every 30 seconds
  );
}

export function useSystemStats(refreshInterval?: number) {
  return useOpenClawData<SystemStats>(
    () => openclawAPI.getSystemStats(),
    {
      activeAgents: 0,
      totalTasks: 0,
      completedTasks: 0,
      pendingTasks: 0,
      uptime: 100,
      totalTokens: 0,
      apiCalls: 0
    },
    refreshInterval
  );
}

export function useGatewayStatus(refreshInterval: number = 10000) {
  return useOpenClawData<GatewayStatus>(
    () => openclawAPI.getGatewayStatus(),
    {
      status: 'offline',
      version: 'Unknown',
      uptime: '0',
      connectedNodes: 0
    },
    refreshInterval
  );
}
