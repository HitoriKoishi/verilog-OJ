import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 导入样式文件
import './styles/theme.css'
import './styles/layout.css'
import './styles/typography.css'
import './styles/buttons.css'
import './styles/forms.css'
import './styles/cards.css'
import './styles/animations.css'
import './styles/loading.css'

const app = createApp(App)
app.use(router)
app.mount('#app')

