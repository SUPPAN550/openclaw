import { useState } from 'react'
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Zap,
  Clock,
  Calendar,
  Download,
  Filter,
  MoreHorizontal,
  AlertCircle,
  CheckCircle,
  Info
} from 'lucide-react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar
} from 'recharts'

const usageStats = [
  { label: '本月消耗', value: '$284.50', change: '+12.5%', trend: 'up', icon: DollarSign },
  { label: 'Token 用量', value: '12.4M', change: '+8.2%', trend: 'up', icon: Zap },
  { label: 'API 调用', value: '45.2K', change: '-3.1%', trend: 'down', icon: BarChart3 },
  { label: '平均响应', value: '245ms', change: '-15ms', trend: 'up', icon: Clock },
]

const dailyUsageData = [
  { date: '03/11', tokens: 320000, cost: 8.5 },
  { date: '03/12', tokens: 380000, cost: 10.2 },
  { date: '03/13', tokens: 420000, cost: 11.8 },
  { date: '03/14', tokens: 350000, cost: 9.3 },
  { date: '03/15', tokens: 480000, cost: 13.5 },
  { date: '03/16', tokens: 520000, cost: 14.8 },
  { date: '03/17', tokens: 410000, cost: 11.2 },
]

const modelDistribution = [
  { name: 'GPT-4', value: 45, color: '#3b82f6' },
  { name: 'GPT-3.5', value: 30, color: '#8b5cf6' },
  { name: 'Claude-3', value: 20, color: '#10b981' },
  { name: '其他', value: 5, color: '#f59e0b' },
]

const agentUsage = [
  { name: 'Jarvis', tokens: 4500000, tasks: 1247 },
  { name: 'Friday', tokens: 3200000, tasks: 856 },
  { name: 'TARS', tokens: 2800000, tasks: 3422 },
  { name: 'Alfred', tokens: 1900000, tasks: 2341 },
]

const alerts = [
  { id: 1, type: 'warning', message: 'Jarvis 的 Token 消耗超过日限额 80%', time: '10分钟前' },
  { id: 2, type: 'info', message: '月度账单已生成，请查看', time: '2小时前' },
  { id: 3, type: 'success', message: 'API 响应时间优化完成', time: '5小时前' },
]

export default function Usage() {
  const [timeRange, setTimeRange] = useState('7d')

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">用量 Usage</h1>
          <p className="text-dark-400 mt-1">监控和分析系统资源使用情况</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 bg-dark-900 rounded-lg p-1 border border-dark-800">
            {['24h', '7d', '30d', '90d'].map((range) => (
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
          <button className="flex items-center gap-2 bg-dark-800 hover:bg-dark-700 text-dark-200 px-4 py-2 rounded-lg transition-colors">
            <Download className="w-4 h-4" />
            <span>导出报告</span>
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {usageStats.map((stat) => {
          const Icon = stat.icon
          const TrendIcon = stat.trend === 'up' ? TrendingUp : TrendingDown
          return (
            <div
              key={stat.label}
              className="bg-dark-900 border border-dark-800 rounded-xl p-5"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-dark-400 text-sm">{stat.label}</p>
                  <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
                  <div className="flex items-center gap-1 mt-2">
                    <TrendIcon className={`w-4 h-4 ${stat.trend === 'up' ? 'text-green-400' : 'text-red-400'}`} />
                    <span className={stat.trend === 'up' ? 'text-green-400' : 'text-red-400'}>
                      {stat.change}
                    </span>
                    <span className="text-dark-500 text-sm">vs 上期</span>
                  </div>
                </div>
                <div className="p-3 bg-dark-800 rounded-xl">
                  <Icon className="w-5 h-5 text-primary-400" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Usage Trend */}
        <div className="lg:col-span-2 bg-dark-900 border border-dark-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold text-white">使用趋势</h3>
              <p className="text-dark-400 text-sm">Token 消耗与成本分析</p>
            </div>
            <button className="p-2 hover:bg-dark-800 rounded-lg transition-colors">
              <MoreHorizontal className="w-5 h-5 text-dark-400" />
            </button>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={dailyUsageData}>
                <defs>
                  <linearGradient id="colorTokens" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#475569" fontSize={12} />
                <YAxis yAxisId="left" stroke="#475569" fontSize={12} />
                <YAxis yAxisId="right" orientation="right" stroke="#475569" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    border: '1px solid #1e293b',
                    borderRadius: '8px',
                  }}
                  labelStyle={{ color: '#94a3b8' }}
                />
                <Area
                  yAxisId="left"
                  type="monotone"
                  dataKey="tokens"
                  stroke="#3b82f6"
                  fillOpacity={1}
                  fill="url(#colorTokens)"
                  name="Tokens"
                />
                <Area
                  yAxisId="right"
                  type="monotone"
                  dataKey="cost"
                  stroke="#10b981"
                  fillOpacity={0}
                  strokeDasharray="5 5"
                  name="Cost ($)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Model Distribution */}
        <div className="bg-dark-900 border border-dark-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold text-white">模型分布</h3>
              <p className="text-dark-400 text-sm">Token 消耗占比</p>
            </div>
          </div>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={modelDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {modelDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    border: '1px solid #1e293b',
                    borderRadius: '8px',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-2 mt-4">
            {modelDistribution.map((model) => (
              <div key={model.name} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: model.color }}
                  />
                  <span className="text-dark-300 text-sm">{model.name}</span>
                </div>
                <span className="text-white text-sm">{model.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agent Usage */}
        <div className="bg-dark-900 border border-dark-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold text-white">员工用量排行</h3>
              <p className="text-dark-400 text-sm">各 Agent 的 Token 消耗情况</p>
            </div>
          </div>
          <div className="space-y-4">
            {agentUsage.map((agent, index) => (
              <div key={agent.name} className="flex items-center gap-4">
                <span className="text-dark-500 text-sm w-6">{index + 1}</span>
                <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-full flex items-center justify-center">
                  <span className="text-white font-semibold text-sm">{agent.name[0]}</span>
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-white text-sm">{agent.name}</span>
                    <span className="text-dark-400 text-sm">
                      {(agent.tokens / 1000000).toFixed(1)}M tokens
                    </span>
                  </div>
                  <div className="h-2 bg-dark-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary-500 rounded-full"
                      style={{ width: `${(agent.tokens / 4500000) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Alerts */}
        <div className="bg-dark-900 border border-dark-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold text-white">用量提醒</h3>
              <p className="text-dark-400 text-sm">系统监控和通知</p>
            </div>
            <button className="text-primary-400 text-sm hover:text-primary-300">
              查看全部
            </button>
          </div>
          <div className="space-y-3">
            {alerts.map((alert) => {
              const AlertIcon = alert.type === 'warning' ? AlertCircle : alert.type === 'success' ? CheckCircle : Info
              const alertColors = {
                warning: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
                success: 'bg-green-500/10 text-green-400 border-green-500/20',
                info: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
              }
              return (
                <div
                  key={alert.id}
                  className={`flex items-start gap-3 p-4 rounded-xl border ${alertColors[alert.type as keyof typeof alertColors]}`}
                >
                  <AlertIcon className="w-5 h-5 flex-shrink-0 mt-0.5" />
                  <div className="flex-1">
                    <p className="text-sm">{alert.message}</p>
                    <p className="text-xs opacity-60 mt-1">{alert.time}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}