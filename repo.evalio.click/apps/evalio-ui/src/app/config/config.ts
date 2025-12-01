type Config = {
  PUBLIC_URL: string;
  NODE_ENV: string;
}

const PUBLIC_URL = process.env.PUBLIC_URL || '';
const NODE_ENV = process.env.NODE_ENV || 'development';


export const config: Config = {
  PUBLIC_URL: PUBLIC_URL,
  NODE_ENV: NODE_ENV,
};


export default config;
