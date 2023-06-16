<template>
    <el-tabs v-model="editableTabsValue" type="card" editable class="tabs" @edit="handleTabsEdit">
        <el-tab-pane v-for="item in editableTabs" :key="item.name" :label="item.title" :name="item.name" class="pane">
            <Content :host="conn.data.host" :port="conn.data.port" :username="conn.data.username"></Content>
            <!-- {{ item.content }} -->
            <!-- <Terminal :name="item.name"></Terminal> -->
        </el-tab-pane>
    </el-tabs>
</template>

<script lang="ts">
import Content from './content.vue'
import { ref } from 'vue'
import type { TabPaneName } from 'element-plus'
export default {
    data() {
        return {
            conn: {
                type: 'initssh', data: {
                    host: '121.43.235.227',
                    port: 22,
                    username: 'root',
                    password: '',
                },
            },
            editableTabs: [
                {
                    title: 'Tab 1',
                    name: '1',
                    content: 'Tab 1 content',
                },
                {
                    title: 'Tab 2',
                    name: '2',
                    content: 'Tab 2 content',
                },
            ],
            editableTabsValue: '1',
            tabIndex: 2,
        }
    },
    methods: {
        initssh(config) {
            console.log('initssh')
            // console.log(this.$socket)
            // if (this.$socket && this.$socket.connected) {
            this.$socket.sendObj(config)
            // } else {
            //     console.log('websocket not ready')
            //     return
            // }

        },
        handleTabsEdit(
            targetName: TabPaneName | undefined,
            action: 'remove' | 'add'
        ) {
            if (action === 'add') {
                this.editableTabs.push({
                    title: `${this.conn.data.username}@${this.conn.data.host}:${this.conn.data.port}`,
                    name: `${this.conn.data.username}@${this.conn.data.host}:${this.conn.data.port}`,
                    content: 'New Tab content',
                })
                this.initssh(this.conn)
                this.editableTabsValue = `${this.conn.data.username}@${this.conn.data.host}:${this.conn.data.port}`
            } else if (action === 'remove') {
                const tabs = this.editableTabs
                let activeName = this.editableTabsValue
                if (activeName === targetName) {
                    tabs.forEach((tab, index) => {
                        if (tab.name === targetName) {
                            const nextTab = tabs[index + 1] || tabs[index - 1]
                            if (nextTab) {
                                activeName = nextTab.name
                            }
                        }
                    })
                }

                this.editableTabsValue = activeName
                this.editableTabs = tabs.filter((tab) => tab.name !== targetName)
            }
        }
    },
    setup() {

    }
}
</script>
<style>
.tabs {
    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;
}

.tabs>.el-tabs__header {
    padding: 0;
    margin: 0;
    border: 0;
}

.tabs>.el-tabs__content {
    /* padding: 32px; */
    padding: 0;
    margin: 0;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
    height: 100%;
    width: 100%;
}

Terminal {
    width: 100%;
    height: 100%;
}

pane {
    height: 100%;
}
</style>
  