import { useState } from 'react'
import {
  Brain,
  Search,
  Filter,
  Trash2,
  Download,
  Upload,
  MoreHorizontal,
  Clock,
  Tag,
  MessageSquare,
  FileText,
  Calendar,
  ChevronRight,
  Database,
  HardDrive,
  Zap
} from 'lucide-react'

const memoryStats = {
  totalEntries: 15432,
  totalSize: '2.4 GB',
  lastBackup: '2024-03-17 08:00',
  growthRate: '+12%',
}

const memoryEntries = [
  {
    id: 1,
    type: 'conversation',
    title: '项目讨论：OpenClaw 控制面板',
    content: '讨论了控制面板的设计方案，包括深色主题、导航结构和数据可视化...',
    tags: ['项目', 'UI设计', '重要'],
    timestamp: '2024-03-17 14:30',
    size: '24 KB',
    agent: 'Jarvis',
  },
  {
    id: 2,
    type: 'document',
    title: 'API 文档：用户认证接口',
    content: '记录了 OAuth2 认证流程的实现细节，包括 token 刷新机制...',
    tags: ['技术文档', 'API', '认证'],
    timestamp: '2024-03-17 12:15',
    size: '156 KB',
    agent: 'TARS',
  },
  {
    id: 3,
    type: 'task',
    title: '待办：优化数据库查询',
    content: '需要优化用户查询接口的性能，考虑添加缓存层...',
    tags: ['待办', '性能优化', '数据库'],
    timestamp: '2024-03-17 10:00',
    size: '8 KB',
    agent: 'Friday',
  },
  {
    id: 4,
    type: 'conversation',
    title: '会议记录：周会',
    content: '本周工作总结：完成了用户模块开发，下周计划进行测试...',
    tags: ['会议', '周报'],
    timestamp: '2024-03-16 16:00',
    size: '45 KB',
    agent: 'Jarvis',
  },
  {
    id: 5,
    type: 'document',
    title: '数据分析报告：Q1 用户增长',
    content: '第一季度用户增长数据分析，DAU 增长 35%，MAU 增长 28%...',
    tags: ['数据分析', '报告', 'Q1'],
    timestamp: '2024-03-16 09:30',
    size: '2.1 MB',
    agent: 'Friday',
  },
  {
    id: 6,
    type: 'conversation',
    title: '技术讨论：微服务架构',
    content: '探讨了将单体应用拆分为微服务的可行性和实施计划...',
    tags: ['架构', '技术讨论', '微服务'],
    timestamp: '2024-03-15 15:20',
    size: '67 KB',
    agent: 'TARS',
  },
]

const typeIcons: Record<string, React.ElementType> = {
  conversation: MessageSquare,
  document: FileText,
  task: Calendar,
}

const typeColors: Record<string, string> = {
  conversation: 'bg-blue-500/10 text-blue-400',
  document: 'bg-green-500/10 text-green-400',
  task: 'bg-orange-500/10 text-orange-400',
}

const categories = [
  { label: '全部', count: 15432 },
  { label: '对话', count: 8234 },
  { label: '文档', count: 4521 },
  { label: '任务', count: 2677 },
]

