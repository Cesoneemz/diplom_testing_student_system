import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/Home.vue'
import Login from './views/Login.vue'
import TestDetail from './views/TestDetail.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: Login },
  { path: '/tests/:id', component: TestDetail, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
//   const token = authStore.token

//   if (!token && to.path !== '/login') {
//     // Если токена нет и пользователь идёт не на логин — редирект на /login
//     next('/login')
//   } else if (token && to.path === '/login') {
//     // Если токен есть и пытается зайти на /login — редирект на /
//     next('/')
//   } else {
//     next()
//   }
// })


export default router
