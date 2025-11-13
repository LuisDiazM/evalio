// Environment configuration
// Variables are injected at compile-time via rspack's define plugin
// from environment-specific .env files (.env.development, .env.qa, .env.production)

type Config = {
  PUBLIC_URL: string;
  AUTH_URL: string;
  NODE_ENV: string;
}

// Direct access to process.env so rspack's define plugin can replace them
// These will be replaced at compile-time with actual string values
const PUBLIC_URL = process.env.PUBLIC_URL || '';
const AUTH_URL = process.env.AUTH_URL || '';
const NODE_ENV = process.env.NODE_ENV || 'development';

// Debug logging
console.log('[config] Raw process.env values:');
console.log('  process.env.PUBLIC_URL =', process.env.PUBLIC_URL, `(type: ${typeof process.env.PUBLIC_URL})`);
console.log('  process.env.AUTH_URL =', process.env.AUTH_URL, `(type: ${typeof process.env.AUTH_URL})`);
console.log('  process.env.NODE_ENV =', process.env.NODE_ENV, `(type: ${typeof process.env.NODE_ENV})`);

export const config: Config = {
  PUBLIC_URL: PUBLIC_URL || (typeof window !== 'undefined' ? window.location.origin : ''),
  AUTH_URL: AUTH_URL,
  NODE_ENV: NODE_ENV,
};

// Log final configuration (only in development)
console.log('[config] Final environment configuration:', {
  PUBLIC_URL: config.PUBLIC_URL,
  AUTH_URL: config.AUTH_URL,
  NODE_ENV: config.NODE_ENV,
});

export default config;
