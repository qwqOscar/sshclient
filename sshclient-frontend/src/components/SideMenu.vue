<template>
	<el-container>
		<el-aside>
			<el-menu active-text-color="#ffd04b" background-color="#545c64" class="el-menu-vertical-demo" default-active="1"
				text-color="#fff" @open="handleOpen" @close="handleClose" @select="changeind">
				<el-menu-item index="1">
					<el-icon>
						<House />
					</el-icon>
					<span>Homepage</span>
				</el-menu-item>
				<el-menu-item index="2">
					<el-icon>
						<Link />
					</el-icon>
					<span>Ssh Terminal</span>
				</el-menu-item>
				<el-menu-item index="3">
					<el-icon>
						<Document />
					</el-icon>
					<span>Sftp Transfer</span>
				</el-menu-item>
				<el-sub-menu index="4" open="@">
					<template #title>
						<el-icon>
							<setting />
						</el-icon>
						<span>Config</span>
					</template>
					<el-menu-item index="4">
						<el-icon>
							<setting />
						</el-icon>
						<span>New Configure</span>
					</el-menu-item>
					<el-menu-item v-for="item in menuItems" :key="item.index" :index="item.index">
						<span>{{ item.text }}</span>
					</el-menu-item>
				</el-sub-menu>
				<!-- <el-menu-item index="4">
				</el-menu-item> -->
			</el-menu>
		</el-aside>
		<el-container>
			<el-main>
				<div>
					<div v-if="currentIndex === '1'">
						<Usage></Usage>
					</div>
					<div v-else-if="currentIndex === '2'">
						<Tab />
					</div>
					<div v-else-if="currentIndex === '3'">
						<Sftp />
					</div>
					<div v-else-if="currentIndex === '4'">
						<Config ind="0"></Config>
					</div>
					<div v-else-if="currentIndex === '4-1'">
						<Config ind="1"></Config>
					</div>
					<div v-else-if="currentIndex === '4-2'">
						<Config ind="2"></Config>
					</div>
					<div v-else-if="currentIndex === '4-3'">
						<Config ind="3"></Config>
					</div>
					<div v-else-if="currentIndex === '4-4'">
						<Config ind="4"></Config>
					</div>
					<div v-else-if="currentIndex === '4-5'">
						<Config ind="5"></Config>
					</div>
				</div>
			</el-main>
		</el-container>

	</el-container>
</template>
  
<script lang="ts" setup>
import {
	Document,
	Menu as IconMenu,
	Location,
	Setting,
} from '@element-plus/icons-vue'
const handleClose = (key: string, keyPath: string[]) => {
	console.log(key, keyPath)
}
</script>
<script lang="ts">
import Tab from './titleBar.vue'
import Config from './Config.vue'
import Usage from './Usage.vue'
import Sftp from './Sftp.vue'
export default {
	components: {
		Tab,
		Config,
	},
	data() {
		return {
			currentIndex: '1',
			menuItems: [
				{
					index: '5',
					text: '',
				}
			],
		}
	},
	methods: {
		changeind(index: string) {
			this.currentIndex = index
			console.log(this.currentIndex)
		},
		handleOpen() {
			if (this.$socket.readyState === 1) {
				this.$socket.sendObj({
					type: 'getconfig',
					data: ''
				})
			}
		}
	},
	mounted() {
		this.$options.sockets.onmessage = (res: any) => {
			var data = JSON.parse(res.data)
			if (data.type === 'config') {
				data = JSON.parse(data.data)
				var arr = Object.keys(data)
				this.menuItems.length = arr.length
				for (var i = 0; i < arr.length; i++) {
					this.menuItems[i] = {
						index: '4-' + (i + 1).toString(),
						text: data[arr[i]]['name'] + ' ' + data[arr[i]]['username'] + '@' + data[arr[i]]['ip'],
					}
				}
			}
		}
	}
}
</script>
<style>
.el-container {
	height: 100%;
}

.el-menu {
	height: 100%;
	width: 100%
}
</style>