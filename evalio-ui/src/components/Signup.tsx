import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { config } from '../config/config';

const SIGNUP_URL = `${config.PUBLIC_URL}/signup`;

const Signup: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (password !== confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }
    setLoading(true);
    try {
      const response = await fetch(SIGNUP_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, name }),
      });
      const data = await response.json();
      if (response.status == 201) {
        navigate('/groups');
      } else {
        setError(data.message || 'Error al registrar');
      }
    } catch {
      setError('Error de red');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <nav style={{ height: 60, display: 'flex', alignItems: 'center', borderBottom: '1px solid #eee', padding: '0 24px' }}>
        <span style={{ fontWeight: 700, fontSize: 22, display: 'flex', alignItems: 'center' }}>
          <span style={{ marginRight: 8, fontSize: 24 }}>▮</span> Evalio
        </span>
      </nav>
      <form onSubmit={handleSubmit} style={{ maxWidth: 480, margin: '64px auto 0', width: '100%' }}>
        <h2 style={{ textAlign: 'center', fontWeight: 700, fontSize: 32, marginBottom: 32 }}>Registrarse</h2>
        <div style={{ marginBottom: 24 }}>
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="Nombre completo"
            required
            style={{ width: '100%', padding: '14px 16px', borderRadius: 8, border: '1px solid #e5e7eb', fontSize: 16 }}
          />
        </div>
        <div style={{ marginBottom: 24 }}>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="myemail@example.com"
            required
            style={{ width: '100%', padding: '14px 16px', borderRadius: 8, border: '1px solid #e5e7eb', fontSize: 16 }}
          />
        </div>
        <div style={{ marginBottom: 24 }}>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="mysecretpassword"
            required
            style={{ width: '100%', padding: '14px 16px', borderRadius: 8, border: '1px solid #e5e7eb', fontSize: 16 }}
          />
        </div>
        <div style={{ marginBottom: 24 }}>
          <input
            type="password"
            value={confirmPassword}
            onChange={e => setConfirmPassword(e.target.value)}
            placeholder="Confirmar contraseña"
            required
            style={{ width: '100%', padding: '14px 16px', borderRadius: 8, border: '1px solid #e5e7eb', fontSize: 16 }}
          />
        </div>
        {error && <div style={{ color: 'red', marginBottom: 16, textAlign: 'center' }}>{error}</div>}
        <button
          type="submit"
          disabled={loading}
          style={{ width: '50%', padding: '14px 0', borderRadius: 12, background: '#e5eefb', color: '#222', fontWeight: 600, fontSize: 18, border: 'none', cursor: loading ? 'not-allowed' : 'pointer' }}
        >
          {loading ? 'Registrando...' : 'Registrarse'}
        </button>
        <div style={{ textAlign: 'right', marginTop: 16 }}>
          <a href="/login" style={{ color: '#6b7280', fontSize: 15, textDecoration: 'underline' }}>Ya tiene una cuenta? Ingresar</a>
        </div>
      </form>
    </div>
  );
};

export default Signup; 