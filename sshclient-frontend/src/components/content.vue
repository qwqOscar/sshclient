<template>
    <div class="content">
        <div id="terminal" ref="xterm"></div>
    </div>
</template>

<script setup>
import { Terminal } from 'xterm'
import 'xterm/css/xterm.css'
import { FitAddon } from 'xterm-addon-fit'
// onMounted(() => {
//     const xterm = createXTerm()
//     initXTerm(xterm)
// })

</script>

<script>
export default {
    data() {
        return {
            term: '',
            rows: 40,
        }
    },
    props: ['msg'],
    methods: {
        createXTerm() {
            let xterm = new Terminal();
            return xterm;
        },

        initXTerm(xterm) {
            xterm.open(this.$refs['xterm'])
            let hello = `Hello from \x1B[1;3;31m${this.msg}\x1B[0m\r\n $ `
            console.log(hello)
            xterm.write(hello)
            const fitAddon = new FitAddon()
            xterm.loadAddon(fitAddon)
            fitAddon.fit()
        }
    },
    mounted() {
        let term = this.createXTerm()
        this.initXTerm(term)

        this.term = term
    }
}
</script>

<style scoped>
.content {
    height: 100%;
    width: 100%;
}

.terminal {
    height: 100%;
}
</style>