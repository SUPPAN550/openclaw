import axios, { AxiosInstance } from 'axios';
import type { 
  Agent, 
  Session, 
  Task, 
  MemoryEntry, 
  Document, 
  UsageStats, 
  SystemStats,
  GatewayStatus 
} from '../types';

// OpenClaw Gateway API client
class OpenClawAPI {
  private client: AxiosInstance;
  private baseURL: string;
  private isOnline: boolean = false;
  private useMockData: boolean = true;

  constructor() {
    // Default to local gateway, can be configured
    const envUrl = import.meta.env.VITE_OPENCLAW_API_URL;
    this.baseURL = envUrl && envUrl.trim() !== '' ? envUrl : '';
    
    // Check if we should use real API or mock data
    const mockDataFlag = import.meta.env.VITE_USE_MOCK_DATA;
    this.useMockData = mockDataFlag === 'true' || mockDataFlag === true || !this.baseURL;
    
    // Create axios client
    this.client = axios.create({
      baseURL: this.baseURL || 'http://localhost:8080/api',
      timeout: 2000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token if available
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('openclaw_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // Gateway Status
  async getGatewayStatus(): Promise<GatewayStatus> {
    // Always use mock data for now
    return {
      status: 'offline',
      version: '2026.3.13',
      uptime: '0',
      connectedNodes: 0
    };
  }

  // Agents
  async getAgents(): Promise<Agent[]> {
    // Load from navigation.json (local file)
    try {
      const response = await fetch('/navigation.json');
      const data = await response.json();
      return data.agents.map((agent: any) => ({
        ...agent,
        status: Math.random() > 0.3 ? 'active' : 'idle',
        lastActive: new Date().toISOString(),
        taskCount: Math.floor(Math.random() * 20)
      }));
    } catch {
      return this.getFallbackAgents();
    }
  }

  private getFallbackAgents(): Agent[] {
    return [
      {
        id: 'may',
        name: 'May',
        title: '核心主控',
        description: '系统核心控制中枢',
        icon: '🎯',
        color: '#4A90D9',
        status: 'active',
        features: [
          { name: '系统状态', action: 'check_system_health', icon: '📊' },
          { name: '每日报告', action: 'generate_daily_report', icon: '📋' },
          { name: '智能体协调', action: 'coordinate_agents', icon: '🎛️' }
        ]
      },
      {
        id: 'gock',
        name: 'Gock',
        title: '每日新闻',
        description: '新闻聚合与摘要',
        icon: '📰',
        color: '#E74C3C',
        status: 'active',
        features: [
          { name: '早间简报', action: 'morning_briefing', icon: '🌅' },
          { name: '晚间汇总', action: 'evening_summary', icon: '🌙' },
          { name: '热点追踪', action: 'trending_topics', icon: '🔥' }
        ]
      }
    ];
  }

  // Sessions
  async getSessions(): Promise<Session[]> {
    return [
      {
        sessionKey: 'main',
        status: 'active',
        lastActive: new Date().toISOString(),
        messageCount: 156
      }
    ];
  }

  // Tasks
  async getTasks(): Promise<Task[]> {
    const now = new Date();
    return [
      {
        id: '1',
        title: '完成控制面板 UI 设计',
        description: '设计 OpenClaw 控制面板的用户界面',
        status: 'in_progress',
        priority: 'high',
        assignee: 'Jarvis',
        progress: 78,
        createdAt: now.toISOString(),
        updatedAt: now.toISOString(),
        tags: ['UI设计', '前端']
      },
      {
        id: '2',
        title: 'API 接口性能优化',
        description: '优化用户查询接口的响应时间',
        status: 'pending',
        priority: 'high',
        assignee: 'TARS',
        progress: 0,
        createdAt: new Date(now.getTime() - 86400000).toISOString(),
        updatedAt: new Date(now.getTime() - 86400000).toISOString(),
        tags: ['后端', '性能优化']
      },
      {
        id: '3',
        title: '数据分析报告生成',
        description: '生成 Q1 用户行为分析报告',
        status: 'completed',
        priority: 'medium',
        assignee: 'Friday',
        progress: 100,
        createdAt: new Date(now.getTime() - 172800000).toISOString(),
        updatedAt: new Date(now.getTime() - 86400000).toISOString(),
        tags: ['数据分析', '报告']
      }
    ];
  }

  // Memory
  async getMemoryEntries(): Promise<MemoryEntry[]> {
    return [
      {
        id: '1',
        content: 'Sir 偏好深色主题界面，专业简洁风格',
        category: 'preferences',
        tags: ['UI', '主题', '偏好'],
        createdAt: new Date().toISOString(),
        source: 'conversation'
      },
      {
        id: '2',
        content: 'Control Center 项目创建于 2026-03-17',
        category: 'events',
        tags: ['项目', '里程碑'],
        createdAt: new Date().toISOString(),
        source: 'system'
      }
    ];
  }

  // Documents
  async getDocuments(): Promise<Document[]> {
    return [
      {
        id: '1',
        title: 'OpenClaw 配置指南',
        type: 'doc',
        status: 'active',
        lastModified: new Date().toISOString(),
        modifiedBy: 'Jarvis',
        size: 25600
      },
      {
        id: '2',
        title: 'API 接口文档',
        type: 'doc',
        status: 'active',
        lastModified: new Date(Date.now() - 86400000).toISOString(),
        modifiedBy: 'TARS',
        size: 51200
      }
    ];
  }

  // Usage Stats
  async getUsageStats(days: number = 7): Promise<UsageStats[]> {
    const stats: UsageStats[] = [];
    const now = new Date();
    
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);
      
      stats.push({
        date: date.toISOString().split('T')[0],
        tokens: Math.floor(Math.random() * 50000) + 50000,
        requests: Math.floor(Math.random() * 500) + 100,
        cost: Math.random() * 5 + 1
      });
    }
    
    return stats;
  }

  // System Stats
  async getSystemStats(): Promise<SystemStats> {
    const agents = await this.getAgents();
    const tasks = await this.getTasks();
    
    return {
      activeAgents: agents.filter(a => a.status === 'active').length,
      totalTasks: tasks.length,
      completedTasks: tasks.filter(t => t.status === 'completed').length,
      pendingTasks: tasks.filter(t => t.status === 'pending').length,
      uptime: 99.9,
      totalTokens: 2450000,
      apiCalls: 15600
    };
  }

  // Execute action
  async executeAction(action: string, params?: any): Promise<any> {
    console.log('Action executed:', action, params);
    return { success: true };
  }
}

// Export singleton instance
export const openclawAPI = new OpenClawAPI();

// Export class for custom instances
export { OpenClawAPI };
