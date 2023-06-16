<template>
    <div class="documentation">
      <h1>使用说明</h1>
  
      <h2>步骤 1</h2>
      <el-card>
        <h3>安装</h3>
        <p>使用以下命令安装依赖：</p>
        <pre><code>npm install element-plus</code></pre>
      </el-card>
  
      <h2>步骤 2</h2>
      <el-card>
        <h3>导入</h3>
        <p>在你的项目中导入 Element Plus：</p>
        <pre><code>import ElementPlus from 'element-plus';
  import 'element-plus/lib/theme-chalk/index.css';
  
  createApp(App).use(ElementPlus).mount('#app');</code></pre>
      </el-card>
  
      <h2>步骤 3</h2>
      <el-card>
        <h3>使用组件</h3>
        <p>在需要使用的组件中添加 Element Plus 的组件标签：</p>
        <pre><code>&lt;template>
    &lt;div>
      &lt;el-button type="primary">主要按钮&lt;/el-button>
      &lt;el-input v-model="inputValue" placeholder="请输入内容">&lt;/el-input>
    &lt;/div>
  &lt;/template></code></pre>
      </el-card>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Documentation',
    data() {
      return {
        inputValue: '',
      };
    },
  };
  </script>
  
  <style scoped>
  .documentation {
    padding: 20px;
  }
  
  h1 {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  h2 {
    font-size: 20px;
    margin-top: 20px;
    margin-bottom: 10px;
  }
  
  h3 {
    font-size: 16px;
    margin-bottom: 10px;
  }
  
  pre {
    background-color: #f5f7fa;
    padding: 10px;
    margin: 10px 0;
    border-radius: 4px;
    overflow-x: auto;
  }
  
  code {
    font-size: 14px;
  }
  </style>
  