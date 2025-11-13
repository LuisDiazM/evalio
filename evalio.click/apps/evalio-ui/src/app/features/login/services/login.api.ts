import { config } from '@/config/config';
import api from '../../../shared/services/api';

export const login = async (email: string, password: string) => {
  return await api.post(`${config.PUBLIC_URL}/login`, { email, password });
};

export const signup = async (email: string, password: string) => {
  return await api.post(`${config.PUBLIC_URL}/signup`, { email, password });
};
