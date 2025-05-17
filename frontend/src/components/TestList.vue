<template>
  <div class="tests-container">
    <h2 class="tests-title">Список доступных тестов</h2>
    <ul class="tests-list">
      <li v-for="test in tests" :key="test.id" class="test-item">
        <router-link :to="`/tests/${test.id}`">{{ test.title }}</router-link>
      </li>
    </ul>

    <h2 class="results-title" v-if="results.length">Мои результаты</h2>
    <ul class="results-list" v-if="results.length">
      <li v-for="result in results" :key="result.id" class="result-item">
        Тест: {{ result.test_title || result.test_id }} — Баллы: {{ result.score }}
      </li>
    </ul>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axiosInstance from '@/axiosInstance'

export default {
  name: 'TestList',
  setup() {
    const tests = ref([])
    const results = ref([])
    const error = ref(null)

    async function fetchTests() {
      try {
        const res = await axiosInstance.get('/tests/tests/')
        tests.value = res.data
      } catch (err) {
        error.value = 'Ошибка при загрузке тестов: ' + (err.response?.data?.detail || err.message)
      }
    }

    async function fetchResults() {
      try {
        const res = await axiosInstance.get('/results/results/')
        results.value = res.data
      } catch (err) {
        error.value = 'Ошибка при загрузке результатов: ' + (err.response?.data?.detail || err.message)
      }
    }

    onMounted(async () => {
      await Promise.all([fetchTests(), fetchResults()])
    })

    return { tests, results, error }
  },
}
</script>

<style scoped>
.tests-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1.5rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.07);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.tests-title,
.results-title {
  margin-bottom: 1.5rem;
  font-size: 1.75rem;
  font-weight: 700;
  color: #222222;
  text-align: center;
}

.tests-list,
.results-list {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem 0;
}

.test-item,
.result-item {
  padding: 0.8rem 1rem;
  margin-bottom: 0.75rem;
  background-color: #f5f7fa;
  border-radius: 8px;
  font-size: 1.1rem;
  color: #333333;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.test-item:hover {
  background-color: #e0e7ff;
}

.error {
  color: red;
  text-align: center;
  margin-top: 1rem;
}
</style>
