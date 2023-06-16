import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/theme-chalk/index.css';
import './style.css';
import App from './App.vue';
import zhCn from 'element-plus/es/locale/lang/zh-cn';
import VueNativeSock from "vue-native-websocket-vue3";
import store from './utils/store';
const app = createApp(App);
// 使用VueNativeSock插件，并进行相关配置
app.use(ElementPlus, {locale : zhCn});
app.use(VueNativeSock, "ws://127.0.0.1:7070", {
  store : store,
  format : 'json',
  // 开启手动调用 connect() 连接服务器
  connectManually: false,
  // 关闭自动重连
  reconnection: true,
}
);
console.log('main.ts')
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app').$nextTick(() => postMessage({ payload: 'removeLoading' }, '*'));
export default app;