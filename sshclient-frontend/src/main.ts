import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/index.css'
import './style.css'
import App from './App.vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

createApp(App).use(ElementPlus, {locale : zhCn}).mount('#app').$nextTick(() => postMessage({ payload: 'removeLoading' }, '*'))
