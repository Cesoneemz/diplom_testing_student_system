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
.test-detail-container {
  max-width: 720px;
  margin: 4rem auto;
  padding: 2.5rem;
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.45);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #f0f0f0;
}

.test-detail-container h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
  color: black;
}

.question-block {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: #f6f9fc;
  border-radius: 14px;
  box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.3);
}

.question-block p {
  margin-bottom: 1rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: black;
}

.question-block ul {
  list-style: none;
  padding-left: 0;
}

.question-block li {
  margin-bottom: 0.8rem;
}

.question-block label {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 1.05rem;
  color: black;
  cursor: pointer;
  transition: color 0.2s ease;
}

.question-block input[type="radio"] {
  accent-color: #40f0a8;
  transform: scale(1.1);
  cursor: pointer;
}

button {
  display: block;
  width: 100%;
  margin-top: 2rem;
  padding: 0.9rem;
  background-color: #40f0a8;
  color: #0d0d0d;
  font-size: 1.1rem;
  font-weight: 700;
  border: none;
  border-radius: 10px;
  transition: background-color 0.3s ease, transform 0.2s ease;
  cursor: pointer;
}

button:hover {
  background-color: #34d29c;
  transform: translateY(-2px);
}

button:disabled {
  background-color: #888888;
  cursor: not-allowed;
  opacity: 0.6;
}

.result {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #ffffff;
  border: 1px solid #5a5a5a;
  border-radius: 10px;
  font-size: 1.2rem;
  font-weight: 600;
  color: #90f3c5;
  text-align: center;
}

.error {
  text-align: center;
  color: #ff4f4f;
  font-weight: 600;
  margin-top: 1.5rem;
  font-size: 1rem;
}

</style>
