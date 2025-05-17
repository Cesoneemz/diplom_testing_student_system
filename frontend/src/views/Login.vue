<template>
  <div>
    <h1>Вход в систему</h1>
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
