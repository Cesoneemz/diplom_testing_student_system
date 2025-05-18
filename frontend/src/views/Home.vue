<template>
  <div class="home">
    <h1 class="welcome">Добро пожаловать</h1>

    <TestList />

    <router-link
      v-if="authStore.role === 'admin' || authStore.role === 'teacher'"
      to="/create-test"
      class="create-test-link"
    >
      Создать тест
    </router-link>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/authStore'
import TestList from '../components/TestList.vue'

export default {
  name: 'HomeView',
  components: { TestList },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  }
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh;
  background-color: #f9f9fb;
  padding: 3rem 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #222222;
}

.welcome {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 2.5rem;
  color: #333333;
}

.create-test-link {
  margin-top: 2rem;
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  font-weight: 600;
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.2s;
}

.create-test-link:hover {
  background-color: #0056b3;
}
</style>
