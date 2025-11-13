# Environment Configuration Guide

## Overview

This application uses environment-specific `.env` files to manage configuration across different deployment environments (development, QA, production).

## How It Works

### 1. Environment Files

The application supports multiple `.env` files:

- `.env.development` - Local development environment
- `.env.qa` - QA/staging environment  
- `.env.production` - Production environment
- `.env` - Default fallback (shared variables)
- `.env.[environment].local` - Local overrides (not committed to git)

### 2. Environment Selection

The environment is determined by the `APP_ENV` or `NODE_ENV` variable:

```fish
# Development (default)
bun nx run @evalio.click/evalio-ui:serve

# QA environment
set -x APP_ENV qa
bun nx run @evalio.click/evalio-ui:serve

# Production build
set -x NODE_ENV production
bun nx run @evalio.click/evalio-ui:build
```

### 3. Variable Injection

Variables from `.env` files are injected at **compile-time** using Rspack's `define` plugin. This means:

- Variables are replaced in the bundle as static strings
- No runtime overhead
- Type-safe access through `config.ts`
- Must rebuild/restart dev server to pick up changes

## Available Variables

Current environment variables:

- `PUBLIC_URL` - Base URL for the application
- `AUTH_URL` - Authentication service URL
- `NODE_ENV` - Current environment (development/production)

## Usage in Code

Import the config object in your components:

```typescript
import { config } from '@/config/config';

// Use the variables
const response = await axios.get(`${config.AUTH_URL}/login`);
console.log('App running on:', config.PUBLIC_URL);
```

## Best Practices

### 1. Never Commit Secrets

Add to `.gitignore`:
```
.env.local
.env.*.local
.env.development.local
.env.qa.local
.env.production.local
```

### 2. Use Environment-Specific Files

- ✅ `.env.development` - Non-sensitive dev defaults
- ✅ `.env.qa` - QA configuration
- ✅ `.env.production` - Production URLs (no secrets)
- ❌ `.env` - Avoid for environment-specific values

### 3. Restart After Changes

Environment variables are injected at build time. After changing `.env` files:

```fish
# Restart dev server
bun nx run @evalio.click/evalio-ui:serve

# Or rebuild
bun nx run @evalio.click/evalio-ui:build
```

### 4. Type Safety

Add new variables to `config.ts`:

```typescript
type Config = {
  PUBLIC_URL: string;
  AUTH_URL: string;
  NEW_VARIABLE: string;  // Add here
}

export const config: Config = {
  PUBLIC_URL: getEnv('PUBLIC_URL', ''),
  AUTH_URL: getEnv('AUTH_URL', ''),
  NEW_VARIABLE: getEnv('NEW_VARIABLE', 'default-value'),
};
```

## Deployment

### Development
```fish
bun nx run @evalio.click/evalio-ui:serve
```
Loads `.env.development`

### QA Deployment
```fish
set -x APP_ENV qa
bun nx run @evalio.click/evalio-ui:build
```
Loads `.env.qa`

### Production Deployment
```fish
set -x NODE_ENV production
bun nx run @evalio.click/evalio-ui:build
```
Loads `.env.production`

## Troubleshooting

### Variables not loading?

1. Check the file exists: `ls apps/evalio-ui/.env.development`
2. Verify the environment: `echo $APP_ENV` or `echo $NODE_ENV`
3. Restart dev server (Ctrl+C and rerun)
4. Check console for `[rspack] Loaded environment from:` message

### Wrong values in browser?

1. Open browser console
2. Look for `[config] Environment configuration loaded:`
3. Verify the loaded values match your `.env` file
4. If not, rebuild/restart the dev server

### Type errors?

Make sure variables are defined in `config.ts` Config type and exported in the config object.

## Security Notes

- ⚠️ **Never store sensitive secrets** (API keys, passwords) in `.env` files that are committed to git
- ✅ Use environment variables on your CI/CD platform for secrets
- ✅ Use `.env.local` files for local development secrets
- ✅ Add `*.local` to `.gitignore`
