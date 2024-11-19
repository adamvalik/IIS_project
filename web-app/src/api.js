import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL || 'http://localhost:8000',
});

export default apiClient;
