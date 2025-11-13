import { config } from '@/config/config';
import api from '../../../shared/services/api';

export type AuthResponse = {
  token: string;
  expires_at: string;
};

export const login = async (email: string, password: string) => {
  const { data } = await api.post<AuthResponse>(`${config.PUBLIC_URL}/public/login`, {
    email,
    password,
  });
  return data;
};

export const signup = async (email: string, password: string) => {
  return await api.post(`${config.PUBLIC_URL}/signup`, { email, password });
};
