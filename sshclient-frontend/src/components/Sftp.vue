<template>
    <el-steps :active="step" finish-status="success" simple>
        <el-step title="Direction" />
        <el-step title="Address" />
        <el-step title="Load" />
    </el-steps>
    <el-row justify="space-between" class="item" tabindex="1" @blur="blurInput($event)" @focus="focusInput($event)">
        <div style="align-items: center;">
            <el-text>Mode</el-text>
        </div>
        <el-switch v-model="mode" class="ml-2" style="--el-switch-off-color: #13ce66" active-text="Upload"
            inactive-text="Download" />
    </el-row>
    <div class="item" tabindex="2" style="filter: blur(1px)" @blur="blurInput($event)" @focus="focusInput($event)">
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
    <el-row class="item" tabindex="3" style="filter: blur(1px);" @blur="blurInput($event)" @focus="focusInput($event)">
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
        }
    },
    methods: {
        blurInput(e: FocusEvent) {
            // 失去焦点时添加模糊效果
            const dom = e.target as HTMLElement
            dom.style.filter = 'blur(1px)'
        },
        focusInput(e: FocusEvent) {
            // 获得焦点时移除模糊效果
            const lastDoms = document.querySelectorAll('[tabindex="1"]')
            console.log(lastDoms)
            lastDoms.forEach((elem) => {
                const lastDom = elem as HTMLElement
                lastDom.style.filter = 'blur(1px)'
            })
            this.step = (e.target as HTMLElement).tabIndex
            const doms = document.querySelectorAll(`[tabindex=${this.step}]`)
            doms.forEach((elem) => {
                const dom = elem as HTMLElement
                dom.style.filter = ''
            })
            // this.step = dom.tabIndex
        },
        passBlur(e: FocusEvent) {
            const dom = e.target as HTMLElement
            dom.parentElement?.blur()
        },
        passFocus(e: FocusEvent) {
            const dom = e.target as HTMLElement
            dom.parentElement?.focus()
        },
        sendData() {
            this.$socket.sendObj({
                type: 'sftp', data: {
                    remote: this.remote,
                    local: this.local,
                    mode: this.mode,
                },
            })
        }
    }
}
</script>
  
<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'

const ruleFormRef = ref<FormInstance>()

const checkAge = (rule: any, value: any, callback: any) => {
    if (!value) {
        return callback(new Error('Please input the age'))
    }
    setTimeout(() => {
        if (!Number.isInteger(value)) {
            callback(new Error('Please input digits'))
        } else {
            if (value < 18) {
                callback(new Error('Age must be greater than 18'))
            } else {
                callback()
            }
        }
    }, 1000)
}

const validatePass = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('Please input the password'))
    } else {
        if (ruleForm.checkPass !== '') {
            if (!ruleFormRef.value) return
            ruleFormRef.value.validateField('checkPass', () => null)
        }
        callback()
    }
}
const validatePass2 = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('Please input the password again'))
    } else if (value !== ruleForm.pass) {
        callback(new Error("Two inputs don't match!"))
    } else {
        callback()
    }
}

const form = reactive({
    remoteAddr: '',
    hostAddr: '',
    age: '',
})

const rules = reactive<FormRules>({
    pass: [{ validator: validatePass, trigger: 'blur' }],
    checkPass: [{ validator: validatePass2, trigger: 'blur' }],
    age: [{ validator: checkAge, trigger: 'blur' }],
})

const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate((valid) => {
        if (valid) {
            console.log('submit!')
        } else {
            console.log('error submit!')
            return false
        }
    })
}

const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}
</script>
<style scoped>
.item {
    background-color: #f5f7fa;
    margin-top: 4px;
}

.no-wrap {
    flex-wrap: nowrap;
}

.inputbox {
    width: 120px;
}
</style>
  