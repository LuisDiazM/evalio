import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { config } from '../config/config';

const LOGIN_URL = `${config.PUBLIC_URL}/login`;

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await fetch(LOGIN_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (response.ok && data.token) {
        localStorage.setItem('access_token', data.token);
        navigate('/groups');
      } else {
        setError('Invalid credentials');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <nav style={{ height: 60, display: 'flex', alignItems: 'center', padding: '0 24px' }}>
        <span style={{ fontWeight: 700, fontSize: 22, display: 'flex', alignItems: 'center' }}>
          <span style={{ marginRight: 8, fontSize: 24 }}>▮</span> Evalio
        </span>
      </nav>
      <form onSubmit={handleSubmit} style={{ maxWidth: 480, margin: '64px auto 0', width: '100%' }}>
        <h2 style={{ textAlign: 'center', fontWeight: 700, fontSize: 32, marginBottom: 32 }}>Ingrese a su cuenta</h2>
        <div style={{ marginBottom: 24 }}>
          <label htmlFor="email" style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="myemail@example.com"
            required
            style={{ width: '100%', padding: '14px 16px', borderRadius: 8, border: '1px solid #e5e7eb', fontSize: 16 }}
          />
        </div>
        <div style={{ marginBottom: 8 }}>
          <label htmlFor="password" style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>Contraseña</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
            style={{ width: '100%', padding: '14px 16px', borderRadius: 8, border: '1px solid #e5e7eb', fontSize: 16 }}
          />
        </div>
        <div style={{ marginBottom: 24 }}>
          <a href="#" style={{ color: '#6b7280', fontSize: 14, textDecoration: 'underline' }}>¿Olvidó su contraseña?</a>
        </div>
        {error && <div style={{ color: 'red', marginBottom: 16, textAlign: 'center' }}>{error}</div>}
        <button
          type="submit"
          disabled={loading}
          style={{ width: '50%', padding: '14px 0', borderRadius: 12, background: '#e5eefb', color: '#222', fontWeight: 600, fontSize: 18, border: 'none', cursor: loading ? 'not-allowed' : 'pointer' }}
        >
          {loading ? 'Ingresando...' : 'Ingresar'}
        </button>
      
      <div style={{textAlign:"right"}}>

      <a href="/signup" style={{ color: '#6b7280', fontSize: 15, textDecoration: 'underline' }}>No tiene una cuenta? Registrarse</a>
      </div>
      </form>


    </div>
  );
};

export default Login; 