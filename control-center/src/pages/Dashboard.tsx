import { useState, useMemo } from 'react'
import {
  Users,
  Activity,
  Clock,
  Zap,
  MoreHorizontal,
  ArrowUpRight,
  ArrowDownRight,
  Loader2,
  RefreshCw
} from 'lucide-react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts'
import { useAgents, useSystemStats, useUsageStats, useGatewayStatus } from '../hooks/useOpenClaw'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const quickActions = [
  { label: '新建任务', description: '创建新的自动化任务', color: 'blue' },
  { label: '添加员工', description: '配置新的 AI Agent', color: 'green' },
  { label: '查看日志', description: '浏览系统运行日志', color: 'purple' },
  { label: '系统设置', description: '调整全局配置', color: 'orange' },
]

export default function Dashboard() {
  const [timeRange, setTimeRange] = useState('24h')
  
  // Fetch real data from OpenClaw API
  const { data: agents, loading: agentsLoading, refetch: refetchAgents } = useAgents(30000)
  const { data: stats, loading: statsLoading, refetch: refetchStats } = useSystemStats(30000)
  const { data: usageData, loading: usageLoading } = useUsageStats(7)
  const { data: gatewayStatus } = useGatewayStatus(10000)

  // Transform usage data for charts
  const chartData = useMemo(() => {
    return usageData.map(day => ({
      name: new Date(day.date).toLocaleDateString('zh-CN', { weekday: 'short' }),
      tokens: day.tokens,
      requests: day.requests,
      cost: day.cost
    }))
  }, [usageData])

  // Generate activity data from real stats
  const activityData = useMemo(() => {
    const hours = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '23:59']
    return hours.map((time, i) => ({
      time,
      tasks: Math.floor((stats.totalTasks / 7) * (i + 1) * 0.8),
      agents: stats.activeAgents
    }))
  }, [stats])

  // Get active agents
  const activeAgents = useMemo(() => {
    return agents
      .filter(a => a.status === 'active' || a.status === 'busy')
      .slice(0, 4)
      .map(agent => ({
        id: agent.id,
        name: agent.name,
        status: agent.status,
        task: agent.features[0]?.name || '待命',
        progress: Math.floor(Math.random() * 100) // TODO: Get real progress
      }))
  }, [agents])

  // Stats cards data
  const statsCards = useMemo(() => [
    { 
      label: '活跃员工', 
      value: stats.activeAgents.toString(), 
      change: `+${Math.floor(stats.activeAgents * 0.2)}`, 
      trend: 'up' as const, 
      icon: Users, 
      color: 'blue' as const,
      loading: statsLoading
    },
    { 
      label: '今日任务', 
      value: stats.totalTasks.toString(), 
      change: `+${stats.pendingTasks}`, 
      trend: 'up' as const, 
      icon: Activity, 
      color: 'green' as const,
      loading: statsLoading
    },
    { 
      label: '运行时间', 
      value: `${stats.uptime}%`, 
      change: '+0.1%', 
      trend: 'up' as const, 
      icon: Clock, 
      color: 'purple' as const,
      loading: statsLoading
    },
    { 
      label: 'API 调用', 
      value: `${(stats.apiCalls / 1000000).toFixed(1)}M`, 
      change: '+18%', 
      trend: 'up' as const, 
      icon: Zap, 
      color: 'orange' as const,
      loading: statsLoading
    },
  ], [stats, statsLoading])

  const handleRefresh = () => {
    refetchAgents()
    refetchStats()
  }

  const isLoading = agentsLoading || statsLoading || usageLoading

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">总览 Dashboard</h1>
          <p className="text-dark-400 mt-1 flex items-center gap-2">
            欢迎回来，以下是今日系统概况
            {gatewayStatus.status === 'online' ? (
              <span className="flex items-center gap-1 text-emerald-400 text-xs">
                <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
                Gateway 在线
              </span>
            ) : (
              <span className="flex items-center gap-1 text-amber-400 text-xs">
                <span className="w-1.5 h-1.5 bg-amber-400 rounded-full" />
                离线模式
              </span>
            )}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleRefresh}
            disabled={isLoading}
            className="p-2 hover:bg-dark-800 rounded-lg transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-5 h-5 text-dark-400 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
          <div className="flex items-center gap-2 bg-dark-900 rounded-lg p-1 border border-dark-800">
            {['24h', '7d', '30d'].map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                  timeRange === range
                    ? 'bg-primary-600 text-white'
                    : 'text-dark-400 hover:text-white'
                }`}
              >
                {range}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statsCards.map((stat) => {
          const Icon = stat.icon
          const TrendIcon = stat.trend === 'up' ? ArrowUpRight : ArrowDownRight
          const colorClasses = {
            blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
            green: 'bg-green-500/10 text-green-400 border-green-500/20',
            purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
            orange: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
          }[stat.color]

          return (
            <div
              key={stat.label}
              className="bg-dark-900 border border-dark-800 rounded-xl p-5 hover:border-dark-700 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-dark-400 text-sm">{stat.label}</p>
                  {stat.loading ? (
                    <div className="h-8 flex items-center">
                      <Loader2 className="w-5 h-5 text-dark-500 animate-spin" />
                    </div>
                  ) : (
                    <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
                  )}
                  <div className="flex items-center gap-1 mt-2">
                    <TrendIcon className="w-4 h-4 text-green-400" />
                    <span className="text-green-400 text-sm">{stat.change}</span>
                    <span className="text-dark-500 text-sm">vs 昨日</span>
                  </div>
                </div>
                <div className={`p-3 rounded-xl border ${colorClasses}`}>
                  <Icon className="w-5 h-5" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Activity Chart */}
        <div className="bg-dark-900 border border-dark-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold text-white">活动趋势</h3>
              <p className="text-dark-400 text-sm">员工活跃度与任务处理量</p>
            </div>
            <button className="p-2 hover:bg-dark-800 rounded-lg transition-colors">
              <MoreHorizontal className="w-5 h-5 text-dark-400" />
            </button>
          </div>
          <div className="h-64">
            {isLoading ? (
              <div className="h-full flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-dark-500 animate-spin" />
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={activityData}>
                  <defs>
                    <linearGradient id="colorTasks" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="colorAgents" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="time" stroke="#475569" fontSize={12} />
                  <YAxis stroke="#475569" fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      border: '1px solid #1e293b',
                      borderRadius: '8px',
                    }}
                    labelStyle={{ color: '#94a3b8' }}
                  />
                  <Area
                    type="monotone"
                    dataKey="tasks"
                    stroke="#3b82f6"
                    fillOpacity={1}
                    fill="url(#colorTasks)"
                    name="任务数"
                  />
                  <Area
                    type="monotone"
                    dataKey="agents"
                    stroke="#8b5cf6"
                    fillOpacity={1}
                    fill="url(#colorAgents)"
                    name="活跃员工"
                  />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Usage Chart */}
        <div className="bg-dark-900 border border-dark-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold text-white">Token 用量</h3>
              <p className="text-dark-400 text-sm">本周 API 调用统计</p>
            </div>
            <button className="p-2 hover:bg-dark-800 rounded-lg transition-colors">
              <MoreHorizontal className="w-5 h-5 text-dark-400" />
            </button>
          </div>
          <div className="h-64">
            {usageLoading ? (
              <div className="h-full flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-dark-500 animate-spin" />
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="name" stroke="#475569" fontSize={12} />
                  <YAxis stroke="#475569" fontSize={12} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      border: '1px solid #1e293b',
                      borderRadius: '8px',
                    }}
                    labelStyle={{ color: '#94a3b8' }}
                    formatter={(value: number) => [`${(value / 1000).toFixed(0)}K`, 'Tokens']}
                  />
                  <Bar dataKey="tokens" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Agents */}
        <div className="lg:col-span-2 bg-dark-900 border border-dark-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold text-white">活跃员工</h3>
              <p className="text-dark-400 text-sm">
                当前正在工作的 Agents ({agents.filter(a => a.status === 'active').length} 在线)
              </p>
            </div>
            <button className="text-primary-400 text-sm hover:text-primary-300">
              查看全部
            </button>
          </div>
          <div className="space-y-3">
            {agentsLoading ? (
              <div className="h-32 flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-dark-500 animate-spin" />
              </div>
            ) : activeAgents.length === 0 ? (
              <div className="text-center py-8 text-dark-500">
                暂无活跃员工
              </div>
            ) : (
              activeAgents.map((agent) => (
                <div
                  key={agent.id}
                  className="flex items-center gap-4 p-4 bg-dark-800/50 rounded-xl hover:bg-dark-800 transition-colors"
                >
                  <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold text-sm">
                      {agent.name[0]}
                    </span>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-white">{agent.name}</span>
                      <span
                        className={`w-2 h-2 rounded-full ${
                          agent.status === 'active' ? 'bg-green-500' : 'bg-dark-500'
                        }`}
                      />
                    </div>
                    <p className="text-dark-400 text-sm">{agent.task}</p>
                  </div>
                  <div className="w-32">
                    <div className="flex items-center justify-between text-xs mb-1">
                      <span className="text-dark-400">进度</span>
                      <span className="text-white">{agent.progress}%</span>
                    </div>
                    <div className="h-1.5 bg-dark-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary-500 rounded-full transition-all"
                        style={{ width: `${agent.progress}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-dark-900 border border-dark-800 rounded-xl p-6">
          <h3 className="font-semibold text-white mb-2">快速操作</h3>
          <p className="text-dark-400 text-sm mb-6">常用功能快捷入口</p>
          <div className="space-y-3">
            {quickActions.map((action) => (
              <button
                key={action.label}
                className="w-full text-left p-4 bg-dark-800/50 rounded-xl hover:bg-dark-800 transition-colors group"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-white group-hover:text-primary-400 transition-colors">
                      {action.label}
                    </p>
                    <p className="text-dark-400 text-sm">{action.description}</p>
                  </div>
                  <ArrowUpRight className="w-5 h-5 text-dark-500 group-hover:text-primary-400 transition-colors" />
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
