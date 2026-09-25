import service from './index'

/**
 * Create simulation
 * @param {Object} data - { project_id, graph_id?, enable_twitter?, enable_reddit? }
 */
export const createSimulation = (data) => {
  return service.post('/api/simulation/create', data)
}

/**
 * Prepare simulation environment (async task)
 * @param {Object} data - { simulation_id, entity_types?, use_llm_for_profiles?, parallel_profile_count?, force_regenerate? }
 */
export const prepareSimulation = (data) => {
  return service.post('/api/simulation/prepare', data)
}

/**
 * Query preparation task progress
 * @param {Object} data - { task_id?, simulation_id? }
 */
export const getPrepareStatus = (data) => {
  return service.post('/api/simulation/prepare/status', data)
}

/**
 * Get simulation status
 * @param {string} simulationId
 */
export const getSimulation = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}`)
}

/**
 * Get agent profiles for simulation
 * @param {string} simulationId
 * @param {string} [platform] - 'reddit' | 'twitter' (optional, auto-selected if omitted)
 */
export const getSimulationProfiles = (simulationId, platform) => {
  const params = platform ? { platform } : {}
  return service.get(`/api/simulation/${simulationId}/profiles`, { params })
}

/**
 * Real-time polling for agent profiles during generation
 * @param {string} simulationId
 * @param {string} [platform] - 'reddit' | 'twitter' (optional, auto-selected if omitted)
 */
export const getSimulationProfilesRealtime = (simulationId, platform) => {
  const params = platform ? { platform } : {}
  return service.get(`/api/simulation/${simulationId}/profiles/realtime`, { params })
}

/**
 * Get simulation configuration
 * @param {string} simulationId
 */
export const getSimulationConfig = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/config`)
}

/**
 * Real-time polling for simulation config during generation
 * @param {string} simulationId
 * @returns {Promise}
 */
export const getSimulationConfigRealtime = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/config/realtime`)
}

/**
 * List all simulations
 * @param {string} [projectId] - Optional, filter by project ID
 */
export const listSimulations = (projectId) => {
  const params = projectId ? { project_id: projectId } : {}
  return service.get('/api/simulation/list', { params })
}

/**
 * Start simulation
 * @param {Object} data - { simulation_id, platform?, max_rounds?, enable_graph_memory_update? }
 */
export const startSimulation = (data) => {
  return service.post('/api/simulation/start', data)
}

/**
 * Stop simulation
 * @param {Object} data - { simulation_id }
 */
export const stopSimulation = (data) => {
  return service.post('/api/simulation/stop', data)
}

/**
 * Get real-time simulation runtime status
 * @param {string} simulationId
 */
export const getRunStatus = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/run-status`)
}

/**
 * Get detailed simulation runtime status (including recent actions)
 * @param {string} simulationId
 */
export const getRunStatusDetail = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/run-status/detail`)
}

/**
 * Get posts created in simulation
 * @param {string} simulationId
 * @param {string} [platform] - 'reddit' | 'twitter' (optional, auto-selected if omitted)
 * @param {number} [limit=50] - Result limit
 * @param {number} [offset=0] - Offset
 */
export const getSimulationPosts = (simulationId, platform, limit = 50, offset = 0) => {
  const params = { limit, offset }
  if (platform) params.platform = platform
  return service.get(`/api/simulation/${simulationId}/posts`, { params })
}

/**
 * Get simulation timeline (aggregated by rounds)
 * @param {string} simulationId
 * @param {number} [startRound=0] - Start round
 * @param {number} [endRound=null] - End round
 */
export const getSimulationTimeline = (simulationId, startRound = 0, endRound = null) => {
  const params = { start_round: startRound }
  if (endRound !== null) {
    params.end_round = endRound
  }
  return service.get(`/api/simulation/${simulationId}/timeline`, { params })
}

/**
 * Get agent statistics
 * @param {string} simulationId
 */
export const getAgentStats = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}/agent-stats`)
}

/**
 * Get simulation action history
 * @param {string} simulationId
 * @param {Object} [params={}] - { limit, offset, platform, agent_id, round_num }
 */
export const getSimulationActions = (simulationId, params = {}) => {
  return service.get(`/api/simulation/${simulationId}/actions`, { params })
}

/**
 * Close simulation environment gracefully
 * @param {Object} data - { simulation_id, timeout? }
 */
export const closeSimulationEnv = (data) => {
  return service.post('/api/simulation/close-env', data)
}

/**
 * Get simulation environment status
 * @param {Object} data - { simulation_id }
 */
export const getEnvStatus = (data) => {
  return service.post('/api/simulation/env-status', data)
}

/**
 * Batch interview agents
 * @param {Object} data - { simulation_id, interviews: [{ agent_id, prompt }] }
 */
export const interviewAgents = (data) => {
  return service.post('/api/simulation/interview/batch', data)
}

/**
 * Get simulation history list (with project details)
 * Used for historical projects display
 * @param {number} [limit=20] - Result limit
 */
export const getSimulationHistory = (limit = 20) => {
  return service.get('/api/simulation/history', { params: { limit } })
}
