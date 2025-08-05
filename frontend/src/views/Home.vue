<template>
  <div class="home-container">
    <div class="header">
      <h1 class="title">抖音广告分析平台</h1>
      <p class="subtitle">一站式达人账号分析与广告投放推荐工具</p>
    </div>

    <el-row :gutter="20" class="card-container">
      <el-col :span="8" v-for="card in cards" :key="card.title">
        <el-card class="box-card" shadow="hover" @click="$router.push(card.route)">
          <div class="card-content">
            <el-icon :size="40" class="card-icon"><component :is="card.icon" /></el-icon>
            <h3 class="card-title">{{ card.title }}</h3>
            <p class="card-description">{{ card.description }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div class="generate-data-container">
        <el-button type="warning" size="large" :loading="loading" @click="onGenerate" :icon="Refresh">一键生成测试数据</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { generateTestData } from '../api'
import { User, EditPen, PieChart, MagicStick, Refresh } from '@element-plus/icons-vue'

const loading = ref(false)
const onGenerate = async () => {
  loading.value = true
  try {
    await generateTestData()
    ElMessage.success('测试数据已生成！')
    setTimeout(() => window.location.reload(), 1000)
  } catch (e) {
    ElMessage.error('生成失败')
  } finally {
    loading.value = false
  }
}

const cards = [
  {
    title: '账号管理',
    description: '管理和查看所有抖音账号信息',
    icon: User,
    route: '/accounts'
  },
  {
    title: '广告主需求',
    description: '查看和管理广告主的需求列表',
    icon: EditPen,
    route: '/advertiser-requests'
  },
  {
    title: '数据可视化',
    description: '通过图表分析账号和广告数据',
    icon: PieChart,
    route: '/visualization'
  },
  {
    title: '账号推荐',
    description: '根据需求智能推荐相关账号',
    icon: MagicStick,
    route: '/recommend'
  }
]
</script>

<style scoped>
.home-container {
  padding: 40px;
  text-align: center;
}

.header {
  margin-bottom: 40px;
}

.title {
  font-size: 3em;
  font-weight: bold;
  color: #333;
}

.subtitle {
  font-size: 1.2em;
  color: #888;
}

.card-container {
  margin-bottom: 40px;
}

.box-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.box-card:hover {
  transform: translateY(-10px);
}

.card-content {
  padding: 20px;
}

.card-icon {
  margin-bottom: 15px;
  color: #409EFF;
}

.card-title {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 10px;
}

.card-description {
  color: #888;
}

.generate-data-container {
  margin-top: 20px;
}
</style>