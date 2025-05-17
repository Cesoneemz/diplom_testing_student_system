import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/tests/tests', // твой backend URL
  withCredentials: true, // если нужна куки авторизация
})

export async function fetchTests() {
  const response = await api.get('/')
  return response.data
}

export async function fetchTestById(testId) {
  const response = await api.get(`/${testId}`)
  return response.data
}

export async function createTest(testData) {
  const response = await api.post('/', testData)
  return response.data
}

export async function updateTest(testId, testData) {
  const response = await api.put(`/${testId}`, testData)
  return response.data
}

export async function deleteTest(testId) {
  await api.delete(`/${testId}`)
}

export async function updateQuestion(questionId, questionData) {
  const response = await api.put(`/questions/${questionId}`, questionData)
  return response.data
}

export async function deleteQuestion(questionId) {
  await api.delete(`/questions/${questionId}`)
}

export async function submitTest(testId, submission) {
  const response = await api.post(`/${testId}/submit`, submission)
  return response.data
}
