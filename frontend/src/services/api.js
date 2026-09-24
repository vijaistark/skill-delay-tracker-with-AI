const API_URL = import.meta.env.VITE_API_URL || '';

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

  try {
    const response = await fetch(`${API_URL}${endpoint}`, config);
    const contentType = response.headers.get('content-type') || '';
    const isJson = contentType.includes('application/json');
    const data = isJson ? await response.json().catch(() => ({})) : await response.text().catch(() => '');

    if (!response.ok) {
      const message = data?.error || data?.detail || data?.message || (typeof data === 'string' && data) || 'Request failed.';
      throw new Error(message);
    }

    return data;
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error('Unable to reach the backend. Check the backend URL and CORS configuration.');
    }
    throw error;
  }
}

export const api = {
  register: (payload) =>
    request('/api/register/', { method: 'POST', body: payload }),

  login: (payload) =>
    request('/api/login/', { method: 'POST', body: payload }),

  getSkills: () =>
    request('/api/skills/'),

  createSkill: (payload) =>
    request('/api/skills/', { method: 'POST', body: payload }),

  updateSkill: (id, payload) =>
    request(`/api/skills/${id}/`, { method: 'PUT', body: payload }),

  deleteSkill: (id) =>
    request(`/api/skills/${id}/`, { method: 'DELETE' }),

  getDashboard: () =>
    request('/api/dashboard/'),

  getLearning: () =>
    request('/api/learning/'),

  createLearning: (payload) =>
    request('/api/learning/', { method: 'POST', body: payload }),

  getRecommendations: () =>
    request('/api/recommendations/'),

  getAiSummary: (payload = {}) =>
    request('/api/ai/summary/', { method: 'POST', body: payload }),
};