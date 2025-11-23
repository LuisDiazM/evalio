import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '@/shared/services/auth-service';

interface RequireAuthProps {
  children: React.ReactElement | null;
}

export default function RequireAuth({ children }: RequireAuthProps) {
  const [checking, setChecking] = useState(true);
  const [ok, setOk] = useState(false);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const valid = await isAuthenticated();
        if (mounted) {
          setOk(valid);
        }
      } catch {
        if (mounted) setOk(false);
      } finally {
        if (mounted) setChecking(false);
      }
    })();

    return () => {
      mounted = false;
    };
  }, []);

  if (checking) return null; // or a small spinner component

  if (!ok) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
