const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

async function request(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
    ...options,
  };

  if (config.body && typeof config.body !== 'string') {
    config.body = JSON.stringify(config.body);
  }

  const response = await fetch(`${API_URL}${endpoint}`, config);
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || data.detail || 'Request failed.');
  }

  return data;
}

export const api = {
  register: (payload) => request('/api/register/', { method: 'POST', body: payload }),
  login: (payload) => request('/api/login/', { method: 'POST', body: payload }),
  getSkills: () => request('/api/skills/'),
  createSkill: (payload) => request('/api/skills/', { method: 'POST', body: payload }),
  updateSkill: (id, payload) => request(`/api/skills/${id}/`, { method: 'PUT', body: payload }),
  deleteSkill: (id) => request(`/api/skills/${id}/`, { method: 'DELETE' }),
  getDashboard: () => request('/api/dashboard/'),
  getLearning: () => request('/api/learning/'),
  createLearning: (payload) => request('/api/learning/', { method: 'POST', body: payload }),
  getRecommendations: () => request('/api/recommendations/'),
  getAiSummary: (payload = {}) => request('/api/ai/summary/', { method: 'POST', body: payload }),
};
