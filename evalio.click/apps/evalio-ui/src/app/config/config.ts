// Environment configuration
// Variables are injected at compile-time via rspack's define plugin
// from environment-specific .env files (.env.development, .env.qa, .env.production)

type Config = {
  PUBLIC_URL: string;
  NODE_ENV: string;
}

// Direct access to process.env so rspack's define plugin can replace them
// These will be replaced at compile-time with actual string values
const PUBLIC_URL = process.env.PUBLIC_URL || '';
const NODE_ENV = process.env.NODE_ENV || 'development';


export const config: Config = {
  PUBLIC_URL: PUBLIC_URL || (typeof window !== 'undefined' ? window.location.origin : ''),
  NODE_ENV: NODE_ENV,
};


export default config;
