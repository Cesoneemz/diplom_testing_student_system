<template>
  <div>
    <h1>Добро пожаловать</h1>
    <TestList />
  </div>
</template>

<script>
import TestList from '../components/TestList.vue'

export default {
  name: 'HomeView',
  components: { TestList }
}
</script>
