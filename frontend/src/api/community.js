const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options)
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.message || '请求失败，请稍后再试。')
  return data
}

export const listComments = (pageKey, anchor = '') => request(`/comments/?page=${encodeURIComponent(pageKey)}&anchor=${encodeURIComponent(anchor)}`)
export const createComment = (payload) => request('/comments/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload),
})
export const likeComment = (id) => request(`/comments/${id}/like/`, { method: 'POST' })
export const listUgc = (category = '') => request(`/ugc/?category=${encodeURIComponent(category)}`)
export const createUgc = (payload) => request('/ugc/', { method: 'POST', body: payload })
export const likeUgc = (id) => request(`/ugc/${id}/like/`, { method: 'POST' })
