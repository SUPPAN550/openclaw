import { useState } from 'react'
import { Routes, Route, NavLink } from 'react-router-dom'
import {
  Users,
  LayoutDashboard,
  Brain,
  FileText,
  BarChart3,
  CheckSquare,
  Settings,
  Menu,
  X,
  ChevronRight,
  Bell,
  Search
} from 'lucide-react'
import Dashboard from './pages/Dashboard'
import Agents from './pages/Agents'
import Memory from './pages/Memory'
import Documents from './pages/Documents'
import Usage from './pages/Usage'
import Tasks from './pages/Tasks'
import SettingsPage from './pages/Settings'

const navItems = [
  { path: '/', label: '总览', labelEn: 'Dashboard', icon: LayoutDashboard },
  { path: '/agents', label: '员工', labelEn: 'Agents', icon: Users },
  { path: '/memory', label: '记忆', labelEn: 'Memory', icon: Brain },
  { path: '/documents', label: '文档', labelEn: 'Documents', icon: FileText },
  { path: '/usage', label: '用量', labelEn: 'Usage', icon: BarChart3 },
  { path: '/tasks', label: '任务', labelEn: 'Tasks', icon: CheckSquare },
  { path: '/settings', label: '设置', labelEn: 'Settings', icon: Settings },
]

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="min-h-screen bg-dark-950 text-dark-100 flex">
      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-dark-900 border-r border-dark-800 transition-transform duration-300 ease-in-out lg:static lg:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between px-6 py-5 border-b border-dark-800">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">OC</span>
              </div>
              <div>
                <h1 className="font-semibold text-white text-sm">OpenClaw</h1>
                <p className="text-xs text-dark-400">Control Center</p>
              </div>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-1.5 hover:bg-dark-800 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group ${
                      isActive
                        ? 'bg-primary-600/10 text-primary-400 border border-primary-600/20'
                        : 'text-dark-400 hover:bg-dark-800 hover:text-dark-200'
                    }`
                  }
                >
                  <Icon className="w-5 h-5" />
                  <div className="flex-1">
                    <span className="font-medium text-sm">{item.label}</span>
                    <span className="block text-xs opacity-60">{item.labelEn}</span>
                  </div>
                  <ChevronRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                </NavLink>
              )
            })}
          </nav>

          {/* User Profile */}
          <div className="p-4 border-t border-dark-800">
            <div className="flex items-center gap-3 px-4 py-3 bg-dark-800/50 rounded-xl">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-full flex items-center justify-center">
                <span className="text-white font-semibold text-sm">S</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">Sir</p>
                <p className="text-xs text-dark-400 truncate">Administrator</p>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="sticky top-0 z-40 bg-dark-950/80 backdrop-blur-xl border-b border-dark-800">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(true)}
                className={`lg:hidden p-2 hover:bg-dark-800 rounded-lg transition-colors ${
                  sidebarOpen ? 'hidden' : ''
                }`}
              >
                <Menu className="w-5 h-5" />
              </button>
              <div className="relative hidden sm:block">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-500" />
                <input
                  type="text"
                  placeholder="搜索..."
                  className="w-64 bg-dark-900 border border-dark-800 rounded-lg pl-10 pr-4 py-2 text-sm placeholder:text-dark-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500/50"
                />
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button className="relative p-2 hover:bg-dark-800 rounded-lg transition-colors">
                <Bell className="w-5 h-5 text-dark-400" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>
              <div className="w-px h-6 bg-dark-800 mx-1"></div>
              <span className="text-sm text-dark-400 hidden sm:inline">v1.0.0</span>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/memory" element={<Memory />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/usage" element={<Usage />} />
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </main>
      </div>

      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}

export default App