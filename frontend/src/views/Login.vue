<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <span><el-icon><User /></el-icon> 登录</span>
        </div>
      </template>
      <el-form @submit.prevent="onLogin" :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onLogin" :loading="loading" style="width: 100%;">登录</el-button>
        </el-form-item>
      </el-form>
      <div class="register-link">
        <span>没有账号？</span>
        <el-link type="primary" @click="showRegister = true">立即注册</el-link>
      </div>
    </el-card>

    <el-dialog v-model="showRegister" title="注册" width="400px" center>
      <el-form @submit.prevent="onRegister" :model="regForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="regForm.username" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="regForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showRegister = false">取消</el-button>
          <el-button type="primary" @click="onRegister" :loading="regLoading">注册</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const form = ref({ username: '', password: '' })
const loading = ref(false)
const router = useRouter()
const route = useRoute()

const showRegister = ref(false)
const regForm = ref({ username: '', password: '' })
const regLoading = ref(false)

async function onLogin() {
  loading.value = true
  try {
    const res = await axios.post('/login', new URLSearchParams(form.value), { baseURL: 'http://localhost:8002' })
    localStorage.setItem('token', res.data.access_token)
    ElMessage.success('登录成功')
    router.replace(route.query.redirect || '/')
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}

async function onRegister() {
  regLoading.value = true
  try {
    await axios.post('/register', regForm.value, { baseURL: 'http://localhost:8002' })
    ElMessage.success('注册成功，请登录')
    showRegister.value = false
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '注册失败')
  } finally {
    regLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.login-card {
  width: 400px;
  border-radius: 15px;
}

.card-header {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
}

.register-link {
  margin-top: 15px;
  text-align: center;
}

.dialog-footer {
  text-align: right;
}
</style>