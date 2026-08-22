const BASE_URL = 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, options)
  if (!response.ok) throw new Error(`API request failed (${response.status})`)
  return response.json()
}

export const api = {
  getFarm: (farmId) => request(`/api/farm/${farmId}`),
  getFarmIntelligence: (farmId) => request(`/api/farm/${farmId}/intelligence`),
  getFarmAdvisory: (farmId) => request(`/api/farm/${farmId}/advisory`),
  getBricsModels: () => request('/api/brics/models'),
  getBricsSchema: () => request('/api/brics/schema'),
  analyzeCropDoctor: (image) => {
    const body = new FormData()
    body.append('leaf_image', image)
    return request('/api/crop-doctor', { method: 'POST', body })
  },
}
