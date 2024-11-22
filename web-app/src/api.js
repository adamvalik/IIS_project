import axios from 'axios';
import store from './auth';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL || 'http://localhost:8000',
});


//Define an interceptor to add the Authorization header to all requests
apiClient.interceptors.request.use(config => {
  const token = store.state.accessToken;
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default apiClient;
