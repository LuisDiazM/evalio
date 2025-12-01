import { config } from '@/config/config';
import api from '../../../shared/services/api';

export type AuthResponse = {
  token: string;
  expires_at: string;
};

export const login = async (email: string, password: string) => {
  console.log('Public URL:', config.PUBLIC_URL);
  const { data } = await api.post<AuthResponse>(
    `${config.PUBLIC_URL}/public/login`,
    {
      email,
      password,
    }
  );
  return data;
};

export type SignUpRequest = {
  email: string;
  password: string;
  name: string;
};

export const signup = async (
  email: string,
  password: string,
  fullName: string
) => {
  const signupData: SignUpRequest = { email, password, name: fullName };
  const { status } = await api.post(
    `${config.PUBLIC_URL}/public/signup`,
    signupData
  );
  return  status ;
};
