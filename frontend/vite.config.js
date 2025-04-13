import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
<<<<<<< Updated upstream
    plugins: [vue()],
    server: {
        proxy: {
            // 将所有API请求代理到Flask后端
            '/api': {
                target: 'http://localhost:5000',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        }
    }
=======
  plugins: [vue()]
>>>>>>> Stashed changes
})
