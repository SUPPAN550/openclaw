// OpenClaw Hub 前端 JavaScript

const API_BASE = '';
let agents = [];
let currentConfigAgent = null;

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
    addLog('系统初始化中...', 'info');
    
    // 加载 Agent 列表
    await loadAgents();
    
    // 获取真实数据
    await checkConnection();
    await refreshStatus();
    await refreshResources();
    
    // 开始定时刷新
    setInterval(checkConnection, 10000);
    setInterval(refreshResources, 5000);
    setInterval(refreshStatus, 10000);
    
    addLog('系统初始化完成', 'info');
});

// 检查网关连接
async function checkConnection() {
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        const data = await response.json();
        
        const statusEl = document.getElementById('connection-status');
        if (data.success && data.connected) {
            statusEl.textContent = '已连接';
            statusEl.className = 'connection-status connected';
            addLog('网关连接正常', 'info');
        } else {
            statusEl.textContent = '未连接';
            statusEl.className = 'connection-status disconnected';
        }
    } catch (error) {
        const statusEl = document.getElementById('connection-status');
        statusEl.textContent = '未连接';
        statusEl.className = 'connection-status disconnected';
        addLog(`连接检查失败: ${error.message}`, 'error');
    }
}

// 加载 Agent 列表
async function loadAgents() {
    try {
        const response = await fetch(`${API_BASE}/api/agents`);
        const data = await response.json();
        
        if (data.success) {
            agents = data.data;
            renderAgents();
            addLog('Agent 列表加载成功', 'info');
        }
    } catch (error) {
        addLog(`加载 Agent 失败: ${error.message}`, 'error');
    }
}

// 渲染 Agent 卡片
function renderAgents() {
    const grid = document.getElementById('agent-grid');
    grid.innerHTML = agents.map(agent => `
        <div class="agent-card" data-agent="${agent.id}">
            <div class="status-indicator ${agent.status}"></div>
            <div class="agent-header">
                <div class="agent-avatar">${agent.animal}</div>
                <div class="agent-info">
                    <h3>${agent.name}</h3>
                    <div class="role">${agent.role}</div>
                </div>
            </div>
            <div class="agent-status">
                <div class="status-row">
                    <span class="status-label">当前状态</span>
                    <span class="status-value ${agent.status === 'working' ? 'working' : ''}">
                        ${getStatusText(agent.status)}
                    </span>
                </div>
                <div class="status-row">
                    <span class="status-label">模型</span>
                    <span class="status-value">${agent.model}</span>
                </div>
                <div class="status-row">
                    <span class="status-label">定时任务</span>
                    <span class="status-value">${agent.schedule}</span>
                </div>
                <div class="status-row">
                    <span class="status-label">最近产出</span>
                    <span class="status-value">${agent.lastOutput}</span>
                </div>
            </div>
            <div class="agent-actions">
                <button class="btn btn-primary" onclick="startAgent('${agent.id}')" id="btn-start-${agent.id}">
                    启动
                </button>
                <button class="btn btn-secondary" onclick="openConfig('${agent.id}')">
                    配置
                </button>
            </div>
        </div>
    `).join('');
    
    updateActiveAgentList();
}

// 获取状态文本
function getStatusText(status) {
    const map = {
        'online': '待命',
        'working': '工作中',
        'idle': '空闲',
        'offline': '离线'
    };
    return map[status] || status;
}

// 更新活跃智能体列表
function updateActiveAgentList() {
    const list = document.getElementById('active-agent-list');
    const activeAgents = agents.filter(a => a.status !== 'offline');
    
    list.innerHTML = activeAgents.map(agent => `
        <li class="agent-list-item">
            <span class="agent-list-avatar">${agent.animal}</span>
            <span class="agent-list-name">${agent.name}</span>
            <span class="agent-list-status ${agent.status === 'online' || agent.status === 'working' ? 'online' : ''}">
                ${getStatusText(agent.status)}
            </span>
        </li>
    `).join('');
}

// 刷新状态
async function refreshStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        const data = await response.json();
        
        if (data.success && data.data) {
            document.getElementById('active-sessions').textContent = data.data.sessions || 0;
            document.getElementById('pending-tasks').textContent = data.data.tasks || 0;
            document.getElementById('pending-approval').textContent = data.data.pending || 0;
        }
    } catch (error) {
        // 使用默认值
        document.getElementById('active-sessions').textContent = '5';
        document.getElementById('pending-tasks').textContent = '0';
        document.getElementById('pending-approval').textContent = '0';
    }
}

// 刷新资源监控
async function refreshResources() {
    try {
        const response = await fetch(`${API_BASE}/api/metrics`);
        const data = await response.json();
        
        if (data.success && data.data) {
            const { cpu, memory, storage } = data.data;
            
            document.getElementById('cpu-value').textContent = `${cpu}%`;
            document.getElementById('cpu-bar').style.width = `${cpu}%`;
            
            document.getElementById('memory-value').textContent = `${memory}%`;
            document.getElementById('memory-bar').style.width = `${memory}%`;
            
            document.getElementById('storage-value').textContent = `${storage}%`;
            document.getElementById('storage-bar').style.width = `${storage}%`;
        }
    } catch (error) {
        addLog(`资源刷新失败: ${error.message}`, 'error');
    }
}

