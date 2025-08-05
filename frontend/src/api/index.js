import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8002', // 根据实际后端端口调整
  timeout: 5000,
});

// 全局响应拦截器
api.interceptors.response.use(
  res => res,
  err => {
    if (err.response) {
      if (err.response.status === 401) {
        localStorage.removeItem('token')
        window.location.href = '/login'
        window.ElMessage && window.ElMessage.error('登录已失效，请重新登录')
      } else if (err.response.status === 403) {
        window.ElMessage && window.ElMessage.error('无权限操作')
      } else {
        window.ElMessage && window.ElMessage.error(err.response.data.detail || '接口异常')
      }
    } else {
      window.ElMessage && window.ElMessage.error('网络异常')
    }
    return Promise.reject(err)
  }
)

// 账号API
export const getAccounts = (params) => api.get('/accounts/', { params });
export const getAccount = (id) => api.get(`/accounts/${id}`);
export const createAccount = (data) => api.post('/accounts/', data);
export const deleteAccount = (id) => api.delete(`/accounts/${id}`);
export const updateAccount = (id, data) => api.put(`/accounts/${id}`, data);

// 广告主需求API
export const getAdvertiserRequests = (params) => api.get('/advertiser_requests/', { params });
export const getAdvertiserRequest = (id) => api.get(`/advertiser_requests/${id}`);
export const createAdvertiserRequest = (data) => api.post('/advertiser_requests/', data);
export const deleteAdvertiserRequest = (id) => api.delete(`/advertiser_requests/${id}`);
export const updateAdvertiserRequest = (id, data) => api.put(`/advertiser_requests/${id}`, data);

export const generateTestData = () => api.post('/generate_test_data/');
export const recommendAccounts = (params) => api.get('/recommend_accounts/', { params });

export default api; 