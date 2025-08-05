<template>
  <div class="request-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span><el-icon><EditPen /></el-icon> 广告主需求管理</span>
          <el-button v-if="isAdmin" type="primary" :icon="Download" @click="exportXLSX">导出Excel</el-button>
          <el-button type="info" :icon="Refresh" @click="fetchRequests">刷新数据</el-button>
        </div>
      </template>

      <el-form :model="form" ref="formRef" :rules="rules" inline class="add-form" v-if="isAdmin">
        <el-form-item label="广告主" prop="advertiser">
          <el-input v-model="form.advertiser" placeholder="广告主名称" />
        </el-form-item>
        <el-form-item label="产品类型">
          <el-input v-model="form.product_type" placeholder="产品类型" />
        </el-form-item>
        <el-form-item label="目标人群">
          <el-input v-model="form.target_audience" placeholder="目标人群" />
        </el-form-item>
        <el-form-item label="预算">
          <el-input-number v-model="form.budget" :min="0" />
        </el-form-item>
        <el-form-item label="需求描述">
          <el-input v-model="form.description" placeholder="需求描述" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" :loading="loading">添加需求</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="requests" v-loading="tableLoading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="advertiser" label="广告主" />
        <el-table-column prop="product_type" label="产品类型" />
        <el-table-column prop="target_audience" label="目标人群" />
        <el-table-column prop="budget" label="预算" />
        <el-table-column prop="description" label="需求描述" />
        <el-table-column prop="created_at" label="创建时间" :formatter="formatDate" />
        <el-table-column label="操作" width="200" v-if="isAdmin">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="onEdit(row)" :icon="Edit">编辑</el-button>
            <el-button size="small" type="danger" @click="onDelete(row.id)" :loading="deleteLoadingId === row.id" :icon="Delete">删除</el-button>
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

    <el-dialog v-model="editVisible" title="编辑需求" width="500px">
      <el-form :model="editForm" ref="editFormRef" label-width="80px">
        <el-form-item label="广告主">
          <el-input v-model="editForm.advertiser" />
        </el-form-item>
        <el-form-item label="产品类型">
          <el-input v-model="editForm.product_type" />
        </el-form-item>
        <el-form-item label="目标人群">
          <el-input v-model="editForm.target_audience" />
        </el-form-item>
        <el-form-item label="预算">
          <el-input-number v-model="editForm.budget" :min="0" />
        </el-form-item>
        <el-form-item label="需求描述">
          <el-input v-model="editForm.description" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" @click="onEditSubmit" :loading="editLoading">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { getAdvertiserRequests, createAdvertiserRequest, deleteAdvertiserRequest, updateAdvertiserRequest } from '../api'
import axios from 'axios'
import { EditPen, Download, Edit, Delete, Refresh } from '@element-plus/icons-vue'
import * as XLSX from 'xlsx';

const requests = ref([])
const form = ref({ advertiser: '', product_type: '', target_audience: '', budget: 0, description: '' })
const formRef = ref()
const loading = ref(false)
const tableLoading = ref(false)
const deleteLoadingId = ref(null)
const page = ref(1)
const pageSize = 10
const total = ref(0)

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

const rules = {
  advertiser: [{ required: true, message: '请输入广告主名称', trigger: 'blur' }],
}

const fetchRequests = async () => {
  tableLoading.value = true
  try {
    const res = await getAdvertiserRequests({ skip: (page.value - 1) * pageSize, limit: pageSize })
    requests.value = res.data.items
    total.value = res.data.total
  } catch (e) {
    ElMessage.error('获取需求数据失败')
  } finally {
    tableLoading.value = false
  }
}
onMounted(fetchRequests)

const onSubmit = () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      await createAdvertiserRequest(form.value)
      ElMessage.success('添加成功')
      form.value = { advertiser: '', product_type: '', target_audience: '', budget: 0, description: '' }
      fetchRequests()
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
    await deleteAdvertiserRequest(id)
    ElMessage.success('删除成功')
    fetchRequests()
  } catch (e) {
    ElMessage.error('删除失败')
  } finally {
    deleteLoadingId.value = null
  }
}

const handlePageChange = (val) => {
  page.value = val
  fetchRequests()
}

// 编辑相关
const editVisible = ref(false)
const editForm = ref({ id: null, advertiser: '', product_type: '', target_audience: '', budget: 0, description: '' })
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
      await updateAdvertiserRequest(editForm.value.id, editForm.value)
      ElMessage.success('修改成功')
      editVisible.value = false
      fetchRequests()
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

function exportXLSX() {
  if (!requests.value.length) return;
  const header = ['ID','广告主','产品类型','目标人群','预算','需求描述','创建时间'];
  const rows = requests.value.map(r => [
    r.id,
    r.advertiser,
    r.product_type,
    r.target_audience,
    r.budget,
    r.description,
    formatDate({ created_at: r.created_at }, null)
  ]);
  const ws = XLSX.utils.aoa_to_sheet([header, ...rows]);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, '广告主需求');
  XLSX.writeFile(wb, 'advertiser_requests.xlsx');
}
</script>

<style scoped>
.request-container {
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