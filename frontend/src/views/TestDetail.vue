<template>
  <div class="test-detail-container" v-if="test">
    <h2>{{ test.title }}</h2>

    <div v-for="question in test.questions" :key="question.id" class="question-block">
      <p>{{ question.text }}</p>

      <ul>
        <li v-for="answer in question.answers" :key="answer.id">
          <label>
            <input
              type="radio"
              :name="question.id"
              :value="answer.id"
              v-model="userAnswers[question.id]"
            />
            {{ answer.text }}
          </label>
        </li>
      </ul>
    </div>

    <button @click="submitTest" :disabled="loading || !allAnswered">Сдать тест</button>

    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="result" class="result">
      Тест сдан! Правильных ответов: {{ result.score }}
    </div>
  </div>

  <div v-else-if="loading">Загрузка теста...</div>
  <div v-else-if="error" class="error">{{ error }}</div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axiosInstance from '@/axiosInstance'

export default {
  name: 'TestDetail',
  setup() {
    const route = useRoute()
    const testId = route.params.id
    const test = ref(null)
    const userAnswers = ref({})
    const loading = ref(false)
    const error = ref(null)
    const result = ref(null)

    const allAnswered = computed(() => {
      if (!test.value) return false
      return test.value.questions.every(q => userAnswers.value[q.id])
    })

    async function loadTest() {
      loading.value = true
      error.value = null
      try {
        const res = await axiosInstance.get(`/tests/tests/${testId}`)
        test.value = res.data
      } catch (e) {
        error.value = 'Ошибка загрузки теста: ' + (e.response?.data?.detail || e.message)
      } finally {
        loading.value = false
      }
    }

    async function submitTest() {
      if (!allAnswered.value) {
        error.value = 'Ответьте на все вопросы'
        return
      }
      loading.value = true
      error.value = null
      try {
        const answersPayload = Object.entries(userAnswers.value).map(([questionId, answerId]) => ({
          question_id: questionId,
          answer_id: answerId,
        }))
        const res = await axiosInstance.post(`/tests/tests/${testId}/submit`, {
          answers: answersPayload,
        })
        result.value = res.data
      } catch (e) {
        error.value = 'Ошибка при сдаче теста: ' + (e.response?.data?.detail || e.message)
      } finally {
        loading.value = false
      }
    }

    onMounted(loadTest)

    return { test, userAnswers, loading, error, submitTest, result, allAnswered }
  },
}
</script>

<style scoped>
body {
  background-color: #121212;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #e5e5e5;
  margin: 0;
  padding: 0;
}

.tests-container {
  max-width: 600px;
  margin: 4rem auto;
  padding: 2.5rem;
  background: linear-gradient(145deg, #1e1e1e, #1a1a1a);
  border-radius: 20px;
  box-shadow: 0 20px 30px rgba(0, 0, 0, 0.4);
  color: #ffffff;
  transition: transform 0.3s ease;
}

.tests-container:hover {
  transform: scale(1.01);
}

.tests-title,
.results-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1.8rem;
  text-align: center;
  color: #ffffff;
}

.tests-list,
.results-list {
  list-style: none;
  padding: 0;
  margin-bottom: 2rem;
}

.test-item,
.result-item {
  padding: 1rem 1.2rem;
  margin-bottom: 1rem;
  background-color: #2a2a2a;
  border-radius: 12px;
  font-size: 1.1rem;
  color: #dddddd;
  transition: background-color 0.2s ease, transform 0.2s ease;
  cursor: pointer;
}

.test-item:hover,
.result-item:hover {
  background-color: #3a3a3a;
  transform: translateY(-2px);
}

.test-item a {
  color: #40f0a8;
  font-weight: 600;
  text-decoration: none;
}

.test-item a:hover {
  text-decoration: underline;
}

.error {
  text-align: center;
  color: #ff4f4f;
  font-weight: 600;
  margin-top: 1rem;
  font-size: 1rem;
}
</style>
