import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    server: {
        proxy: {
            // 将所有API请求代理到Flask后端
            '/api': {
                target: 'http://localhost:5000',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '')
            },
            // 添加对静态资源的代理
            '/problem/static': {
                target: 'http://localhost:5000',
                changeOrigin: true
            }
        }
    }
})
