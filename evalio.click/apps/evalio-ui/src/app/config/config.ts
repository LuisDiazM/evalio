// Config object built from environment variables.
// Prioritize runtime sources appropriate for an NX monorepo using Bun and rspack:
// 1) process.env (Bun/Node), 2) globalThis.__ENV__ (server-injected at runtime),
// 3) import.meta.env (rspack compile-time) as a last resort.

type Config = {
  PUBLIC_URL: string
  AUTH_URL: string
}

const getEnv = (key: string, fallback = ''): string => {
  // 1) process.env (Bun / Node)
  const maybeProcess = globalThis as unknown as { process?: { env?: Record<string, string | undefined> } }
  if (maybeProcess.process?.env && typeof maybeProcess.process.env[key] !== 'undefined') {
    return String(maybeProcess.process.env[key])
  }

  // 2) runtime-injected global (e.g., window.__ENV__ or globalThis.__ENV__)
  const maybeGlobalEnv = globalThis as unknown as { __ENV__?: Record<string, string | undefined> }
  if (maybeGlobalEnv.__ENV__ && typeof maybeGlobalEnv.__ENV__[key] !== 'undefined') {
    return String(maybeGlobalEnv.__ENV__[key])
  }

  // 3) import.meta.env (bundle-time replacements like rspack support)
  try {
    const meta = (import.meta as unknown as { env?: Record<string, unknown> }).env
    if (meta && typeof meta[key] !== 'undefined') return String(meta[key])
  } catch {
    // ignore if import.meta is not available in this runtime
  }

  return fallback
}

export const config: Config = {
  // Prefer PUBLIC_URL, fallback to VITE_REACT_PUBLIC_URL for compatibility
  PUBLIC_URL: getEnv('PUBLIC_URL', getEnv('VITE_REACT_PUBLIC_URL', '')),
  AUTH_URL: getEnv('AUTH_URL', ''),
}

export default config;
