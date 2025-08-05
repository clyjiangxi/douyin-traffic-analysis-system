<template>
  <el-container class="app-container">
    <el-aside width="200px" class="app-aside">
      <div class="logo-container">
        <el-icon><Platform /></el-icon>
        <span>广告分析平台</span>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        class="app-menu"
      >
        <el-menu-item index="/">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/accounts">
          <el-icon><User /></el-icon>
          <span>账号管理</span>
        </el-menu-item>
        <el-menu-item index="/advertiser-requests">
          <el-icon><EditPen /></el-icon>
          <span>广告主需求</span>
        </el-menu-item>
        <el-menu-item index="/visualization">
          <el-icon><DataAnalysis /></el-icon>
          <span>数据可视化</span>
        </el-menu-item>
        <el-menu-item index="/recommend">
          <el-icon><MagicStick /></el-icon>
          <span>账号推荐</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="app-header">
        <div style="flex-grow: 1;"></div>
        <div style="text-align: right;padding-right: 2rem;margin-top: 20px;">
          <template v-if="user">
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                <span>
                  {{ user.username }}
                  <el-tag v-if="user.role === 'admin'" type="success" size="small" style="margin-left: 8px;">管理员</el-tag>
                </span>
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout"><el-icon><SwitchButton /></el-icon>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button type="primary" @click="$router.push('/login')">登录</el-button>
          </template>
        </div>
      </el-header>
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { House, User, EditPen, DataAnalysis, MagicStick, Platform, ArrowDown, SwitchButton } from '@element-plus/icons-vue'

const user = ref(null)
const router = useRouter()

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

window.addEventListener('storage', fetchUser)

function logout() {
  localStorage.removeItem('token')
  user.value = null
  ElMessage.success('已退出登录')
  router.replace('/login')
}

function handleCommand(command) {
  if (command === 'logout') {
    logout()
  }
}
</script>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.app-container {
  height: 100vh;
}

.app-aside {
  background-color: #304156;
  color: #bfcbd9;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #fff;
}

'''.app-menu {
  border-right: none !important;
  background-color: transparent !important;
}

.el-menu-item {
  color: #bfcbd9 !important;
  background-color: transparent !important;
}

.el-menu-item:hover {
  background-color: #263445 !important;
}

.el-menu-item.is-active {
  color: #409EFF !important;
  background-color: #263445 !important;
}'''

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e6e6e6;
}

.app-main {
  background-color: #f0f2f5;
}

.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
  display: flex;
  align-items: center;
  border: none;
}
</style>