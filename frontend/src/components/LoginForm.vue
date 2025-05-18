<template>
  <div class="login-container">
    <form class="login-form" @submit.prevent="login">
      <h2 class="login-title">Вход в систему</h2>

      <label for="username">Имя пользователя</label>
      <input
        id="username"
        v-model="username"
        type="text"
        required
        placeholder="Введите имя пользователя"
      />

      <label for="password">Пароль</label>
      <input
        id="password"
        v-model="password"
        type="password"
        required
        placeholder="Введите пароль"
      />

      <button type="submit">Войти</button>

      <p class="error-message" v-if="error">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  methods: {
    async login() {
      try {
        const params = new URLSearchParams()
        params.append('username', this.username)
        params.append('password', this.password)

        const res = await axios.post('http://localhost:8000/auth/login', params)

        this.authStore.setUser(res.data.access_token, res.data.user_role)
        this.$router.push('/')
      } catch (err) {
        this.error = 'Ошибка входа: ' + (err.response?.data?.detail || err.message)
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  padding-top: 6vh;
  min-height: 100vh;
  background-color: #f9f9f9;
}

.login-form {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.login-title {
  text-align: center;
  font-size: 1.5rem;
  color: #333333;
  margin-bottom: 1rem;
}

.login-form label {
  font-weight: 500;
  color: #444444;
}

.login-form input {
  padding: 0.6rem 0.8rem;
  border: 1px solid #cccccc;
  border-radius: 8px;
  background-color: #ffffff;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.login-form input:focus {
  outline: none;
  border-color: #007bff;
}

.login-form button {
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  background-color: #007bff;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-form button:hover {
  background-color: #0056b3;
}

.error-message {
  color: #d9534f;
  font-size: 0.95rem;
  text-align: center;
}

</style>
