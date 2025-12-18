const { NxAppRspackPlugin } = require('@nx/rspack/app-plugin');
const { NxReactRspackPlugin } = require('@nx/rspack/react-plugin');
const { join, resolve } = require('path');
const rspack = require('@rspack/core');
const fs = require('fs');
const dotenv = require('dotenv');
// Load environment variables from .env files in the monorepo
function loadEnvFiles() {
  const repoRoot = resolve(__dirname, '../../');
  const appDir = __dirname;
  // Load in order of precedence (later files override earlier ones)
  const envFiles = [
    join(repoRoot, '.env'),
    join(repoRoot, '.env.local'),
    join(appDir, '.env'),
    join(appDir, '.env.local'),
    join(appDir, '.env.prod'),
  ];
  const env = {};
  for (const file of envFiles) {
    if (fs.existsSync(file)) {
      const result = dotenv.config({ path: file });
      if (result.parsed) {
        Object.assign(env, result.parsed);
      }
    }
  }
  return env;
}
// Build DefinePlugin definitions to inject into process.env
function buildProcessEnvDefinitions(envVars) {
  const definitions = {};
  // Inject all loaded env vars into process.env
  for (const key of Object.keys(envVars)) {
    definitions[`process.env.${key}`] = JSON.stringify(envVars[key]);
  }
  // Also preserve NODE_ENV from the actual process.env
  if (process.env.NODE_ENV) {
    definitions['process.env.NODE_ENV'] = JSON.stringify(process.env.NODE_ENV);
  }
  return definitions;
}
const envVars = loadEnvFiles();
module.exports = {
  entry: {
    main: join(__dirname, 'src/main.tsx'),
  },
  output: {
    path: join(__dirname, '../../dist/apps/evalio-ui'),
  },
  resolve: {
    alias: {
      '@': join(__dirname, 'src/app'),
    },
  },
  devServer: {
    port: 5000,
    historyApiFallback: {
      index: '/index.html',
      disableDotRule: true,
      htmlAcceptHeaders: ['text/html', 'application/xhtml+xml'],
    },
  },
  plugins: [
    new NxAppRspackPlugin({
      tsConfig: './tsconfig.app.json',
      main: './src/main.tsx',
      index: './src/index.html',
      baseHref: '/',
      assets: ['./src/favicon.ico', './src/assets'],
      styles: ['./src/styles.scss'],
      outputHashing: process.env['NODE_ENV'] === 'production' ? 'all' : 'none',
      optimization: process.env['NODE_ENV'] === 'production',
    }),
    new NxReactRspackPlugin({
      // Uncomment this line if you don't want to use SVGR
      // See: https://react-svgr.com/
      // svgr: false
    }),
    new rspack.DefinePlugin(buildProcessEnvDefinitions(envVars)),
  ],
};
