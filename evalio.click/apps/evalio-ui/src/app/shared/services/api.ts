import axios from 'axios';
import { config } from '@/config/config';

const base = config?.PUBLIC_URL || '';
const api = axios.create({ baseURL: base });

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
