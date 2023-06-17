<template>
    <el-button class="add" size="small" @click="showopt">
      Add New Connect
    </el-button>

    <el-tabs v-model="editableTabsValue" type="card" closable class="tabs" @tab-remove="removeTab" >
        <el-tab-pane v-for="item in editableTabs" :key="item.name" :label="item.title" :name="item.name" class="pane">
            <Content :host="item.ip" port="22" :username="item.username"></Content>
            <!-- {{ item.content }} -->
            <!-- <Terminal :name="item.name"></Terminal> -->
        </el-tab-pane>
    </el-tabs>
    <el-dialog
    v-model="dialogVisible"
    title="Choose config"
    width="50%"
    height="50%"
  >
  <span>
    <el-select v-model="configval" placeholder="Select">
    <el-option
    v-for="item in options"
    :key="item.value"
    :label="item.label"
    :value="item.value"
    />
    </el-select>
  </span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button  @click="addTab">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts">
import Content from './content.vue'
export default {
    data() {
        return {
            editableTabs: [] as Record<string, string | number>[],
            editableTabsValue: '1',
            tabIndex: 2,
            dialogVisible : false,
            options: [] as Record<string, string>,
            configs: { } as Record<string, Record<string, string | number>>,
            configval: "" as string,
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
        removeTab(targetName: string) {
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
        },
        showopt() {
            if (this.$socket.readyState === 1) {
            this.$socket.sendObj({
                type: 'getconfig',
                data: ''
            })
            }
            this.dialogVisible = true
        },
        addTab() {
            console.log(this.configval)
            this.dialogVisible = false
            console.log(this.configs[this.configval])
            this.editableTabs.push({
                title: `${this.configs[this.configval]['username']}@${this.configs[this.configval]['ip']}:${22}`,
                name: `${this.configs[this.configval]['username']}@${this.configs[this.configval]['ip']}:${22}`,
                content: 'New Tab content',
                username : this.configs[this.configval]['username'],
                ip : this.configs[this.configval]['ip'],
            })
            this.initssh(
                {
                    type: 'initssh', data: {
                    host: this.configs[this.configval]['ip'],
                    port: 22,
                    username: this.configs[this.configval]['username'],
                    password: this.configs[this.configval]['password'],
                },  
                }
            )
            this.editableTabsValue = `${this.configs[this.configval]['username']}@${this.configs[this.configval]['ip']}:${22}`          
        },
    },
    setup() {

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
                for(var i = 0;i < arr.length;i++)
                {
                    this.options[i] = {
                        // label : data[arr[i]]['name'] + '——' + data[arr[i]]['username'] + '@' + data[arr[i]]['ip'],
                        label : data[arr[i]]['name'],
                        value : arr[i],
                    }
                }
			}
		}
    },
}
</script>
<style scoped>
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
.add{
    position: absolute;
    right: 5%;
    z-index: 100;
}
</style>
  