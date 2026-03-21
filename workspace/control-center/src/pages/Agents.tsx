import { useState, useMemo } from 'react'
import {
  Users,
  Plus,
  Search,
  Filter,
  MoreHorizontal,
  Play,
  Pause,
  Settings,
  Trash2,
  Edit,
  Copy,
  Bot,
  MessageSquare,
  FileText,
  Code,
  Sparkles,
  Loader2,
  RefreshCw,
  AlertCircle
} from 'lucide-react'
import { useAgents } from '../hooks/useOpenClaw'
import { openclawAPI } from '../api/openclaw'
import type { Agent } from '../types'

const getAgentIcon = (type: string) => {
  switch (type) {
    case 'code': return Code
    case 'document': return FileText
    case 'analyst': return Sparkles
    default: return Bot
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'active': return 'bg-green-500'
    case 'busy': return 'bg-amber-500'
    case 'idle': return 'bg-slate-500'
    case 'offline': return 'bg-red-500'
    default: return 'bg-slate-500'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'active': return '活跃'
    case 'busy': return '忙碌'
    case 'idle': return '空闲'
    case 'offline': return '离线'
    default: return '未知'
  }
}

export default function Agents() {
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const { data: agents, loading, error, refetch } = useAgents(30000)

  // Filter agents
  const filteredAgents = useMemo(() => {
    return agents.filter(agent => {
      const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          agent.description?.toLowerCase().includes(searchQuery.toLowerCase())
      const matchesStatus = statusFilter === 'all' || agent.status === statusFilter
      return matchesSearch && matchesStatus
    })
  }, [agents, searchQuery, statusFilter])

  // Stats
  const stats = useMemo(() => ({
    total: agents.length,
    active: agents.filter(a => a.status === 'active').length,
    busy: agents.filter(a => a.status === 'busy').length,
    idle: agents.filter(a => a.status === 'idle').length,
    offline: agents.filter(a => a.status === 'offline').length
  }), [agents])

  const handleAction = async (action: string, agentId: string) => {
    try {
      await openclawAPI.executeAction(action, { agentId })
      refetch()
    } catch (err) {
      console.error('Action failed:', err)
    }
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
          <p className="text-slate-400">加载失败</p>
          <button 
            onClick={refetch}
            className="mt-4 px-4 py-2 bg-primary-600 rounded-lg text-white hover:bg-primary-500"
          >
            重试
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">员工 Agents</h1>
          <p className="text-slate-400 mt-1">
            管理 AI 员工，查看状态和性能
            {!loading && <span className="ml-2 text-slate-500">({stats.total} 个员工)</span>}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={refetch}
            disabled={loading}
            className="p-2 hover:bg-slate-800 rounded-lg transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-5 h-5 text-slate-400 ${loading ? 'animate-spin' : ''}`} />
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-500 rounded-lg text-white transition-colors">
            <Plus className="w-4 h-4" />
            <span>添加员工</span>
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-5 gap-4 mb-6">
        {[
          { label: '总计', value: stats.total, color: 'text-white' },
          { label: '活跃', value: stats.active, color: 'text-green-400' },
          { label: '忙碌', value: stats.busy, color: 'text-amber-400' },
          { label: '空闲', value: stats.idle, color: 'text-slate-400' },
          { label: '离线', value: stats.offline, color: 'text-red-400' },
        ].map((stat) => (
          <div key={stat.label} className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
            <p className="text-slate-500 text-sm">{stat.label}</p>
            <p className={`text-2xl font-bold ${stat.color}`}>
              {loading ? <Loader2 className="w-6 h-6 animate-spin" /> : stat.value}
            </p>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="搜索员工..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-primary-500"
          />
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-primary-500"
        >
          <option value="all">全部状态</option>
          <option value="active">活跃</option>
          <option value="busy">忙碌</option>
          <option value="idle">空闲</option>
          <option value="offline">离线</option>
        </select>
      </div>

      {/* Agents Grid */}
      {loading ? (
        <div className="flex-1 flex items-center justify-center">
          <Loader2 className="w-12 h-12 text-slate-500 animate-spin" />
        </div>
      ) : (
        <div className="flex-1 overflow-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {filteredAgents.map((agent) => {
              const Icon = getAgentIcon(agent.id)
              return (
                <div
                  key={agent.id}
                  className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors group"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div 
                        className="w-12 h-12 rounded-xl flex items-center justify-center"
                        style={{ backgroundColor: `${agent.color}20`, color: agent.color }}
                      >
                        <span className="text-2xl">{agent.icon}</span>
                      </div>
                      <div>
                        <h3 className="font-semibold text-white">{agent.name}</h3>
                        <p className="text-sm text-slate-400">{agent.title}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${getStatusColor(agent.status)}`} />
                      <span className="text-xs text-slate-400">{getStatusText(agent.status)}</span>
                    </div>
                  </div>

                  <p className="text-slate-400 text-sm mb-4 line-clamp-2">
                    {agent.description}
                  </p>

                  {/* Capabilities */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    {agent.features?.slice(0, 3).map((feature) => (
                      <span
                        key={feature.name}
                        className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-300"
                      >
                        {feature.name}
                      </span>
                    ))}
                  </div>

                  {/* Stats */}
                  <div className="flex items-center justify-between text-sm mb-4">
                    <span className="text-slate-500">
                      任务: {agent.taskCount || 0}
                    </span>
                    <span className="text-slate-500">
                      最后活跃: {agent.lastActive ? new Date(agent.lastActive).toLocaleDateString('zh-CN') : '未知'}
                    </span>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 pt-4 border-t border-slate-800">
                    <button 
                      onClick={() => handleAction('start', agent.id)}
                      className="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-green-500/10 hover:bg-green-500/20 text-green-400 rounded-lg transition-colors text-sm"
                    >
                      <Play className="w-4 h-4" />
                      启动
                    </button>
                    <button 
                      onClick={() => handleAction('pause', agent.id)}
                      className="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 rounded-lg transition-colors text-sm"
                    >
                      <Pause className="w-4 h-4" />
                      暂停
                    </button>
                    <button className="p-2 hover:bg-slate-800 rounded-lg transition-colors">
                      <Settings className="w-4 h-4 text-slate-400" />
                    </button>
                  </div>
                </div>
              )
            })}
          </div>

          {filteredAgents.length === 0 && !loading && (
            <div className="text-center py-12">
              <Bot className="w-12 h-12 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-500">没有找到匹配的员工</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
