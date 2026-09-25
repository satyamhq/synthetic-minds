import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

const renderHost = process.env.RENDER_EXTERNAL_HOSTNAME

const allowedHosts = [
  'synthetic-minds.onrender.com',
  '.onrender.com',
  'localhost',
  '127.0.0.1'
]

if (renderHost && !allowedHosts.includes(renderHost)) {
  allowedHosts.push(renderHost)
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@locales': path.resolve(__dirname, '../locales')
    }
  },
  server: {
    port: parseInt(process.env.PORT || '3000', 10),
    open: false,
    allowedHosts,
    proxy: {
      '/api': {
        target: process.env.BACKEND_URL || 'http://localhost:5001',
        changeOrigin: true,
        secure: false
      }
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-vue': ['vue', 'vue-router', 'vue-i18n'],
          'vendor-d3': ['d3'],
          'vendor-axios': ['axios']
        }
      }
    },
    chunkSizeWarningLimit: 600
  }
})
