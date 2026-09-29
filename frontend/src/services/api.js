const BASE_URL = 'https://impactnexus-backend.onrender.com'

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, options)
  if (!response.ok) throw new Error(`API request failed (${response.status})`)
  return response.json()
}

function flattenIntelligence(data) {
  if (!data?.satellite && data?.ndvi !== undefined) return data
  const satellite = data?.satellite || {}
  const weather = data?.weather || {}
  const soil = data?.soil || {}
  return {
    ndvi: satellite.NDVI ?? satellite.ndvi,
    evi: satellite.EVI ?? satellite.evi,
    savi: satellite.SAVI ?? satellite.savi,
    ndmi: satellite.NDMI ?? satellite.ndmi,
    cloud_cover: satellite.cloud ?? satellite.cloud_cover,
    temperature: weather.temperature,
    humidity: weather.humidity,
    rainfall: weather.rainfall,
    wind: weather.wind,
    forecast: weather.forecast,
    ph: soil.pH ?? soil.ph,
    npk: soil.NPK ?? soil.npk,
    organic_carbon: soil.organic_carbon,
    soil_moisture: soil.soil_moisture,
    soil_health_score: soil.soil_health_score,
  }
}

function normalizeAdvisory(data) {
  if (!data || typeof data !== 'object') return data
  let recommendations = data.recommendations
  if (Array.isArray(recommendations) && typeof recommendations[0] === 'string') {
    recommendations = recommendations.map((text) => ({ category: 'Farm action', text, priority: 'Medium' }))
  }
  const first = recommendations?.[0]
  const recommendation = data.recommendation || (typeof first === 'string' ? first : first?.text)
  return { ...data, recommendations, recommendation }
}

function normalizeDiagnosis(data) {
  if (!data || typeof data !== 'object') return data
  const confidence = Number(data.confidence)
  if (!Number.isFinite(confidence)) return data
  return { ...data, confidence: confidence <= 1 ? Math.round(confidence * 100) : Math.round(confidence) }
}

export const api = {
  getFarm: (farmId) => request(`/api/farm/${farmId}`),
  getFarmIntelligence: async (farmId) => flattenIntelligence(await request(`/api/farm/${farmId}/intelligence`)),
  getFarmAdvisory: async (farmId) => normalizeAdvisory(await request(`/api/farm/${farmId}/advisory`)),
  getBricsModels: () => request('/api/brics/models'),
  getBricsSchema: () => request('/api/brics/schema'),
  analyzeCropDoctor: async (image) => {
    const body = new FormData()
    body.append('leaf_image', image)
    return normalizeDiagnosis(await request('/api/crop-doctor', { method: 'POST', body }))
  },
}
