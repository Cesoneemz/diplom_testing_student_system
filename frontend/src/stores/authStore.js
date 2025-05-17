import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    username: null
  }),
  actions: {
    setToken(token) {
      this.token = token
    },
    clearToken() {
      this.token = null
      this.username = null
    }
  }
})
