import { defineStore } from 'pinia'
import * as api from '../api/tests'

export const useTestsStore = defineStore('tests', {
  state: () => ({
    tests: [],
    currentTest: null,
    loading: false,
    error: null,
    result: null,
  }),
  actions: {
    async loadTests() {
      this.loading = true
      try {
        this.tests = await api.fetchTests()
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async loadTest(id) {
      this.loading = true
      try {
        this.currentTest = await api.fetchTestById(id)
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async createTest(testData) {
      this.loading = true
      try {
        const newTest = await api.createTest(testData)
        this.tests.push(newTest)
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async updateTest(id, testData) {
      this.loading = true
      try {
        const updated = await api.updateTest(id, testData)
        const idx = this.tests.findIndex(t => t.id === id)
        if (idx !== -1) this.tests[idx] = updated
        if (this.currentTest?.id === id) this.currentTest = updated
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async deleteTest(id) {
      this.loading = true
      try {
        await api.deleteTest(id)
        this.tests = this.tests.filter(t => t.id !== id)
        if (this.currentTest?.id === id) this.currentTest = null
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async updateQuestion(questionId, questionData) {
      this.loading = true
      try {
        const updatedQuestion = await api.updateQuestion(questionId, questionData)
        // Обновить в currentTest
        if (this.currentTest) {
          const qIndex = this.currentTest.questions.findIndex(q => q.id === questionId)
          if (qIndex !== -1) this.currentTest.questions[qIndex] = updatedQuestion
        }
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async deleteQuestion(questionId) {
      this.loading = true
      try {
        await api.deleteQuestion(questionId)
        if (this.currentTest) {
          this.currentTest.questions = this.currentTest.questions.filter(q => q.id !== questionId)
        }
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async submitTest(testId, answers) {
      this.loading = true
      this.result = null
      try {
        // answers: [{question_id, answer_id}, ...]
        this.result = await api.submitTest(testId, { answers })
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
  },
})
