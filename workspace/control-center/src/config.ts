// OpenClaw Control Center Configuration

export const config = {
  // API Configuration
  api: {
    // OpenClaw Gateway URL
    // Change this to your actual OpenClaw gateway URL
    baseURL: import.meta.env.VITE_OPENCLAW_API_URL || 'http://localhost:8080/api',
    
    // WebSocket URL for real-time updates
    wsURL: import.meta.env.VITE_OPENCLAW_WS_URL || 'ws://localhost:8080/ws',
    
    // Request timeout in milliseconds
    timeout: 10000,
    
    // Auto-refresh intervals (in milliseconds)
    refreshIntervals: {
      agents: 30000,      // 30 seconds
      tasks: 30000,       // 30 seconds
      stats: 30000,       // 30 seconds
      usage: 60000,       // 1 minute
      gateway: 10000,     // 10 seconds
    }
  },

  // UI Configuration
  ui: {
    // Default theme
    theme: 'dark' as const,
    
    // Sidebar collapsed by default on mobile
    sidebarCollapsed: false,
    
    // Items per page for lists
    pageSize: 20,
  },

  // Feature Flags
  features: {
    // Enable real-time WebSocket updates
    realtime: false,
    
    // Enable task management
    tasks: true,
    
    // Enable memory browser
    memory: true,
    
    // Enable document management
    documents: true,
    
    // Enable usage analytics
    analytics: true,
  }
}

// Helper to check if running in development
export const isDev = import.meta.env.DEV

// Helper to get API URL
export const getApiUrl = () => config.api.baseURL

// Helper to get WebSocket URL
export const getWsUrl = () => config.api.wsURL
