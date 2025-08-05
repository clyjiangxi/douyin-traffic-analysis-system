<template>
  <div class="recommend-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span><el-icon><MagicStick /></el-icon> 账号推荐</span>
        </div>
      </template>

      <el-form :model="form" inline class="recommend-form">
        <el-form-item label="产品类型">
          <el-select v-model="form.product_type" placeholder="请选择产品类型">
            <el-option label="不限" value="" />
            <el-option label="美妆" value="美妆" />
            <el-option label="数码" value="数码" />
            <el-option label="服饰" value="服饰" />
            <el-option label="美食" value="美食" />
            <el-option label="母婴" value="母婴" />
          </el-select>
        </el-form-item>
        <el-form-item label="最低粉丝数">
          <el-input-number v-model="form.min_fans" :min="0" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" :loading="loading" :icon="Search">推荐账号</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="accounts" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="nickname" label="昵称" />
        <el-table-column prop="douyin_id" label="抖音号" />
        <el-table-column prop="fans_count" label="粉丝数" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column prop="reason" label="推荐理由" />
      </el-table>
      <el-empty v-if="!accounts.length" description="暂无推荐结果，请填写需求后点击推荐" />
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { recommendAccounts } from '../api'
import { MagicStick, Search } from '@element-plus/icons-vue'

const form = ref({ product_type: '', min_fans: 0 })
const accounts = ref([])
const loading = ref(false)

const onSubmit = async () => {
  loading.value = true
  try {
    const res = await recommendAccounts(form.value)
    accounts.value = res.data
    if (!res.data.length) ElMessage.info('暂无符合条件的账号')
  } catch (e) {
    ElMessage.error('推荐失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.recommend-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recommend-form {
  margin-bottom: 20px;
}
</style>