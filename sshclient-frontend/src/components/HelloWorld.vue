<template>
  
    <button type="button" @click="count++">count is {{ count }}</button>
    <el-button @click="pingpong">
      点击
    </el-button>
    
</template>

<script lang="ts">
import { Dictionary } from 'lodash'
import { ref } from 'vue'
export default {
  data () {
    return {
      buttontext : 'ping',
      count : 0,    
    }
  },
  methods : {
    pingpong () {
      // console.log('wwxnb')
      // console.log(this.$socket)
      this.$socket.send('111')
    },
  },
  created () {
    this.$options.sockets.onmessage = (res : any) =>{
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
