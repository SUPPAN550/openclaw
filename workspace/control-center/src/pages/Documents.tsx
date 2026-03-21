import { useState } from 'react'
import {
  FileText,
  Folder,
  Plus,
  Search,
  Grid,
  List,
  MoreHorizontal,
  Download,
  Share2,
  Trash2,
  Edit,
  Clock,
  User,
  File,
  Image,
  Table,
  Presentation,
  ChevronRight,
  Upload,
  Filter
} from 'lucide-react'

const folders = [
  { id: 1, name: '全部文档', count: 156 },
  { id: 2, name: '最近使用', count: 12 },
  { id: 3, name: '与我共享', count: 8 },
  { id: 4, name: '我的收藏', count: 23 },
  { id: 5, name: '回收站', count: 5 },
]

const documents = [
  {
    id: 1,
    name: '产品需求文档：OpenClaw v2.0',
    type: 'doc',
    size: '2.4 MB',
    updatedAt: '2024-03-17 14:30',
    author: 'Jarvis',
    folder: '产品文档',
  },
  {
    id: 2,
    name: 'Q1 财务报表.xlsx',
    type: 'sheet',
    size: '856 KB',
    updatedAt: '2024-03-17 11:20',
    author: 'Friday',
    folder: '财务',
  },
  {
    id: 3,
    name: '系统架构图',
    type: 'image',
    size: '1.2 MB',
    updatedAt: '2024-03-16 16:45',
    author: 'TARS',
    folder: '设计',
  },
  {
    id: 4,
    name: 'API 接口文档',
    type: 'doc',
    size: '456 KB',
    updatedAt: '2024-03-16 10:00',
    author: 'TARS',
    folder: '技术文档',
  },
  {
    id: 5,
    name: '用户调研报告.pptx',
    type: 'presentation',
    size: '5.6 MB',
    updatedAt: '2024-03-15 15:30',
    author: 'Friday',
    folder: '产品文档',
  },
  {
    id: 6,
    name: '数据库设计文档',
    type: 'doc',
    size: '1.8 MB',
    updatedAt: '2024-03-15 09:00',
    author: 'TARS',
    folder: '技术文档',
  },
  {
    id: 7,
    name: '会议纪要：周会 2024-03-15',
    type: 'doc',
    size: '234 KB',
    updatedAt: '2024-03-15 17:00',
    author: 'Jarvis',
    folder: '会议记录',
  },
  {
    id: 8,
    name: '竞品分析报告',
    type: 'doc',
    size: '3.2 MB',
    updatedAt: '2024-03-14 14:00',
    author: 'Friday',
    folder: '产品文档',
  },
]

const typeIcons: Record<string, React.ElementType> = {
  doc: FileText,
  sheet: Table,
  image: Image,
  presentation: Presentation,
  folder: Folder,
  file: File,
}

const typeColors: Record<string, string> = {
  doc: 'bg-blue-500/10 text-blue-400',
  sheet: 'bg-green-500/10 text-green-400',
  image: 'bg-purple-500/10 text-purple-400',
  presentation: 'bg-orange-500/10 text-orange-400',
  folder: 'bg-yellow-500/10 text-yellow-400',
  file: 'bg-dark-500/10 text-dark-400',
}

const typeLabels: Record<string, string> = {
  doc: '文档',
  sheet: '表格',
  image: '图片',
  presentation: '演示文稿',
  folder: '文件夹',
  file: '文件',
}

