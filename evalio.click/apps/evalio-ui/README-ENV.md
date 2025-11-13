# 🚀 Quick Start - Multi-Environment Setup

## Environment Files Created

✅ `.env.development` - Local development (localhost)
✅ `.env.qa` - QA/Staging environment
✅ `.env.production` - Production environment
✅ `.env` - Shared/fallback configuration

## Running Different Environments

### Development (default)
```fish
bun nx run @evalio.click/evalio-ui:serve
```
Loads: `.env.development` → `.env`

### QA Environment
```fish
set -x APP_ENV qa
bun nx run @evalio.click/evalio-ui:serve
```
Loads: `.env.qa` → `.env`

### Production Build
```fish
set -x NODE_ENV production
bun nx run @evalio.click/evalio-ui:build
```
Loads: `.env.production` → `.env`

## Usage in Code

```typescript
import { config } from '@/config/config';

// Access environment variables
console.log(config.PUBLIC_URL);  // Type-safe!
console.log(config.AUTH_URL);
console.log(config.NODE_ENV);
```

## Verification

After starting the dev server, check:

1. **Terminal output** - Should see:
   ```
   [rspack] Loaded environment from: .../apps/evalio-ui/.env.development
   ```

2. **Browser console** - Should see (in development):
   ```
   [config] Environment configuration loaded: {
     PUBLIC_URL: "http://localhost:5000",
     AUTH_URL: "http://localhost:3000/auth",
     NODE_ENV: "development"
   }
   ```

## File Watcher Issue?

If you see `ENOSPC: System limit for number of file watchers reached`:

```fish
./fix-file-watchers.fish
```

This increases the system limit for file watchers.

## 📚 Full Documentation

See [ENV_SETUP.md](./ENV_SETUP.md) for complete documentation including:
- How to add new variables
- Security best practices
- Deployment strategies
- Troubleshooting guide

## Adding New Variables

1. Add to your `.env.*` files:
   ```properties
   NEW_API_URL=https://api.example.com
   ```

2. Update `src/app/config/config.ts`:
   ```typescript
   type Config = {
     PUBLIC_URL: string;
     AUTH_URL: string;
     NEW_API_URL: string;  // Add here
   }

   export const config: Config = {
     PUBLIC_URL: getEnv('PUBLIC_URL', ''),
     AUTH_URL: getEnv('AUTH_URL', ''),
     NEW_API_URL: getEnv('NEW_API_URL', ''),  // Add here
   };
   ```

3. Restart dev server to pick up changes

## Security

⚠️ **Never commit sensitive secrets to git!**

Use `.env.*.local` files for local secrets (already in `.gitignore`):

```fish
# Create local override
echo 'API_KEY=secret-key-here' > .env.development.local
```
