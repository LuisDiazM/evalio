type Config = {
  PUBLIC_URL: string;
  NODE_ENV: string;
  FORWARD_SERVICE_URL: string;
  USERS_SERVICE_URL: string;
  ADMIN_SERVICE_URL: string;
};

const PUBLIC_URL = process.env.PUBLIC_URL || '';
const NODE_ENV = process.env.NODE_ENV || 'development';
const FORWARD_URL = process.env.FORWARD_SERVICE_URL || '';
const USERS_URL = process.env.USERS_SERVICE_URL || '';
const ADMIN_URL = process.env.ADMIN_SERVICE_URL || '';

export const config: Config = {
  PUBLIC_URL: PUBLIC_URL,
  NODE_ENV: NODE_ENV,
  FORWARD_SERVICE_URL: FORWARD_URL,
  USERS_SERVICE_URL: USERS_URL,
  ADMIN_SERVICE_URL: ADMIN_URL,
};

export default config;
