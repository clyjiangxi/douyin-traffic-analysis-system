import { createRouter, createWebHistory } from 'vue-router'
import Account from '../views/Account.vue'
import AdvertiserRequest from '../views/AdvertiserRequest.vue'
import Home from '../views/Home.vue'
import DataVisualization from '../views/DataVisualization.vue'
import Recommend from '../views/Recommend.vue'
import Login from '../views/Login.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/accounts', name: 'Account', component: Account, meta: { requiresAuth: true } },
  { path: '/advertiser-requests', name: 'AdvertiserRequest', component: AdvertiserRequest, meta: { requiresAuth: true } },
  { path: '/visualization', name: 'DataVisualization', component: DataVisualization, meta: { requiresAuth: true } },
  { path: '/recommend', name: 'Recommend', component: Recommend, meta: { requiresAuth: true } },
  { path: '/login', name: 'Login', component: Login },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router 