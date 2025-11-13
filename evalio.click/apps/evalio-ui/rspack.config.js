const { NxAppRspackPlugin } = require('@nx/rspack/app-plugin');
const { NxReactRspackPlugin } = require('@nx/rspack/react-plugin');
const { DefinePlugin } = require('@rspack/core');
const { join } = require('path');
const dotenv = require('dotenv');
const { existsSync } = require('fs');

// Determine which .env file to load based on NODE_ENV or APP_ENV
// Priority: .env.[APP_ENV] > .env.[NODE_ENV] > .env
function loadEnvironmentVariables() {
  const appEnv = process.env.APP_ENV || process.env.NODE_ENV || 'development';

  // List of possible .env files in priority order
  const envFiles = [
    join(__dirname, `.env.${appEnv}`),
    join(__dirname, `.env.${appEnv}.local`),
    join(__dirname, '.env'),
  ];

  let loadedEnv = {};

  // Load each existing file (later files override earlier ones)
  for (const envFile of envFiles) {
    if (existsSync(envFile)) {
      const result = dotenv.config({ path: envFile });
      if (result.parsed) {
        loadedEnv = { ...loadedEnv, ...result.parsed };
        console.log(`[rspack] Loaded environment from: ${envFile}`);
      }
    }
  }

  return loadedEnv;
}

// Build the define object for compile-time variable injection
function buildDefinePlugin() {
  const env = loadEnvironmentVariables();
  const defines = {};

  // Inject NODE_ENV
  defines['process.env.NODE_ENV'] = JSON.stringify(process.env.NODE_ENV || 'development');

  // Inject all variables from .env files
  for (const [key, value] of Object.entries(env)) {
    defines[`process.env.${key}`] = JSON.stringify(value);
    console.log(`[rspack] Injecting process.env.${key} = ${JSON.stringify(value)}`);
  }

  console.log('[rspack] Total defines injected:', Object.keys(defines).length);
  return defines;
}

module.exports = {
  output: {
    path: join(__dirname, 'dist'),
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
    new DefinePlugin(buildDefinePlugin()),
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
  ],
};
