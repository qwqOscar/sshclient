<template>
    <!-- <div class="content"> -->
    <div id="terminal" ref="xterm"></div>
    <!-- </div> -->
</template>

<script setup>
import { Terminal } from 'xterm'
import 'xterm/css/xterm.css'
import 'xterm/lib/xterm.js'
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
            user: 'root',
            term: '',
            rows: 40,
            cols: 100,
            input: '',
            length: 0,
            idx: 0,
            history: []
        }
    },
    props: ['msg'],
    methods: {
        createXTerm() {
            let xterm = new Terminal({
                rendererType: "canvas",
                convertEol: true,
                cursorBlink: true,
                rows: this.rows,
                cols: this.cols,
                disableStdin: false
            });
            return xterm;
        },

        initXTerm(xterm) {
            this.history = []
            this.idx = 0
            const prefix = `${this.user} $ `
            const fitAddon = new FitAddon()
            xterm.open(this.$refs['xterm'])
            xterm.loadAddon(fitAddon)
            let hello = `\x1B[1;3;32mWelcome to Terminal-${this.msg}.\x1B[0m`
            xterm.writeln(hello)
            xterm.prompt = () => {
                xterm.write(prefix)
                this.input = ''
                this.length = 0
            }
            xterm.prompt()
            fitAddon.fit()

            xterm.onKey((e) => {
                const { key, domEvent } = e
                const { keyCode, altKey, altGraphKey, ctrlKey, metaKey } = domEvent
                const printAble = !(altKey || altGraphKey || ctrlKey || metaKey)
                console.log(xterm._core.buffer)
                const currentY = xterm._core.buffer.y
                const currentX = xterm._core.buffer.x;
                console.log(currentX, currentY)
                if (domEvent.code == 'Enter') {
                    xterm.writeln('')
                    if (this.input.length) {
                        this.history.push(this.input)
                        this.idx = this.history.length
                    }
                    xterm.prompt()
                    console.log(this.history)
                } else if (domEvent.code == 'Backspace' && currentX > prefix.length) {
                    const start = currentX - prefix.length
                    xterm.write('\x1b[0D\x1b[0K')
                    xterm.write(xterm.buffer.active.getLine(currentX))
                    xterm.write(this.input.slice(start))
                    // xterm._core.buffer.x = currentX - 1;
                    xterm.write(`\x1b[${currentY + 1};${currentX}H`)
                    console.log(xterm._core.buffer.x)
                    this.input = this.input.slice(0, start - 1) + this.input.slice(start)
                } else if (domEvent.code == 'ArrowUp') {
                    if (this.idx) {
                        this.idx--;
                        xterm.write(`\x1b[${currentY + 1};${prefix.length + 1}H\x1b[0K\x1b[${currentY + 1};${prefix.length + 1}H`)
                        xterm.write(this.history[this.idx])
                    }
                } else if (domEvent.code == 'ArrowDown') {
                    if (this.idx < this.history.length) {
                        this.idx++;
                        xterm.write(`\x1b[${currentY + 1};${prefix.length + 1}H\x1b[0K\x1b[${currentY + 1};${prefix.length + 1}H`)
                        xterm.write(this.history[this.idx])
                    }
                } else if (domEvent.code == 'ArrowLeft' || domEvent == 'ArrowRight') {
                    xterm.write(e.key)
                } else {
                    this.input += e.key;
                    this.length++;
                    xterm.write(e.key)
                }
            })
            // xterm.onData((k) => {
            //     console.log(k.code)
            //     if (k == 127) {
            //         console.log(333)
            //     } else if (k == 13) {
            //         console.log(222)
            //     }
            //     xterm.write(k)
            // })

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