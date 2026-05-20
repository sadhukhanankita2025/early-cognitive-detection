import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5175,
    proxy: {
      '/predict': 'http://localhost:5000',
      '/download-report': 'http://localhost:5000',
      '/health': 'http://localhost:5000',
    },
  },
  build: {
    chunkSizeWarningLimit: 2000,
  },
})
