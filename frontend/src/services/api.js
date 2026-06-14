import axios from 'axios';

const isProd = import.meta.env.PROD;
const baseURL = isProd ? 'https://ai-incident-investigation-copilot.onrender.com/api' : '/api';

// The Vite server proxy forwards /api calls to http://localhost:8000
const API = axios.create({
  baseURL,
  timeout: 25000, // Multi-agent execution and RAG lookups can take a few seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

export const runInvestigation = async (payload) => {
  const response = await API.post('/investigate', payload);
  return response.data;
};

export const getIncidentHistory = async () => {
  const response = await API.get('/history');
  return response.data;
};  

export const getIncidentDetails = async (incidentId) => {
  const response = await API.get(`/investigation/${incidentId}`);
  return response.data;
};

export const listKBDocs = async () => {
  const response = await API.get('/incidents/kb');
  return response.data;
};

export const addKBDoc = async (payload) => {
  const response = await API.post('/incidents/kb', payload);
  return response.data;
};

export const getSystemHealth = async () => {
  const response = await API.get('/health');
  return response.data;
};

export default API;
