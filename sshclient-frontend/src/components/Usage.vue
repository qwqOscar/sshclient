<template>
  <div class="documentation">
    <h1>信息安全原理课程课程设计</h1>
    <h2>2053925 万唯循 1953246 方若愚</h2>
    <h2>问题重述</h2>
    <el-card>
      <h3>考虑若干智能手机为用户终端，数据存储和web服务部署在一个linux服务器上，服务器与终端间应用层至少采用TLS保护，设计一个基于ssh对该服务器的远程配置和管理的原型系统。</h3>
    </el-card>

    <h2>工作总述</h2>
    <el-card>
      <h3>
        在上述问题的背景下，我们开发了一款桌面应用，前端使用了vite+vue3+electron的框架，中间件使用了python的paramiko库，paramiko库支持基于ssh的和sftp的远程连接，并且可以模拟终端命令行的交互，同时我们使用websocket作为前端和中间件的连接，值得一提的是两者的websocket连接的url为localhost，在本地运行
      </h3>
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
  