export default function Documents() {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('list')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedFolder, setSelectedFolder] = useState(1)
  const [selectedDocs, setSelectedDocs] = useState<number[]>([])

  const filteredDocs = documents.filter((doc) =>
    doc.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const toggleDocSelection = (id: number) => {
    setSelectedDocs((prev) =>
      prev.includes(id) ? prev.filter((d) => d !== id) : [...prev, id]
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">文档 Documents</h1>
          <p className="text-dark-400 mt-1">管理和协作处理团队文档</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 bg-dark-800 hover:bg-dark-700 text-dark-200 px-4 py-2 rounded-lg transition-colors">
            <Upload className="w-4 h-4" />
            <span>上传</span>
          </button>
          <button className="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors">
            <Plus className="w-4 h-4" />
            <span>新建</span>
          </button>
        </div>
      </div>

      <div className="flex gap-6">
        {/* Sidebar */}
        <aside className="w-60 flex-shrink-0 space-y-1">
          {folders.map((folder) => (
            <button
              key={folder.id}
              onClick={() => setSelectedFolder(folder.id)}
              className={`w-full flex items-center justify-between px-4 py-2.5 rounded-lg text-sm transition-colors ${
                selectedFolder === folder.id
                  ? 'bg-primary-600/10 text-primary-400'
                  : 'text-dark-400 hover:bg-dark-800 hover:text-dark-200'
              }`}
            >
              <span className="flex items-center gap-2">
                <Folder className="w-4 h-4" />
                {folder.name}
              </span>
              <span className="text-xs opacity-60">{folder.count}</span>
            </button>
          ))}

          <div className="pt-4 mt-4 border-t border-dark-800">
            <p className="px-4 text-xs text-dark-500 uppercase tracking-wider mb-2">存储空间</p>
            <div className="px-4">
              <div className="h-2 bg-dark-800 rounded-full overflow-hidden">
                <div className="h-full w-3/4 bg-gradient-to-r from-primary-500 to-purple-500 rounded-full" />
              </div>
              <p className="text-xs text-dark-400 mt-2">7.5 GB / 10 GB 已使用</p>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <div className="flex-1 min-w-0">
          {/* Toolbar */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4 flex-1">
              <div className="relative w-64">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-500" />
                <input
                  type="text"
                  placeholder="搜索文档..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-dark-900 border border-dark-800 rounded-lg pl-10 pr-4 py-2 text-sm placeholder:text-dark-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500/50"
                />
              </div>
              <button className="flex items-center gap-2 text-dark-400 hover:text-white text-sm">
                <Filter className="w-4 h-4" />
                筛选
              </button>
            </div>
            <div className="flex items-center gap-1 bg-dark-900 rounded-lg p-1 border border-dark-800">
              <button
                onClick={() => setViewMode('list')}
                className={`p-1.5 rounded transition-colors ${
                  viewMode === 'list' ? 'bg-dark-800 text-white' : 'text-dark-400 hover:text-white'
                }`}
              >
                <List className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode('grid')}
                className={`p-1.5 rounded transition-colors ${
                  viewMode === 'grid' ? 'bg-dark-800 text-white' : 'text-dark-400 hover:text-white'
                }`}
              >
                <Grid className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Documents */}
          {viewMode === 'list' ? (
            <div className="bg-dark-900 border border-dark-800 rounded-xl overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-dark-800">
                    <th className="px-4 py-3 text-left">
                      <input
                        type="checkbox"
                        className="w-4 h-4 rounded border-dark-600 bg-dark-800 text-primary-600"
                      />
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-dark-400 uppercase">名称</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-dark-400 uppercase">文件夹</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-dark-400 uppercase">作者</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-dark-400 uppercase">更新时间</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-dark-400 uppercase">大小</th>
                    <th className="px-4 py-3 text-right"></th>
                  </tr>
                </thead>
                <tbody>
                  {filteredDocs.map((doc) => {
                    const TypeIcon = typeIcons[doc.type]
                    return (
                      <tr
                        key={doc.id}
                        className="border-b border-dark-800 last:border-0 hover:bg-dark-800/50 transition-colors"
                      >
                        <td className="px-4 py-3">
                          <input
                            type="checkbox"
                            checked={selectedDocs.includes(doc.id)}
                            onChange={() => toggleDocSelection(doc.id)}
                            className="w-4 h-4 rounded border-dark-600 bg-dark-800 text-primary-600"
                          />
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-3">
                            <div className={`p-2 rounded-lg ${typeColors[doc.type]}`}>
                              <TypeIcon className="w-4 h-4" />
                            </div>
                            <span className="text-white text-sm">{doc.name}</span>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-dark-400 text-sm">{doc.folder}</td>
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-2">
                            <div className="w-6 h-6 bg-gradient-to-br from-primary-500 to-purple-600 rounded-full flex items-center justify-center">
                              <span className="text-white text-xs font-medium">{doc.author[0]}</span>
                            </div>
                            <span className="text-dark-300 text-sm">{doc.author}</span>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-dark-400 text-sm">{doc.updatedAt}</td>
                        <td className="px-4 py-3 text-dark-400 text-sm">{doc.size}</td>
                        <td className="px-4 py-3 text-right">
                          <button className="p-1.5 hover:bg-dark-800 rounded-lg transition-colors">
                            <MoreHorizontal className="w-4 h-4 text-dark-400" />
                          </button>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filteredDocs.map((doc) => {
                const TypeIcon = typeIcons[doc.type]
                return (
                  <div
                    key={doc.id}
                    className="bg-dark-900 border border-dark-800 rounded-xl p-4 hover:border-dark-700 transition-all group"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className={`p-3 rounded-xl ${typeColors[doc.type]}`}>
                        <TypeIcon className="w-6 h-6" />
                      </div>
                      <button className="p-1.5 hover:bg-dark-800 rounded-lg transition-colors opacity-0 group-hover:opacity-100">
                        <MoreHorizontal className="w-4 h-4 text-dark-400" />
                      </button>
                    </div>
                    <h3 className="font-medium text-white text-sm mb-1 line-clamp-2">{doc.name}</h3>
                    <p className="text-dark-500 text-xs mb-3">{typeLabels[doc.type]} · {doc.size}</p>
                    <div className="flex items-center justify-between pt-3 border-t border-dark-800">
                      <div className="flex items-center gap-1.5">
                        <div className="w-5 h-5 bg-gradient-to-br from-primary-500 to-purple-600 rounded-full flex items-center justify-center">
                          <span className="text-white text-xs">{doc.author[0]}</span>
                        </div>
                        <span className="text-dark-400 text-xs">{doc.author}</span>
                      </div>
                      <span className="text-dark-500 text-xs">{doc.updatedAt.split(' ')[0]}</span>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}