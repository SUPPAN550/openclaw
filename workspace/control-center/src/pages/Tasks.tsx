import { useState, useMemo } from 'react'
import {
  CheckSquare,
  Plus,
  Search,
  Filter,
  MoreHorizontal,
  Calendar,
  User,
  Tag,
  Clock,
  Loader2,
  RefreshCw,
  AlertCircle
} from 'lucide-react'
import { useTasks } from '../hooks/useOpenClaw'
import { openclawAPI } from '../api/openclaw'
import type { Task } from '../types'

const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'bg-green-500/10 text-green-400 border-green-500/20'
    case 'in_progress': return 'bg-blue-500/10 text-blue-400 border-blue-500/20'
    case 'pending': return 'bg-amber-500/10 text-amber-400 border-amber-500/20'
    case 'failed': return 'bg-red-500/10 text-red-400 border-red-500/20'
    default: return 'bg-slate-500/10 text-slate-400 border-slate-500/20'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'completed': return '已完成'
    case 'in_progress': return '进行中'
    case 'pending': return '待处理'
    case 'failed': return '失败'
    default: return '未知'
  }
}

const getPriorityColor = (priority: string) => {
  switch (priority) {
    case 'high': return 'text-red-400'
    case 'medium': return 'text-amber-400'
    case 'low': return 'text-slate-400'
    default: return 'text-slate-400'
  }
}

export default function Tasks() {
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const { data: tasks, loading, error, refetch } = useTasks(30000)

  // Filter tasks
  const filteredTasks = useMemo(() => {
    return tasks.filter(task => {
      const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          task.description?.toLowerCase().includes(searchQuery.toLowerCase())
      const matchesStatus = statusFilter === 'all' || task.status === statusFilter
      return matchesSearch && matchesStatus
    })
  }, [tasks, searchQuery, statusFilter])

  // Stats
  const stats = useMemo(() => ({
    total: tasks.length,
    pending: tasks.filter(t => t.status === 'pending').length,
    inProgress: tasks.filter(t => t.status === 'in_progress').length,
    completed: tasks.filter(t => t.status === 'completed').length
  }), [tasks])

  const handleStatusChange = async (taskId: string, newStatus: string) => {
    try {
      await openclawAPI.executeAction('update_task', { taskId, status: newStatus })
      refetch()
    } catch (err) {
      console.error('Failed to update task:', err)
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
          <h1 className="text-2xl font-bold text-white">任务 Tasks</h1>
          <p className="text-slate-400 mt-1">管理和跟踪团队任务进度</p>
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
            <span>新建任务</span>
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-slate-800 rounded-lg">
              <CheckSquare className="w-5 h-5 text-slate-400" />
            </div>
            <div>
              <p className="text-slate-500 text-sm">总任务</p>
              <p className="text-xl font-bold text-white">
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : stats.total}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-amber-500/10 rounded-lg">
              <Clock className="w-5 h-5 text-amber-400" />
            </div>
            <div>
              <p className="text-slate-500 text-sm">待处理</p>
              <p className="text-xl font-bold text-amber-400">
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : stats.pending}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <Clock className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <p className="text-slate-500 text-sm">进行中</p>
              <p className="text-xl font-bold text-blue-400">
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : stats.inProgress}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-500/10 rounded-lg">
              <CheckSquare className="w-5 h-5 text-green-400" />
            </div>
            <div>
              <p className="text-slate-500 text-sm">已完成</p>
              <p className="text-xl font-bold text-green-400">
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : stats.completed}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="搜索任务..."
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
          <option value="pending">待处理</option>
          <option value="in_progress">进行中</option>
          <option value="completed">已完成</option>
        </select>
      </div>

      {/* Task List */}
      {loading ? (
        <div className="flex-1 flex items-center justify-center">
          <Loader2 className="w-12 h-12 text-slate-500 animate-spin" />
        </div>
      ) : (
        <div className="flex-1 overflow-auto space-y-3">
          {filteredTasks.map((task) => (
            <div
              key={task.id}
              className="bg-slate-900/50 border border-slate-800 rounded-xl p-4 hover:border-slate-700 transition-colors"
            >
              <div className="flex items-start gap-4">
                <input
                  type="checkbox"
                  checked={task.status === 'completed'}
                  onChange={() => handleStatusChange(task.id, task.status === 'completed' ? 'pending' : 'completed')}
                  className="mt-1 w-5 h-5 rounded border-slate-600 bg-slate-800 text-primary-600 focus:ring-primary-500"
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className={`font-medium ${task.status === 'completed' ? 'text-slate-500 line-through' : 'text-white'}`}>
                        {task.title}
                      </h3>
                      <p className="text-slate-400 text-sm mt-1">{task.description}</p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs border ${getStatusColor(task.status)}`}>
                      {getStatusText(task.status)}
                    </span>
                  </div>

                  <div className="flex items-center gap-6 mt-3 text-sm">
                    {task.assignee && (
                      <div className="flex items-center gap-1.5 text-slate-400">
                        <User className="w-4 h-4" />
                        <span>{task.assignee}</span>
                      </div>
                    )}
                    {task.dueDate && (
                      <div className="flex items-center gap-1.5 text-slate-400">
                        <Calendar className="w-4 h-4" />
                        <span>{new Date(task.dueDate).toLocaleDateString('zh-CN')}</span>
                      </div>
                    )}
                    <div className={`flex items-center gap-1.5 ${getPriorityColor(task.priority)}`}>
                      <Tag className="w-4 h-4" />
                      <span>{task.priority === 'high' ? '高' : task.priority === 'medium' ? '中' : '低'}优先级</span>
                    </div>
                  </div>

                  {/* Progress */}
                  {task.status === 'in_progress' && (
                    <div className="mt-3">
                      <div className="flex items-center justify-between text-xs mb-1">
                        <span className="text-slate-400">进度</span>
                        <span className="text-white">{task.progress}%</span>
                      </div>
                      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-primary-500 rounded-full transition-all"
                          style={{ width: `${task.progress}%` }}
                        />
                      </div>
                    </div>
                  )}

                  {/* Tags */}
                  {task.tags && task.tags.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-3">
                      {task.tags.map((tag) => (
                        <span key={tag} className="px-2 py-0.5 bg-slate-800 rounded text-xs text-slate-400">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <button className="p-2 hover:bg-slate-800 rounded-lg transition-colors">
                  <MoreHorizontal className="w-4 h-4 text-slate-400" />
                </button>
              </div>
            </div>
          ))}

          {filteredTasks.length === 0 && !loading && (
            <div className="text-center py-12">
              <CheckSquare className="w-12 h-12 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-500">没有找到匹配的任务</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
