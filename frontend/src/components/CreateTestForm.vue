<template>
  <div class="test-create-container">
    <form class="test-create-form" @submit.prevent="createTest">
      <h2 class="form-title">Создание теста</h2>

      <label for="title">Название теста</label>
      <input
        id="title"
        v-model="title"
        type="text"
        required
        placeholder="Введите название теста"
      />

      <div v-for="(question, qIndex) in questions" :key="qIndex" class="question-block">
        <label>Вопрос {{ qIndex + 1 }}</label>
        <input
          v-model="question.text"
          type="text"
          required
          placeholder="Введите текст вопроса"
        />

        <div
          v-for="(answer, aIndex) in question.answers"
          :key="aIndex"
          class="answer-block"
        >
          <input
            v-model="answer.text"
            type="text"
            required
            placeholder="Введите текст ответа"
          />
          <label>
            <input
              type="checkbox"
              v-model="answer.is_correct"
            />
            Правильный
          </label>
          <button type="button" @click="removeAnswer(qIndex, aIndex)">Удалить ответ</button>
        </div>

        <button type="button" @click="addAnswer(qIndex)">Добавить ответ</button>
        <button type="button" @click="removeQuestion(qIndex)" class="remove-question-btn">
          Удалить вопрос
        </button>
      </div>

      <button type="button" @click="addQuestion" class="add-question-btn">
        Добавить вопрос
      </button>

      <button type="submit" class="submit-btn">Создать тест</button>

      <p class="error-message" v-if="error">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

export default {
  name: 'TestCreateForm',
  data() {
    return {
      title: '',
      questions: [
        {
          text: '',
          answers: [
            { text: '', is_correct: false },
            { text: '', is_correct: false }
          ],
        }
      ],
      error: ''
    }
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  methods: {
    addQuestion() {
      this.questions.push({
        text: '',
        answers: [
          { text: '', is_correct: false },
          { text: '', is_correct: false }
        ]
      })
    },
    removeQuestion(index) {
      this.questions.splice(index, 1)
    },
    addAnswer(qIndex) {
      this.questions[qIndex].answers.push({ text: '', is_correct: false })
    },
    removeAnswer(qIndex, aIndex) {
      this.questions[qIndex].answers.splice(aIndex, 1)
    },
    async createTest() {
      try {
        this.error = ''

        // Формируем payload строго по схемам TestCreateFull
        const payload = {
          title: this.title,
          questions: this.questions.map(q => ({
            text: q.text,
            answers: q.answers.map(a => ({
              text: a.text,
              is_correct: a.is_correct
            }))
          }))
        }

        const config = {
          headers: {
            Authorization: `Bearer ${this.authStore.token}`
          }
        }

        await axios.post('http://localhost:8000/tests/tests', payload, config)

        this.$router.push('/')
      } catch (err) {
        this.error = 'Ошибка создания теста: ' + (err.response?.data?.detail || err.message)
      }
    }
  }
}
</script>

<style scoped>
.test-create-container {
  display: flex;
  justify-content: center;
  padding-top: 4vh;
  min-height: 100vh;
  background-color: #f9f9f9;
}

.test-create-form {
  background-color: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 700px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-title {
  text-align: center;
  font-size: 1.75rem;
  color: #333;
  margin-bottom: 1rem;
}

label {
  font-weight: 600;
  color: #444;
  margin-bottom: 0.25rem;
}

input[type="text"] {
  padding: 0.6rem 0.8rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input[type="text"]:focus {
  outline: none;
  border-color: #007bff;
}

.question-block {
  background: #f7f7f7;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.answer-block {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.answer-block input[type="text"] {
  flex-grow: 1;
}

button {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #0056b3;
  color: white;
}

button[type="button"] {
  background-color: #007bff;
  color: white;
}

.remove-question-btn {
  background-color: #d9534f;
  color: white;
  margin-top: 0.5rem;
}

.add-question-btn {
  background-color: #28a745;
  color: white;
  align-self: center;
}

.submit-btn {
  background-color: #007bff;
  color: white;
  font-size: 1.1rem;
  margin-top: 1rem;
}

.error-message {
  color: #d9534f;
  text-align: center;
  font-weight: 600;
}
</style>
