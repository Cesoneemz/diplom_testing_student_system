import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    role: null // Добавляем роль
  }),
  actions: {
    setUser(token, role) {
      this.token = token
      this.role = role
    },
    clearUser() {
      this.token = null
      this.role = null
    }
  }
})
