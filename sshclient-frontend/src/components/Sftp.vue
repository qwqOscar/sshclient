<template>
    <el-steps :active="step" finish-status="success" simple>
        <el-step title="Config" />
        <el-step title="Direction" />
        <el-step title="Address" />
    </el-steps>
    <el-row class="item" tabindex="1">
        <el-select v-model="configval" placeholder="Select">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
    </el-row>
    <el-row justify="space-between" class="item" tabindex="2" @blur="blurInput($event)" @focus="focusInput($event)">
        <div style="align-items: center;">
            <el-text>Mode</el-text>
        </div>
        <el-switch v-model="mode" class="ml-2" style="--el-switch-off-color: #13ce66" active-text="Upload"
            inactive-text="Download" />
    </el-row>
    <div class="item" tabindex="3" @blur="blurInput($event)" @focus="focusInput($event)">
        <el-row class="no-wrap" justify="space-between">
            <el-text>Local Address</el-text>
            <el-input v-model="local" placeholder="Local" class="inputbox" tabindex="2" @blur="blurInput($event)"
                @focus="focusInput($event)" />
        </el-row>
        <el-row class="no-wrap" justify="space-between">
            <el-text>Remote Address</el-text>
            <el-input v-model="remote" placeholder="Remote" class="inputbox" />
        </el-row>
    </div>
    <el-row class="item" tabindex="4" @blur="blurInput($event)" @focus="focusInput($event)">
        <el-button type="primary" @click="sendData">Load</el-button>
    </el-row>
</template>

<script lang="ts">

export default {
    data() {
        return {
            step: 1,
            mode: true,
            local: '',
            remote: '',
            options: [],
            configs: {},
            configval: ""
        }
    },
    methods: {
        blurInput(e: FocusEvent) {
            // 失去焦点时添加模糊效果
            // const dom = e.target as HTMLElement
            // dom.style.filter = 'blur(1px)'
        },
        focusInput(e: FocusEvent) {
            // 获得焦点时移除模糊效果
            // const lastDoms = document.querySelectorAll('[tabindex="1"]')
            // console.log(lastDoms)
            // lastDoms.forEach((elem) => {
            //     const lastDom = elem as HTMLElement
            //     lastDom.style.filter = 'blur(1px)'
            // })
            this.step = (e.target as HTMLElement).tabIndex
            // const doms = document.querySelectorAll(`[tabindex=${this.step}]`)
            // doms.forEach((elem) => {
            //     const dom = elem as HTMLElement
            //     dom.style.filter = ''
            // })
            // this.step = dom.tabIndex
        },
        // passBlur(e: FocusEvent) {
        //     const dom = e.target as HTMLElement
        //     dom.parentElement?.blur()
        // },
        // passFocus(e: FocusEvent) {
        //     const dom = e.target as HTMLElement
        //     dom.parentElement?.focus()
        // },
        sendData() {
            if (!this.configs[this.configval] || !this.local || !this.remote) {
                ElMessage({
                    message: 'Fill All the Fields!',
                    type: 'error',
                    duration: 1000,
                })
            }
            this.$socket.sendObj({
                type: 'sftp', data: {
                    ip: this.configs[this.configval]['ip'],
                    username: this.configs[this.configval]['username'],
                    password: this.configs[this.configval]['password'],
                    port: 22,
                    remote: this.remote,
                    local: this.local,
                    mode: this.mode,
                },
            })
        }
    },
    mounted() {
        if (this.$socket.readyState === 1) {
            this.$socket.sendObj({
                type: 'getconfig',
                data: ''
            })
        }
        this.$options.sockets.onmessage = (res: any) => {
            var data = JSON.parse(res.data)
            if (data.type === 'config') {
                data = JSON.parse(data.data)
                var arr = Object.keys(data)
                this.options.length = arr.length
                this.configs = data
                for (var i = 0; i < arr.length; i++) {
                    this.options[i] = {
                        // label : data[arr[i]]['name'] + '——' + data[arr[i]]['username'] + '@' + data[arr[i]]['ip'],
                        label: data[arr[i]]['name'],
                        value: arr[i],
                    }
                }
            }
            if (data.type === 'done') {
                const message = this.mode ? 'Upload' : 'Download'
                ElMessage({
                    message: message + ' Successfully!',
                    type: 'success',
                    duration: 1000,
                })
            }
        }
    }
}
</script>
  

<style scoped>
.item {
    background-color: #f5f7fa;
    margin-top: 4px;
}

/* .item:not([tabindex='1']) {
    filter: blur(1px)
} */

.no-wrap {
    flex-wrap: nowrap;
}

.inputbox {
    width: 120px;
}
</style>
  