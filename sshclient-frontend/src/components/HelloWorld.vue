<template>
  <h1>{{ msg }}</h1>

  <div class="card">
    <button type="button" @click="count++">count is {{ count }}</button>
    <el-button @click="initssh">
      点击初始化ssh
    </el-button>
    <el-button @click="sshcmd">
      点击发送命令
    </el-button>
    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>
  <p>
    Check out
    <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
      >create-vue</a
    >, the official Vue + Vite starter
  </p>
  <p>
    Install
    <a href="https://github.com/vuejs/language-tools" target="_blank">Volar</a>
    in your IDE for a better DX
  </p>
  <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
</template>

<script lang="ts">
import { ref } from 'vue'
export default {
  props : {
    msg : String
  },
  data () {
    return {
      buttontext : 'ping',
      count : 0,    
    }
  },
  methods : {
    initssh () {
      // console.log('wwxnb')
      // console.log(this.$socket)
      this.$socket.sendObj({type : 'initssh', data : {
        host : '139.196.203.149' ,
        port : 22,
        username : 'root',
        password : '',
      }, })
    },
    sshcmd () {
      // console.log('wwxnb')
      // console.log(this.$socket)
      this.$socket.sendObj({type : 'sshcmd', data : {
        host : '139.196.203.149' ,
        port : 22,
        username : 'root',
        cmd : 'ls -l'
      }, })
    },
  },
  created () {
    this.$options.sockets.onmessage = (res : any) =>{
      console.log(res.type)
      console.log(res.data)
    }
  },
  unmounted() {
    this.$socket.close()
  },
}

const count = ref(0)
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
