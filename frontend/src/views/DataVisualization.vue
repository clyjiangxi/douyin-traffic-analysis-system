<template>
  <div class="visualization-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span><el-icon><Histogram /></el-icon> 账号粉丝数分布</span>
              <el-button v-if="isAdmin" type="primary" :icon="Download" @click="exportFansChart">导出图片</el-button>
            </div>
          </template>
          <div ref="fansChart" style="width: 100%; height: 400px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span><el-icon><DataLine /></el-icon> 广告主预算分布</span>
              <el-button v-if="isAdmin" type="primary" :icon="Download" @click="exportBudgetChart">导出图片</el-button>
            </div>
          </template>
          <div ref="budgetChart" style="width: 100%; height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import * as echarts from 'echarts'
import { getAccounts, getAdvertiserRequests } from '../api'
import axios from 'axios'
import { Histogram, DataLine, Download } from '@element-plus/icons-vue'

const fansChart = ref(null)
const budgetChart = ref(null)
let fansChartInstance = null
let budgetChartInstance = null

const user = ref(null)
function fetchUser() {
  const token = localStorage.getItem('token')
  if (!token) {
    user.value = null
    return
  }
  axios.get('http://localhost:8002/me', { headers: { Authorization: `Bearer ${token}` } })
    .then(res => { user.value = res.data })
    .catch(() => { user.value = null })
}
onMounted(fetchUser)

const isAdmin = computed(() => user.value && user.value.role === 'admin')

const renderFansChart = (accounts) => {
  const fansData = accounts.map(a => ({ name: a.nickname, value: a.fans_count }))
  fansChartInstance = echarts.init(fansChart.value)
  fansChartInstance.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: fansData.map(d => d.name) },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: fansData.map(d => d.value), name: '粉丝数' }]
  })
}

const renderBudgetChart = (requests) => {
  const budgetData = requests.map(r => ({ name: r.advertiser, value: r.budget }))
  budgetChartInstance = echarts.init(budgetChart.value)
  budgetChartInstance.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: budgetData.map(d => d.name) },
    yAxis: { type: 'value' },
    series: [{ type: 'line', data: budgetData.map(d => d.value), name: '预算', smooth: true }]
  })
}

function exportFansChart() {
  if (fansChartInstance) {
    const url = fansChartInstance.getDataURL({ type: 'png', backgroundColor: '#fff' })
    const a = document.createElement('a')
    a.href = url
    a.download = 'fans_chart.png'
    a.click()
  }
}

function exportBudgetChart() {
  if (budgetChartInstance) {
    const url = budgetChartInstance.getDataURL({ type: 'png', backgroundColor: '#fff' })
    const a = document.createElement('a')
    a.href = url
    a.download = 'budget_chart.png'
    a.click()
  }
}

onMounted(async () => {
  const accRes = await getAccounts({ limit: 1000 })
  const reqRes = await getAdvertiserRequests({ limit: 1000 })
  renderFansChart(accRes.data.items)
  renderBudgetChart(reqRes.data.items)
})
</script>

<style scoped>
.visualization-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>