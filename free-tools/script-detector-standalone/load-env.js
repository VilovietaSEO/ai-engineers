/**
 * Simple .env file loader (no dependencies)
 * Loads environment variables from .env file
 */

const fs = require('fs');
const path = require('path');

function loadEnv() {
  const envPath = path.join(__dirname, '.env');

  // Check if .env file exists
  if (!fs.existsSync(envPath)) {
    console.log('ℹ️  No .env file found. Enhanced detection disabled.');
    console.log('   To enable: cp .env.example .env and add your Browserless API key');
    return;
  }

  // Read and parse .env file
  const envFile = fs.readFileSync(envPath, 'utf8');
  const lines = envFile.split('\n');

  for (const line of lines) {
    // Skip comments and empty lines
    if (line.trim().startsWith('#') || !line.trim()) {
      continue;
    }

    // Parse KEY=VALUE format
    const match = line.match(/^\s*([A-Z_]+)\s*=\s*(.*)$/);
    if (match) {
      const [, key, value] = match;
      process.env[key] = value.trim();
    }
  }

  if (process.env.BROWSERLESS_API_KEY && process.env.BROWSERLESS_API_KEY !== 'your_api_key_here') {
    console.log('✅ Browserless API key loaded - Enhanced detection enabled');
  }
}

module.exports = { loadEnv };
