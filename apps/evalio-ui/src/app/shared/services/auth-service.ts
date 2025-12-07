import { jwtDecode } from 'jwt-decode';
import axios from 'axios';
import { config } from '@/config/config';

interface DecodedToken {
  exp: number;
  email: string;
  name: string;
}

export const isTokenValid = (token: string): boolean => {
  try {
    const decoded = jwtDecode<DecodedToken>(token);
    const currentTime = Date.now() / 1000;
    return decoded.exp > currentTime;
  } catch {
    return false;
  }
};

export const verifyTokenWithBackend = async (token: string): Promise<boolean> => {
  try {
    const response = await axios.get(`${config.FORWARD_SERVICE_URL}/auth`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      validateStatus: () => true,
    })

    return response.status >= 200 && response.status < 300
  } catch {
    return false;
  }
};

export const isAuthenticated = async (): Promise<boolean> => {
  const token = localStorage.getItem('access_token');
  if (!token) return false;

  // Verificar si el token es válido localmente
  if (!isTokenValid(token)) {
    localStorage.removeItem('access_token');
    return false;
  }

  // Verificar el token con el backend
  const isValid = await verifyTokenWithBackend(token);
  if (!isValid) {
    localStorage.removeItem('access_token');
    return false;
  }

  return true;
};