export default function Memory() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('全部')
  const [selectedEntries, setSelectedEntries] = useState<number[]>([])

  const toggleEntrySelection = (id: number) => {
    setSelectedEntries((prev) =>
      prev.includes(id) ? prev.filter((e) => e !== id) : [...prev, id]
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">记忆 Memory</h1>
          <p className="text-dark-400 mt-1">管理和检索 AI 员工的记忆数据</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 bg-dark-800 hover:bg-dark-700 text-dark-200 px-4 py-2 rounded-lg transition-colors">
            <Upload className="w-4 h-4" />
            <span>导入</span>
          </button>
          <button className="flex items-center gap-2 bg-dark-800 hover:bg-dark-700 text-dark-200 px-4 py-2 rounded-lg transition-colors">
            <Download className="w-4 h-4" />
            <span>导出</span>
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-dark-900 border border-dark-800 rounded-xl p-5">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-primary-500/10 rounded-xl">
              <Database className="w-5 h-5 text-primary-400" />
            </div>
            <div>
              <p className="text-dark-400 text-sm">记忆条目</p>
              <p className="text-xl font-bold text-white">{memoryStats.totalEntries.toLocaleString()}</p>
            </div>
          </div>
        </div>
        <div className="bg-dark-900 border border-dark-800 rounded-xl p-5">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-purple-500/10 rounded-xl">
              <HardDrive className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <p className="text-dark-400 text-sm">存储空间</p>
              <p className="text-xl font-bold text-white">{memoryStats.totalSize}</p>
            </div>
          </div>
        </div>
        <div className="bg-dark-900 border border-dark-800 rounded-xl p-5">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-green-500/10 rounded-xl">
              <Clock className="w-5 h-5 text-green-400" />
            </div>
            <div>
              <p className="text-dark-400 text-sm">上次备份</p>
              <p className="text-xl font-bold text-white">{memoryStats.lastBackup}</p>
            </div>
          </div>
        </div>
        <div className="bg-dark-900 border border-dark-800 rounded-xl p-5">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-orange-500/10 rounded-xl">
              <Zap className="w-5 h-5 text-orange-400" />
            </div>
            <div>
              <p className="text-dark-400 text-sm">增长率</p>
              <p className="text-xl font-bold text-green-400">{memoryStats.growthRate}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-500" />
          <input
            type="text"
            placeholder="搜索记忆..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-dark-900 border border-dark-800 rounded-lg pl-10 pr-4 py-2.5 text-sm placeholder:text-dark-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500/50"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-dark-400" />
          <select className="bg-dark-900 border border-dark-800 rounded-lg px-4 py-2.5 text-sm text-dark-200 focus:outline-none focus:ring-2 focus:ring-primary-500/20">
            <option>按时间排序</option>
            <option>按大小排序</option>
            <option>按类型排序</option>
          </select>
        </div>
      </div>

      {/* Category Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {categories.map((cat) => (
          <button
            key={cat.label}
            onClick={() => setSelectedCategory(cat.label)}
            className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-colors ${
              selectedCategory === cat.label
                ? 'bg-primary-600 text-white'
                : 'bg-dark-800 text-dark-400 hover:text-white'
            }`}
          >
            {cat.label}
            <span className="ml-2 text-xs opacity-60">({cat.count.toLocaleString()})</span>
          </button>
        ))}
      </div>

      {/* Memory List */}
      <div className="space-y-3">
        {memoryEntries.map((entry) => {
          const TypeIcon = typeIcons[entry.type]
          return (
            <div
              key={entry.id}
              className="bg-dark-900 border border-dark-800 rounded-xl p-5 hover:border-dark-700 transition-all group"
            >
              <div className="flex items-start gap-4">
                {/* Checkbox */}
                <input
                  type="checkbox"
                  checked={selectedEntries.includes(entry.id)}
                  onChange={() => toggleEntrySelection(entry.id)}
                  className="mt-1 w-4 h-4 rounded border-dark-600 bg-dark-800 text-primary-600 focus:ring-primary-500/20"
                />

                {/* Icon */}
                <div className={`p-2 rounded-lg ${typeColors[entry.type]}`}>
                  <TypeIcon className="w-5 h-5" />
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className="font-medium text-white group-hover:text-primary-400 transition-colors">
                        {entry.title}
                      </h3>
                      <p className="text-dark-400 text-sm mt-1 line-clamp-2">
                        {entry.content}
                      </p>
                    </div>
                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button className="p-1.5 hover:bg-dark-800 rounded-lg transition-colors">
                        <Download className="w-4 h-4 text-dark-400" />
                      </button>
                      <button className="p-1.5 hover:bg-dark-800 rounded-lg transition-colors">
                        <Trash2 className="w-4 h-4 text-dark-400" />
                      </button>
                      <button className="p-1.5 hover:bg-dark-800 rounded-lg transition-colors">
                        <MoreHorizontal className="w-4 h-4 text-dark-400" />
                      </button>
                    </div>
                  </div>

                  {/* Meta */}
                  <div className="flex items-center gap-4 mt-3">
                    <div className="flex items-center gap-1.5 text-dark-500 text-xs">
                      <Clock className="w-3.5 h-3.5" />
                      <span>{entry.timestamp}</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-dark-500 text-xs">
                      <Database className="w-3.5 h-3.5" />
                      <span>{entry.size}</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-dark-500 text-xs">
                      <Brain className="w-3.5 h-3.5" />
                      <span>{entry.agent}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      {entry.tags.map((tag) => (
                        <span
                          key={tag}
                          className="px-2 py-0.5 bg-dark-800 text-dark-400 text-xs rounded-full"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Arrow */}
                <ChevronRight className="w-5 h-5 text-dark-600 group-hover:text-dark-400 transition-colors" />
              </div>
            </div>
          )
        })}
      </div>

      {/* Load More */}
      <div className="text-center">
        <button className="px-6 py-2.5 bg-dark-800 hover:bg-dark-700 text-dark-300 rounded-lg transition-colors text-sm">
          加载更多
        </button>
      </div>
    </div>
  )
}