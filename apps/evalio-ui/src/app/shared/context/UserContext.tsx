import React, { createContext, useContext, useEffect, useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import { isTokenValid } from '@/shared/services/auth-service';

type User = {
  name: string;
  email: string;
  professor_id?: string;
};

type UserContextValue = {
  user: User | null;
  setUserFromToken: (token: string) => void;
  logout: () => void;
};

const UserContext = createContext<UserContextValue | undefined>(undefined);

const tokenKey = 'access_token';

const decodeToUser = (token: string): User | null => {
  try {
    // decode payload and map fields
    const decoded = jwtDecode<Record<string, unknown>>(token);
    const name = String(decoded?.name ?? '');
    const email = String(decoded?.email ?? '');
    const professor_id = (decoded?.professor_id ?? decoded?.professorId) as string | undefined;
    return { name, email, professor_id };
  } catch (err) {
    console.debug('Invalid token for decoding user', err);
    return null;
  }
};

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const setUserFromToken = (token: string) => {
    if (!token) return;
    try {
      if (!isTokenValid(token)) {
        console.warn('Token invalid when trying to set user');
        return;
      }
    } catch (err) {
      console.debug('isTokenValid failed', err);
    }
    const u = decodeToUser(token);
    if (u) {
      setUser(u);
      try {
        localStorage.setItem(tokenKey, token);
      } catch (err) {
        console.debug('localStorage set failed', err);
      }
    }
  };

  const logout = () => {
    setUser(null);
    try {
      localStorage.removeItem(tokenKey);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    try {
      const token = localStorage.getItem(tokenKey);
      if (token && isTokenValid(token)) {
        const u = decodeToUser(token);
        if (u) setUser(u);
      }
    } catch (err) {
      console.debug('hydrate user failed', err);
    }
  }, []);

  return <UserContext.Provider value={{ user, setUserFromToken, logout }}>{children}</UserContext.Provider>;
};

export const useUser = (): UserContextValue => {
  const ctx = useContext(UserContext);
  if (!ctx) throw new Error('useUser must be used within UserProvider');
  return ctx;
};

export default UserContext;
