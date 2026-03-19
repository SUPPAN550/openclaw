#!/usr/bin/env python3
"""
OpenClaw Hub Test Agent
功能测试智能体 - 验证所有功能是否正常运行
"""

import requests
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Tuple

# 配置
BACKEND_URL = "http://localhost:5000"
GATEWAY_URL = "http://127.0.0.1:18789"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests: List[Tuple[str, bool, str]] = []
    
    def add(self, name: str, success: bool, message: str = ""):
        self.tests.append((name, success, message))
        if success:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print("\n" + "="*60)
        print("📊 测试报告")
        print("="*60)
        
        for name, success, message in self.tests:
            status = f"{Colors.GREEN}✓{Colors.END}" if success else f"{Colors.RED}✗{Colors.END}"
            print(f"{status} {name}")
            if message and not success:
                print(f"   {Colors.RED}  → {message}{Colors.END}")
        
        print("\n" + "-"*60)
        total = self.passed + self.failed
        print(f"总计: {total} | {Colors.GREEN}通过: {self.passed}{Colors.END} | {Colors.RED}失败: {self.failed}{Colors.END}")
        
        if self.failed == 0:
            print(f"\n{Colors.GREEN}🎉 所有测试通过！{Colors.END}")
        else:
            print(f"\n{Colors.RED}⚠️ 有 {self.failed} 个测试失败{Colors.END}")
        print("="*60)

class OpenClawHubTester:
    def __init__(self):
        self.results = TestResult()
        self.session = requests.Session()
    
    def test_backend_connection(self):
        """测试后端服务连接"""
        print(f"\n{Colors.BLUE}🔌 测试后端连接...{Colors.END}")
        try:
            response = self.session.get(f"{BACKEND_URL}/api/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.results.add("后端连接", True)
                    return True
                else:
                    self.results.add("后端连接", False, f"网关未连接: {data.get('error', '未知错误')}")
                    return False
            else:
                self.results.add("后端连接", False, f"HTTP {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.results.add("后端连接", False, "无法连接到后端服务，请确保服务已启动")
            return False
        except Exception as e:
            self.results.add("后端连接", False, str(e))
            return False
    
    def test_agents_api(self):
        """测试 Agent API"""
        print(f"\n{Colors.BLUE}👥 测试 Agent API...{Colors.END}")
        
        # 获取 Agent 列表
        try:
            response = self.session.get(f"{BACKEND_URL}/api/agents", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and len(data.get('data', [])) == 6:
                    self.results.add("获取 Agent 列表", True)
                else:
                    self.results.add("获取 Agent 列表", False, f"Agent 数量不正确: {len(data.get('data', []))}")
            else:
                self.results.add("获取 Agent 列表", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.results.add("获取 Agent 列表", False, str(e))
        
        # 测试启动 Agent
        try:
            response = self.session.post(f"{BACKEND_URL}/api/agents/may/start", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.results.add("启动 Agent", True)
                else:
                    self.results.add("启动 Agent", False, data.get('error', '未知错误'))
            else:
                self.results.add("启动 Agent", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.results.add("启动 Agent", False, str(e))
    
    def test_metrics_api(self):
        """测试系统资源 API"""
        print(f"\n{Colors.BLUE}📊 测试系统资源 API...{Colors.END}")
        
        try:
            response = self.session.get(f"{BACKEND_URL}/api/metrics", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    metrics = data.get('data', {})
                    checks = [
                        ('cpu' in metrics, "CPU 数据"),
                        ('memory' in metrics, "内存数据"),
                        ('storage' in metrics, "存储数据"),
                        (0 <= metrics.get('cpu', -1) <= 100, "CPU 范围有效"),
                        (0 <= metrics.get('memory', -1) <= 100, "内存范围有效"),
                    ]
                    
                    all_valid = all(check[0] for check in checks)
                    if all_valid:
                        self.results.add("系统资源监控", True)
                        print(f"   CPU: {metrics.get('cpu')}%")
                        print(f"   Memory: {metrics.get('memory')}%")
                        print(f"   Storage: {metrics.get('storage')}%")
                    else:
                        failed = [c[1] for c in checks if not c[0]]
                        self.results.add("系统资源监控", False, f"数据无效: {', '.join(failed)}")
                else:
                    self.results.add("系统资源监控", False, data.get('error', '未知错误'))
            else:
                self.results.add("系统资源监控", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.results.add("系统资源监控", False, str(e))
    
    def test_gateway_operations(self):
        """测试网关操作"""
        print(f"\n{Colors.BLUE}⚙️ 测试网关操作...{Colors.END}")
        
        # 版本检查
        try:
            response = self.session.get(f"{BACKEND_URL}/api/gateway/version", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.results.add("版本检查", True)
                    print(f"   版本: {data.get('version', '未知')}")
                else:
                    self.results.add("版本检查", False, data.get('error', '未知错误'))
            else:
                self.results.add("版本检查", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.results.add("版本检查", False, str(e))
        
        # 注意：重启和停止服务会实际影响网关，这里只测试 API 响应
        # 实际生产环境应谨慎使用
    
    def test_frontend(self):
        """测试前端页面"""
        print(f"\n{Colors.BLUE}🌐 测试前端页面...{Colors.END}")
        
        try:
            response = self.session.get(BACKEND_URL, timeout=5)
            if response.status_code == 200:
                content = response.text
                checks = [
                    ('OpenClaw Hub' in content, "页面标题"),
                    ('agent-grid' in content, "Agent 网格"),
                    ('cpu-bar' in content, "CPU 进度条"),
                    ('memory-bar' in content, "内存进度条"),
                    ('storage-bar' in content, "存储进度条"),
                    ('log-content' in content, "日志区域"),
                    ('config-modal' in content, "配置模态框"),
                ]
                
                all_present = all(check[0] for check in checks)
                if all_present:
                    self.results.add("前端页面", True)
                else:
                    missing = [c[1] for c in checks if not c[0]]
                    self.results.add("前端页面", False, f"缺少元素: {', '.join(missing)}")
            else:
                self.results.add("前端页面", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.results.add("前端页面", False, str(e))
    
    def run_all_tests(self):
        """运行所有测试"""
        print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BLUE}🧪 OpenClaw Hub 功能测试{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"后端地址: {BACKEND_URL}")
        print(f"网关地址: {GATEWAY_URL}")
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 先测试后端连接
        if not self.test_backend_connection():
            print(f"\n{Colors.RED}❌ 后端服务未启动，无法继续测试{Colors.END}")
            print(f"{Colors.YELLOW}请运行: cd backend && python app.py{Colors.END}")
            self.results.print_summary()
            return
        
        # 运行其他测试
        self.test_agents_api()
        self.test_metrics_api()
        self.test_gateway_operations()
        self.test_frontend()
        
        # 打印报告
        self.results.print_summary()

def main():
    print("OpenClaw Hub Test Agent")
    print("功能测试智能体\n")
    
    tester = OpenClawHubTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
