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
  max-width: 680px;
  margin: 3rem auto;
  padding: 2rem 2.5rem;
  background-color: #ffffff;
  border-radius: 14px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.06);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.tests-title,
.results-title {
  margin-bottom: 1.8rem;
  font-size: 1.9rem;
  font-weight: 700;
  color: #1f1f1f;
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
  padding: 1rem 1.2rem;
  margin-bottom: 0.85rem;
  background-color: #f6f9fc;
  border: 1px solid #d9e2ec;
  border-radius: 10px;
  font-size: 1.1rem;
  color: #2d2d2d;
  transition: all 0.25s ease;
}

.test-item:hover {
  background-color: #e3ecff;
  border-color: #b0c4ff;
}

.result-item {
  background-color: #f9f9f9;
  border: 1px solid #eeeeee;
}

.result-item:hover {
  background-color: #f1f5ff;
}

.test-item a {
  text-decoration: none;
  color: #1a73e8;
  font-weight: 600;
}

.test-item a:hover {
  text-decoration: underline;
}

.error {
  color: #d93025;
  text-align: center;
  margin-top: 1.5rem;
  font-size: 1rem;
}

</style>
