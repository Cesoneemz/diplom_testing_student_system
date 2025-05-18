<template>
  <div class="login">
    <h1 class="title">Вход в систему</h1>
    <LoginForm />
  </div>
</template>

<script>
import LoginForm from '../components/LoginForm.vue'

export default {
  name: 'Login',
  components: { LoginForm }
}
</script>

<style scoped>
.login {
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

.title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 2.5rem;
  color: #333333;
}
</style>
