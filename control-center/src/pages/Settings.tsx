import { useState } from 'react';
import { 
  Settings, 
  Bell, 
  Shield, 
  Database, 
  Globe, 
  Moon, 
  Sun, 
  User, 
  Key,
  Save,
  RefreshCw,
  CheckCircle,
  AlertTriangle,
  Info
} from 'lucide-react';

interface SettingSection {
  id: string;
  title: string;
  icon: React.ReactNode;
  description: string;
}

const sections: SettingSection[] = [
  { id: 'general', title: '常规设置', icon: <Settings size={20} />, description: '基本系统配置' },
  { id: 'notifications', title: '通知', icon: <Bell size={20} />, description: '消息提醒设置' },
  { id: 'security', title: '安全', icon: <Shield size={20} />, description: '安全与隐私' },
  { id: 'storage', title: '存储', icon: <Database size={20} />, description: '数据存储管理' },
  { id: 'network', title: '网络', icon: <Globe size={20} />, description: '连接配置' },
  { id: 'account', title: '账户', icon: <User size={20} />, description: '个人信息' },
];

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState('general');
  const [darkMode, setDarkMode] = useState(true);
  const [autoStart, setAutoStart] = useState(true);
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    desktop: false,
    sound: true,
  });
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const renderGeneralSettings = () => (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">外观</h3>
        <div className="flex items-center justify-between py-3 border-b border-slate-700/50">
          <div className="flex items-center gap-3">
            {darkMode ? <Moon size={20} className="text-indigo-400" /> : <Sun size={20} className="text-amber-400" />}
            <div>
              <p className="text-slate-200 font-medium">深色模式</p>
              <p className="text-slate-500 text-sm">使用深色主题</p>
            </div>
          </div>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`relative w-14 h-7 rounded-full transition-colors ${darkMode ? 'bg-indigo-600' : 'bg-slate-600'}`}
          >
            <span className={`absolute top-1 w-5 h-5 bg-white rounded-full transition-transform ${darkMode ? 'left-8' : 'left-1'}`} />
          </button>
        </div>
        <div className="flex items-center justify-between py-3">
          <div className="flex items-center gap-3">
            <RefreshCw size={20} className="text-emerald-400" />
            <div>
              <p className="text-slate-200 font-medium">开机自启</p>
              <p className="text-slate-500 text-sm">系统启动时自动运行</p>
            </div>
          </div>
          <button
            onClick={() => setAutoStart(!autoStart)}
            className={`relative w-14 h-7 rounded-full transition-colors ${autoStart ? 'bg-emerald-600' : 'bg-slate-600'}`}
          >
            <span className={`absolute top-1 w-5 h-5 bg-white rounded-full transition-transform ${autoStart ? 'left-8' : 'left-1'}`} />
          </button>
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">语言与区域</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">界面语言</label>
            <select className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">
              <option>简体中文</option>
              <option>繁體中文</option>
              <option>English</option>
              <option>日本語</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">时区</label>
            <select className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">
              <option>Asia/Shanghai (GMT+8)</option>
              <option>Asia/Tokyo (GMT+9)</option>
              <option>UTC</option>
              <option>America/New_York (EST)</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );

  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">通知渠道</h3>
        <div className="space-y-4">
          {[
            { key: 'email', label: '邮件通知', desc: '接收重要事件的邮件提醒', icon: <Info size={18} /> },
            { key: 'push', label: '推送通知', desc: '浏览器推送消息', icon: <Bell size={18} /> },
            { key: 'desktop', label: '桌面通知', desc: '系统桌面弹窗', icon: <AlertTriangle size={18} /> },
            { key: 'sound', label: '声音提醒', desc: '播放提示音', icon: <CheckCircle size={18} /> },
          ].map((item) => (
            <div key={item.key} className="flex items-center justify-between py-2">
              <div className="flex items-center gap-3">
                <span className="text-slate-400">{item.icon}</span>
                <div>
                  <p className="text-slate-200 font-medium">{item.label}</p>
                  <p className="text-slate-500 text-sm">{item.desc}</p>
                </div>
              </div>
              <button
                onClick={() => setNotifications({ ...notifications, [item.key]: !notifications[item.key as keyof typeof notifications] })}
                className={`relative w-12 h-6 rounded-full transition-colors ${notifications[item.key as keyof typeof notifications] ? 'bg-indigo-600' : 'bg-slate-600'}`}
              >
                <span className={`absolute top-0.5 w-5 h-5 bg-white rounded-full transition-transform ${notifications[item.key as keyof typeof notifications] ? 'left-6' : 'left-0.5'}`} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4 flex items-center gap-2">
          <Key size={20} className="text-amber-400" />
          API 密钥管理
        </h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">OpenAI API Key</label>
            <div className="flex gap-2">
              <input
                type="password"
                value="sk-••••••••••••••••••••••••••••••"
                readOnly
                className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-400"
              />
              <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-slate-200 transition-colors">
                更新
              </button>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">Feishu Webhook</label>
            <div className="flex gap-2">
              <input
                type="password"
                value="https://••••••••••••••••••••••••••••••"
                readOnly
                className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-400"
              />
              <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-slate-200 transition-colors">
                更新
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4 flex items-center gap-2">
          <Shield size={20} className="text-emerald-400" />
          访问控制
        </h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2">
            <span className="text-slate-200">双因素认证</span>
            <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-full text-sm">已启用</span>
          </div>
          <div className="flex items-center justify-between py-2">
            <span className="text-slate-200">登录通知</span>
            <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-full text-sm">已启用</span>
          </div>
          <div className="flex items-center justify-between py-2">
            <span className="text-slate-200">会话超时</span>
            <select className="bg-slate-900 border border-slate-700 rounded px-3 py-1 text-slate-200 text-sm">
              <option>30 分钟</option>
              <option>1 小时</option>
              <option>4 小时</option>
              <option>永不</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );

  const renderStorageSettings = () => (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">存储使用情况</h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-slate-400">文档存储</span>
              <span className="text-slate-200">2.4 GB / 10 GB</span>
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div className="h-full w-[24%] bg-indigo-500 rounded-full" />
            </div>
          </div>
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-slate-400">记忆数据</span>
              <span className="text-slate-200">156 MB / 1 GB</span>
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div className="h-full w-[15%] bg-emerald-500 rounded-full" />
            </div>
          </div>
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-slate-400">日志文件</span>
              <span className="text-slate-200">890 MB / 2 GB</span>
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div className="h-full w-[45%] bg-amber-500 rounded-full" />
            </div>
          </div>
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">数据管理</h3>
        <div className="space-y-3">
          <button className="w-full flex items-center justify-between p-3 bg-slate-900/50 rounded-lg hover:bg-slate-900 transition-colors">
            <span className="text-slate-200">导出所有数据</span>
            <span className="text-slate-500 text-sm">JSON</span>
          </button>
          <button className="w-full flex items-center justify-between p-3 bg-slate-900/50 rounded-lg hover:bg-slate-900 transition-colors">
            <span className="text-slate-200">清理缓存</span>
            <span className="text-slate-500 text-sm">128 MB</span>
          </button>
          <button className="w-full flex items-center justify-between p-3 bg-red-900/20 rounded-lg hover:bg-red-900/30 transition-colors">
            <span className="text-red-400">清除所有记忆</span>
            <span className="text-red-500 text-sm">危险</span>
          </button>
        </div>
      </div>
    </div>
  );

  const renderNetworkSettings = () => (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">代理设置</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-slate-200">使用代理</span>
            <button className="relative w-12 h-6 rounded-full bg-slate-600">
              <span className="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full" />
            </button>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-2">代理地址</label>
              <input
                type="text"
                placeholder="127.0.0.1"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-2">端口</label>
              <input
                type="text"
                placeholder="7890"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">连接状态</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2">
            <span className="text-slate-400">OpenClaw Gateway</span>
            <span className="flex items-center gap-2 text-emerald-400">
              <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
              已连接
            </span>
          </div>
          <div className="flex items-center justify-between py-2">
            <span className="text-slate-400">Feishu API</span>
            <span className="flex items-center gap-2 text-emerald-400">
              <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
              正常
            </span>
          </div>
          <div className="flex items-center justify-between py-2">
            <span className="text-slate-400">WebSocket</span>
            <span className="flex items-center gap-2 text-emerald-400">
              <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
              在线
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderAccountSettings = () => (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">个人信息</h3>
        <div className="flex items-center gap-4 mb-6">
          <div className="w-20 h-20 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-3xl font-bold text-white">
            S
          </div>
          <div>
            <p className="text-xl font-semibold text-slate-100">Sir</p>
            <p className="text-slate-400">Administrator</p>
            <p className="text-slate-500 text-sm">admin@openclaw.local</p>
          </div>
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">显示名称</label>
            <input
              type="text"
              defaultValue="Sir"
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">邮箱</label>
            <input
              type="email"
              defaultValue="admin@openclaw.local"
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
            />
          </div>
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-slate-100 mb-4">密码</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">当前密码</label>
            <input
              type="password"
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">新密码</label>
            <input
              type="password"
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-indigo-500"
            />
          </div>
          <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-white transition-colors">
            更新密码
          </button>
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeSection) {
      case 'general': return renderGeneralSettings();
      case 'notifications': return renderNotificationSettings();
      case 'security': return renderSecuritySettings();
      case 'storage': return renderStorageSettings();
      case 'network': return renderNetworkSettings();
      case 'account': return renderAccountSettings();
      default: return renderGeneralSettings();
    }
  };

  return (
    <div className="h-full flex">
      {/* Sidebar */}
      <div className="w-64 border-r border-slate-700/50 bg-slate-900/30">
        <div className="p-4">
          <h2 className="text-lg font-semibold text-slate-100 mb-4 flex items-center gap-2">
            <Settings size={20} className="text-indigo-400" />
            设置
          </h2>
          <nav className="space-y-1">
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-colors ${
                  activeSection === section.id
                    ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`}
              >
                {section.icon}
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm">{section.title}</p>
                  <p className="text-xs opacity-70 truncate">{section.description}</p>
                </div>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-slate-100">
                {sections.find(s => s.id === activeSection)?.title}
              </h1>
              <p className="text-slate-500 mt-1">
                {sections.find(s => s.id === activeSection)?.description}
              </p>
            </div>
            <button
              onClick={handleSave}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                saved
                  ? 'bg-emerald-600 text-white'
                  : 'bg-indigo-600 hover:bg-indigo-500 text-white'
              }`}
            >
              {saved ? <CheckCircle size={18} /> : <Save size={18} />}
              {saved ? '已保存' : '保存更改'}
            </button>
          </div>
          {renderContent()}
        </div>
      </div>
    </div>
  );
}
