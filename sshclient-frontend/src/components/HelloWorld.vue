<template>
  
    <button type="button" @click="count++">count is {{ count }}</button>
    <el-button @click="initssh">
      点击初始化ssh
    </el-button>
    <el-button @click="sshcmd">
      点击发送命令
    </el-button>
    
</template>

<script lang="ts">
import { ref } from 'vue'
export default {
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
        password : 'E_2A6nV_-gnVPmf',
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
