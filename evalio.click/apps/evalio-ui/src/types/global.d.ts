declare module '@/*' {
  const value: Record<string, unknown>
  export default value
}

declare module '*.json' {
  const value: Record<string, unknown>
  export default value
}

// Specific declaration for the runtime config module so named imports like
// `import { config } from '@/config/config'` resolve during type checking.
declare module '@/config/config' {
  export const config: Record<string, string>
  export default config
}
