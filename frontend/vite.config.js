import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
    // 加载环境变量
    const env = loadEnv(mode, process.cwd())

    return {
        plugins: [vue()],
        define: {
            'process.env': {},
            'process.browser': true,
            'global': 'globalThis',
            'window.state': '{}',
            'state': '{}',
        },
        server: {
            proxy: {
                '/api': {
                    target: env.VITE_API_BASE_URL,
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/api/, '')
                },
                '/problem/static': {
                    target: env.VITE_API_BASE_URL,
                    changeOrigin: true
                }
            }
        }
    }
})