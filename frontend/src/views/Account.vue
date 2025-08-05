<template>
  <div class="account-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span><el-icon><User /></el-icon> 账号管理</span>
          <el-button v-if="isAdmin" type="primary" :icon="Download" @click="exportXLSX">导出Excel</el-button>
          <el-button type="info" :icon="Refresh" @click="fetchAccounts">刷新数据</el-button>
        </div>
      </template>

      <el-form :model="form" ref="formRef" :rules="rules" inline class="add-form">
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="抖音昵称" :disabled="!isAdmin" />
        </el-form-item>
        <el-form-item label="抖音号" prop="douyin_id">
          <el-input v-model="form.douyin_id" placeholder="抖音号" :disabled="!isAdmin" />
        </el-form-item>
        <el-form-item label="粉丝数">
          <el-input-number v-model="form.fans_count" :min="0" :disabled="!isAdmin" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" :loading="loading" :disabled="!isAdmin">添加账号</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="accounts" v-loading="tableLoading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="nickname" label="昵称" />
        <el-table-column prop="douyin_id" label="抖音号" />
        <el-table-column prop="fans_count" label="粉丝数" />
        <el-table-column prop="created_at" label="创建时间" :formatter="formatDate" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <div v-if="isAdmin">
              <el-button size="small" type="primary" @click="onEdit(row)" :icon="Edit">编辑</el-button>
              <el-button size="small" type="danger" @click="onDelete(row.id)" :loading="deleteLoadingId === row.id" :icon="Delete">删除</el-button>
            </div>
            <span v-else class="text-secondary small">仅管理员可操作</span>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-if="total > pageSize"
        background
        layout="prev, pager, next"
        :total="total"
        :page-size="pageSize"
        @current-change="handlePageChange"
        class="pagination-container"
      />
    </el-card>

    <el-dialog v-model="editVisible" title="编辑账号" width="500px">
      <el-form :model="editForm" ref="editFormRef" label-width="80px">
        <el-form-item label="昵称">
          <el-input v-model="editForm.nickname" :disabled="!isAdmin" />
        </el-form-item>
        <el-form-item label="抖音号">
          <el-input v-model="editForm.douyin_id" :disabled="!isAdmin" />
        </el-form-item>
        <el-form-item label="粉丝数">
          <el-input-number v-model="editForm.fans_count" :min="0" :disabled="!isAdmin" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" @click="onEditSubmit" :loading="editLoading" :disabled="!isAdmin">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { getAccounts, createAccount, deleteAccount, updateAccount } from '../api'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { User, Download, Edit, Delete, Refresh } from '@element-plus/icons-vue'
import * as XLSX from 'xlsx';

const accounts = ref([])
const form = ref({ nickname: '', douyin_id: '', fans_count: 0 })
const formRef = ref()
const loading = ref(false)
const tableLoading = ref(false)
const deleteLoadingId = ref(null)
const page = ref(1)
const pageSize = 10
const total = ref(0)

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

const isAdmin = computed(() => user.value && user.value.role === 'admin')

const rules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  douyin_id: [{ required: true, message: '请输入抖音号', trigger: 'blur' }],
}

const fetchAccounts = async () => {
  tableLoading.value = true
  try {
    const res = await getAccounts({ skip: (page.value - 1) * pageSize, limit: pageSize })
    accounts.value = res.data.items
    total.value = res.data.total
  } catch (e) {
    ElMessage.error('获取账号数据失败')
  } finally {
    tableLoading.value = false
  }
}
onMounted(fetchAccounts)

const onSubmit = () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      await createAccount(form.value)
      ElMessage.success('添加成功')
      form.value = { nickname: '', douyin_id: '', fans_count: 0 }
      fetchAccounts()
    } catch (e) {
      ElMessage.error('添加失败')
    } finally {
      loading.value = false
    }
  })
}

const onDelete = async (id) => {
  deleteLoadingId.value = id
  try {
    await deleteAccount(id)
    ElMessage.success('删除成功')
    fetchAccounts()
  } catch (e) {
    ElMessage.error('删除失败')
  } finally {
    deleteLoadingId.value = null
  }
}

const handlePageChange = (val) => {
  page.value = val
  fetchAccounts()
}

// 编辑相关
const editVisible = ref(false)
const editForm = ref({ id: null, nickname: '', douyin_id: '', fans_count: 0 })
const editFormRef = ref()
const editLoading = ref(false)
const onEdit = (row) => {
  editForm.value = { ...row }
  editVisible.value = true
}
const onEditSubmit = () => {
  editFormRef.value.validate(async (valid) => {
    if (!valid) return
    editLoading.value = true
    try {
      await updateAccount(editForm.value.id, editForm.value)
      ElMessage.success('修改成功')
      editVisible.value = false
      fetchAccounts()
    } catch (e) {
      ElMessage.error('修改失败')
    } finally {
      editLoading.value = false
    }
  })
}

function formatDate(row, column) {
  const date = new Date(row.created_at);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function exportCSV() {
  if (!accounts.value.length) return;
  const header = ['ID','昵称','抖音号','粉丝数','创建时间'];
  const rows = accounts.value.map(a => [
    a.id,
    a.nickname,
    a.douyin_id,
    a.fans_count,
    formatDate({ created_at: a.created_at }, null)
  ]);
  const BOM = new Uint8Array([0xEF, 0xBB, 0xBF]);
  const csvContent = [header, ...rows]
    .map(row => row.map(String).map(s => `"${s.replace(/"/g,'""')}` + '"').join(','))
    .join('\n');
  const blob = new Blob([BOM, csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'accounts.csv';
  a.click();
  URL.revokeObjectURL(url);
}

function exportXLSX() {
  const header = ['ID','昵称','抖音号','粉丝数','创建时间'];
  const rows = accounts.value.map(a => [
    a.id,
    a.nickname,
    a.douyin_id,
    a.fans_count,
    formatDate({ created_at: a.created_at }, null)
  ]);
  const ws = XLSX.utils.aoa_to_sheet([header, ...rows]);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, '账号');
  XLSX.writeFile(wb, 'accounts.xlsx');
}
</script>

<style scoped>
.account-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add-form {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>