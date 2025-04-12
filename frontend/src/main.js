import { createApp } from 'vue'
import App from './App.vue'
// 导入路由配置
import router from './router'

// 创建应用并使用路由
const app = createApp(App)
app.use(router) // 使用路由
app.mount('#app') // 挂载应用

