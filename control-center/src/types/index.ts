// OpenClaw API Types

export interface Agent {
  id: string;
  name: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  status: 'active' | 'idle' | 'busy' | 'offline';
  features: Feature[];
  lastActive?: string;
  taskCount?: number;
}

export interface Feature {
  name: string;
  action: string;
  icon: string;
}

export interface Session {
  sessionKey: string;
  agentId?: string;
  status: 'active' | 'idle' | 'completed';
  lastMessage?: string;
  lastActive: string;
  messageCount?: number;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high';
  assignee?: string;
  dueDate?: string;
  progress: number;
  createdAt: string;
  updatedAt: string;
  tags?: string[];
}

export interface MemoryEntry {
  id: string;
  content: string;
  category: string;
  tags: string[];
  createdAt: string;
  updatedAt?: string;
  source?: string;
}

export interface Document {
  id: string;
  title: string;
  type: 'doc' | 'sheet' | 'bitable' | 'file';
  status: 'active' | 'archived' | 'draft';
  lastModified: string;
  modifiedBy?: string;
  size?: number;
}

export interface UsageStats {
  date: string;
  tokens: number;
  requests: number;
  cost: number;
}

export interface SystemStats {
  activeAgents: number;
  totalTasks: number;
  completedTasks: number;
  pendingTasks: number;
  uptime: number;
  totalTokens: number;
  apiCalls: number;
}

export interface GatewayStatus {
  status: 'online' | 'offline' | 'degraded';
  version: string;
  uptime: string;
  connectedNodes: number;
}
