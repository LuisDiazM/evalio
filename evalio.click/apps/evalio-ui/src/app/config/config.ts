// Config object built from environment variables.
// Prioritize runtime sources appropriate for an NX monorepo using Bun and rspack:
// 1) process.env (Bun/Node), 2) globalThis.__ENV__ (server-injected at runtime),
// 3) import.meta.env (rspack compile-time) as a last resort.

type Config = {
  PUBLIC_URL: string
  AUTH_URL: string
}

const getEnv = (key: string, fallback = ''): string => {
  // 1) Build-time injected process.env (rspack define plugin replaces these at compile time)
  try {
    if (typeof process !== 'undefined' && process.env) {
      const value = process.env[key];
      if (value !== undefined) {
        return String(value);
      }
    }
  } catch {
    // process not available
  }
  // 2) Runtime fallback for development - use location origin for PUBLIC_URL
  if (key === 'PUBLIC_URL' && typeof window !== 'undefined' && window.location) {
    return window.location.origin;
  }

  return fallback;
}

export const config: Config = {
  // Prefer PUBLIC_URL, fallback to VITE_REACT_PUBLIC_URL for compatibility
  PUBLIC_URL: getEnv('PUBLIC_URL', getEnv('VITE_REACT_PUBLIC_URL', '')),
  AUTH_URL: getEnv('AUTH_URL', ''),
}

export default config;
