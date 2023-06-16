<template>
	<el-row>

	</el-row>
	<el-row justify="center">
    <el-form
      label-position="right"
      label-width="120px"
      :model="formLabelAlign"
			size="large"
			disable
    >
      <el-form-item label="Connect Name">
        <el-input v-model="formLabelAlign.name" />
      </el-form-item>
      <el-form-item label="Server IP">
        <el-input v-model="formLabelAlign.ip" />
      </el-form-item>
      <el-form-item label="Username">
        <el-input v-model="formLabelAlign.username" />
      </el-form-item>
      <el-form-item label="Password">
        <el-input v-model="formLabelAlign.pwd" />
      </el-form-item>
    </el-form>
	</el-row>
	<el-row justify="space-evenly" align="middle">
		<el-col span="4">
			<el-button type="primary" @click="addupdate">
				{{ ind != 0 ? '保存修改' : '添加配置' }} 
			</el-button>
		</el-col>
		
		<el-col span="4">
			<el-button type="primary" @click="dialogVisible = true" v-if="ind != 0">
				删除
			</el-button>
		</el-col>
	</el-row>
    <el-dialog
    v-model="dialogVisible"
    title="Warning"
    width="50%"
    :before-close="handleClose"
  >
    <span>Are you sure to delete the Configuration?</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="del">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>
  
<script lang="ts" setup>
import { reactive, ref } from 'vue'  
import { ElMessageBox } from 'element-plus'
import { onMounted } from 'vue';
const handleClose = (done: () => void) => {
	ElMessageBox.confirm('Are you sure to close this dialog?')
		.then(() => {
			done()
		})
		.catch((e : string) => {
			// catch error
			console.log(e)
		})
}
</script>
<script lang="ts">
import { ElMessage } from 'element-plus';
export default{
	props : [
		"ind"
	],
	data(){
		return {
			formLabelAlign : {
				id : '',
				name: '',
				ip: '',
				username: '',
				pwd : '',
			},
			dialogVisible : false,
		}
	},
	methods : {
		addupdate(){
			if(this.$props.ind === this.formLabelAlign.id)
			{
				console.log('wwxnb')
				console.log(this.$props.ind)
				console.log('wwxnb')
				this.$socket.sendObj({
					type : 'updateconfig',
					data : {
						'id' : this.formLabelAlign.id,
						'name' : this.formLabelAlign.name,
						'ip' : this.formLabelAlign.ip,
						'username' : this.formLabelAlign.username,
						'pwd' : this.formLabelAlign.pwd,
					}
				})
			}
			else
			{
				this.$socket.sendObj({
					type : 'createconfig',
					data : {
						'name' : this.formLabelAlign.name,
						'ip' : this.formLabelAlign.ip,
						'username' : this.formLabelAlign.username,
						'pwd' : this.formLabelAlign.pwd,
					}
				})
			}
		},
		del(){
			console.log(this.$props.ind)
			if(this.$props.ind != 0)
			{
				this.dialogVisible = false
				this.$socket.sendObj({
					type : 'deleteconfig',
					data : {
						'id' : this.formLabelAlign.id,
						'name' : this.formLabelAlign.name,
						'ip' : this.formLabelAlign.ip,
						'username' : this.formLabelAlign.username,
						'pwd' : this.formLabelAlign.pwd,
					}
				})
			}
		}
	},
	beforeUnmount() {
		this.$options.sockets.onmessage = (res : any) =>{
			// console.log('frynb')
		}		
	}, 
	mounted () {
		console.log(this.$props.ind)
		if(this.$socket.readyState === 1 && this.$props.ind != 0)
		{
			this.$socket.sendObj({
				type : 'getconfig',
				data : ''
			})
		}
		this.$options.sockets.onmessage = (res : any) =>{
			var data = JSON.parse(res.data)
			if(data.type === 'config' && this.$props.ind != 0)
			{
				data = JSON.parse(data.data)
				var arr = Object.keys(data)
				console.log(this.formLabelAlign)
				this.formLabelAlign.id = arr[this.$props.ind - 1]
				this.formLabelAlign.name = data[arr[this.$props.ind - 1]]['name']
				this.formLabelAlign.ip = data[arr[this.$props.ind - 1]]['ip']
				this.formLabelAlign.username = data[arr[this.$props.ind - 1]]['username']
				this.formLabelAlign.pwd = data[arr[this.$props.ind - 1]]['password']
			}
			else if(data.type === 'updateconfig')
			{
				console.log(data)
				if(data.data.msg == 'Success!' && this.$props.ind === data.data.id)
				{
					ElMessage({
					message: 'Update Successfully!',
					type: 'success',
					duration : 1000,
					})
				}
				location.reload()
			}
			else if(data.type === 'deleteconfig')
			{
				if(data.data.msg == 'Success!' && this.$props.ind === data.data.id)
				{
					ElMessage({
					message: 'Delete Successfully!',
					type: 'success',
					duration : 1000,
					})
				}
				location.reload()
			}
			else if(data.type === 'createconfig')
			{
				if(data.data.msg == 'Success!' && this.$props.ind === data.data.id)
				{
					ElMessage({
					message: 'Create Successfully! Please Flash to View.',
					type: 'success',
					duration : 1000,
					})
				}
				location.reload()
			}
    	}
	},
}
</script>
<style scoped>

</style>