// 启动 Agent
async function startAgent(agentId) {
    const btn = document.getElementById(`btn-start-${agentId}`);
    btn.disabled = true;
    btn.innerHTML = '<span class="loading"></span>';
    
    try {
        const response = await fetch(`${API_BASE}/api/agents/${agentId}/start`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            addLog(`Agent ${agentId} 启动成功`, 'info');
            // 更新状态
            const agent = agents.find(a => a.id === agentId);
            if (agent) {
                agent.status = 'working';
                renderAgents();
            }
        } else {
            showToast(data.error || '启动失败', 'error');
            addLog(`Agent ${agentId} 启动失败: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`启动失败: ${error.message}`, 'error');
        addLog(`Agent ${agentId} 启动失败: ${error.message}`, 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = '启动';
    }
}

// 打开配置
function openConfig(agentId) {
    const agent = agents.find(a => a.id === agentId);
    if (!agent) return;
    
    currentConfigAgent = agent;
    document.getElementById('config-name').value = agent.name;
    document.getElementById('config-model').value = agent.model;
    document.getElementById('config-schedule').value = agent.schedule;
    document.getElementById('config-modal').classList.add('active');
}

// 关闭配置
function closeConfig() {
    document.getElementById('config-modal').classList.remove('active');
    currentConfigAgent = null;
}

// 保存配置
async function saveConfig() {
    if (!currentConfigAgent) return;
    
    const model = document.getElementById('config-model').value;
    const schedule = document.getElementById('config-schedule').value;
    
    // 更新本地配置
    currentConfigAgent.model = model;
    currentConfigAgent.schedule = schedule;
    
    renderAgents();
    showToast('配置保存成功', 'success');
    addLog(`Agent ${currentConfigAgent.name} 配置已更新`, 'info');
    closeConfig();
}

// 快捷操作 - 进入 WebUI
function openWebUI() {
    window.open('http://127.0.0.1:18789', '_blank');
    addLog('打开 WebUI', 'info');
}

// 快捷操作 - 重启服务
async function restartService() {
    const btn = document.getElementById('btn-restart');
    btn.disabled = true;
    
    try {
        addLog('正在重启网关服务...', 'info');
        const response = await fetch(`${API_BASE}/api/gateway/restart`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            showToast('服务重启成功', 'success');
            addLog('网关服务重启成功', 'info');
        } else {
            showToast(data.error || '重启失败', 'error');
            addLog(`重启失败: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`重启失败: ${error.message}`, 'error');
        addLog(`重启失败: ${error.message}`, 'error');
    } finally {
        btn.disabled = false;
    }
}

// 快捷操作 - 版本检查
async function checkVersion() {
    const btn = document.getElementById('btn-version');
    btn.disabled = true;
    
    try {
        addLog('正在检查版本...', 'info');
        const response = await fetch(`${API_BASE}/api/gateway/version`);
        const data = await response.json();
        
        if (data.success) {
            showToast(`版本: ${data.version}`, 'success');
            addLog(`当前版本: ${data.version}`, 'info');
        } else {
            showToast(data.error || '检查失败', 'error');
            addLog(`版本检查失败: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`检查失败: ${error.message}`, 'error');
        addLog(`版本检查失败: ${error.message}`, 'error');
    } finally {
        btn.disabled = false;
    }
}

// 快捷操作 - 故障修复
async function fixIssues() {
    const btn = document.getElementById('btn-fix');
    btn.disabled = true;
    
    try {
        addLog('正在执行故障修复...', 'info');
        const response = await fetch(`${API_BASE}/api/gateway/fix`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            showToast('故障修复完成', 'success');
            addLog('故障修复完成', 'info');
            if (data.fixes && data.fixes.length > 0) {
                data.fixes.forEach(fix => addLog(fix, 'info'));
            }
        } else {
            showToast(data.error || '修复失败', 'error');
            addLog(`故障修复失败: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`修复失败: ${error.message}`, 'error');
        addLog(`故障修复失败: ${error.message}`, 'error');
    } finally {
        btn.disabled = false;
    }
}

// 快捷操作 - 沙箱模式
async function toggleSandbox() {
    const btn = document.getElementById('btn-sandbox');
    btn.disabled = true;
    
    try {
        addLog('正在切换沙箱模式...', 'info');
        const response = await fetch(`${API_BASE}/api/gateway/sandbox`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            showToast('沙箱模式切换成功', 'success');
            addLog('沙箱模式已切换', 'info');
        } else {
            showToast(data.error || '切换失败', 'error');
            addLog(`沙箱模式切换失败: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`切换失败: ${error.message}`, 'error');
        addLog(`沙箱模式切换失败: ${error.message}`, 'error');
    } finally {
        btn.disabled = false;
    }
}

// 快捷操作 - 停止服务
async function stopService() {
    if (!confirm('确定要停止 OpenClaw 服务吗？')) {
        return;
    }
    
    const btn = document.getElementById('btn-stop');
    btn.disabled = true;
    
    try {
        addLog('正在停止服务...', 'info');
        const response = await fetch(`${API_BASE}/api/gateway/stop`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            showToast('服务已停止', 'success');
            addLog('网关服务已停止', 'info');
        } else {
            showToast(data.error || '停止失败', 'error');
            addLog(`停止服务失败: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`停止失败: ${error.message}`, 'error');
        addLog(`停止服务失败: ${error.message}`, 'error');
    } finally {
        btn.disabled = false;
    }
}

// 添加日志
function addLog(message, type = 'info') {
    const logContent = document.getElementById('log-content');
    const now = new Date();
    const time = now.toTimeString().split(' ')[0];
    
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.innerHTML = `
        <span class="log-time">[${time}]</span>
        <span class="log-${type}">${message}</span>
    `;
    
    logContent.appendChild(entry);
    logContent.scrollTop = logContent.scrollHeight;
    
    // 限制日志数量
    while (logContent.children.length > 100) {
        logContent.removeChild(logContent.firstChild);
    }
}

// 显示 Toast
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
