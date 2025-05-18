import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/Home.vue'
import Login from './views/Login.vue'
import TestDetail from './views/TestDetail.vue'
import CreateTestForm from './components/CreateTestForm.vue'
import { useAuthStore } from './stores/authStore'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: Login },
  { path: '/tests/:id', component: TestDetail, props: true },
  { path: '/create-test',  component: CreateTestForm, meta: { requiresAuth: true, roles: ['admin', 'teacher']}}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const token = authStore.token
  const userRole = authStore.role

  if (to.meta.requiresAuth) {
    if (!token) {
      // Не авторизован — на логин
      next('/login')
      return
    }

    if (to.meta.roles && !to.meta.roles.includes(userRole)) {
      // Авторизован, но нет нужной роли — можно, например, на главную
      next('/')
      return
    }
  } else {
    // Если пытаемся попасть на логин, когда уже авторизованы — редирект на /
    if (token && to.path === '/login') {
      next('/')
      return
    }
  }

  next()
})


export default router
