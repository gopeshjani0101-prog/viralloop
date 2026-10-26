import axios from 'axios';

const API_BASE = '/api';

export const api = {
  // Pipeline
  getPipelineStatus: async () => {
    const res = await axios.get(`${API_BASE}/pipeline/status`);
    return res.data;
  },
  triggerPipelineRun: async (topic = null) => {
    const res = await axios.post(`${API_BASE}/pipeline/run`, { topic });
    return res.data;
  },
  startAutonomous: async (interval_seconds = 120) => {
    const res = await axios.post(`${API_BASE}/pipeline/autonomous/start`, { interval_seconds });
    return res.data;
  },
  stopAutonomous: async () => {
    const res = await axios.post(`${API_BASE}/pipeline/autonomous/stop`);
    return res.data;
  },

  // Videos
  getVideos: async () => {
    const res = await axios.get(`${API_BASE}/videos`);
    return res.data.videos || [];
  },
  getVideo: async (id) => {
    const res = await axios.get(`${API_BASE}/videos/${id}`);
    return res.data;
  },

  // Analytics
  getAnalyticsOverview: async () => {
    const res = await axios.get(`${API_BASE}/analytics/overview`);
    return res.data;
  },
  refreshAnalytics: async () => {
    const res = await axios.post(`${API_BASE}/analytics/refresh`);
    return res.data;
  },

  // Learning Insights
  getLearningInsights: async () => {
    const res = await axios.get(`${API_BASE}/learning/insights`);
    return res.data.insights || [];
  },

  // Settings
  getSettings: async () => {
    const res = await axios.get(`${API_BASE}/settings`);
    return res.data;
  },
  updateSettings: async (settingsData) => {
    const res = await axios.post(`${API_BASE}/settings`, settingsData);
    return res.data;
  }
};
