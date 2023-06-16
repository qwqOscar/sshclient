<template>
    <el-tabs v-model="editableTabsValue" type="card" editable class="tabs" @edit="handleTabsEdit">
        <el-tab-pane v-for="item in editableTabs" :key="item.name" :label="item.title" :name="item.name"
        class="pane"
        >
            <Content :msg="item.name"></Content>
            <!-- {{ item.content }} -->
            <!-- <Terminal :name="item.name"></Terminal> -->
        </el-tab-pane>
    </el-tabs>
</template>
<script lang="ts" setup>
import Content from './content.vue'
import { ref } from 'vue'
import type { TabPaneName } from 'element-plus'



let tabIndex = 2

const editableTabsValue = ref('1')
const editableTabs = ref([
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
])



const handleTabsEdit = (
    targetName: TabPaneName | undefined,
    action: 'remove' | 'add'
) => {
    if (action === 'add') {
        const newTabName = `${++tabIndex}`
        editableTabs.value.push({
            title: 'New Tab',
            name: newTabName,
            content: 'New Tab content',
        })
        editableTabsValue.value = newTabName
    } else if (action === 'remove') {
        const tabs = editableTabs.value
        let activeName = editableTabsValue.value
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

        editableTabsValue.value = activeName
        editableTabs.value = tabs.filter((tab) => tab.name !== targetName)
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
  