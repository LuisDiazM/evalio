import axios from 'axios';
import { config } from '../config/config';

const api = axios.create({
  baseURL: config.MANAGER_URL,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    config.headers['Professor-Id'] = '123412341234';
    config.headers['Professor-Name'] = 'Ingri Rojas';
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
