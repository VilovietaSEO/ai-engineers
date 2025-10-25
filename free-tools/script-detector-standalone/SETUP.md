# Setup Guide - Script Detector

## Basic Setup (No API Key Required)

The script detector works **without any API key** for static HTML analysis. Just run:

```bash
node example.js
```

This will detect 100+ technologies from static HTML/JavaScript code.

## Enhanced Setup (Optional - For Dynamic Pixel Detection)

To detect pixels loaded dynamically via Google Tag Manager, you'll need a Browserless API key.

### Step 1: Get Browserless API Key

1. Go to https://www.browserless.io/
2. Sign up for an account (free trial available)
3. Get your API key from the dashboard
4. Pricing: ~$5/month for 2,000 requests (~$0.003 per analysis)

### Step 2: Configure Your API Key

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your key
nano .env
```

Your `.env` file should look like:
```bash
BROWSERLESS_API_KEY=your_actual_api_key_here
```

### Step 3: Verify Setup

```bash
node example.js 3
```

You should see: `✅ Browserless API key loaded - Enhanced detection enabled`

## Security Notes

✅ **Safe:**
- `.env` file is already in `.gitignore`
- Your API key will **NOT** be committed to git
- The `.env.example` only shows the template

❌ **Never:**
- Never commit your actual `.env` file
- Never put your API key directly in code
- Never share your `.env` file publicly

## Usage in Your Code

### Option 1: Using load-env.js (Recommended)

```javascript
const { loadEnv } = require('./load-env');
loadEnv(); // Loads .env automatically

const { analyzeAndSave } = require('./src/index');

await analyzeAndSave('https://example.com', {
  browserlessApiKey: process.env.BROWSERLESS_API_KEY
});
```

### Option 2: Direct Environment Variable

```javascript
const { analyzeAndSave } = require('./src/index');

// Pass API key from environment
await analyzeAndSave('https://example.com', {
  browserlessApiKey: process.env.BROWSERLESS_API_KEY
});
```

### Option 3: No Enhanced Detection

```javascript
const { analyzeAndSave } = require('./src/index');

// Works without API key - static analysis only
await analyzeAndSave('https://example.com');
```

## What's the Difference?

### Without Browserless (Free)
- Detects tools embedded in HTML source
- Fast and reliable
- No cost
- Works for most websites

### With Browserless (Enhanced)
- Everything above, plus:
- Detects pixels loaded via GTM
- Captures network requests
- Analyzes cookies
- Better for JavaScript-heavy sites
- ~$0.003 per analysis

## Troubleshooting

### "No .env file found"
This is normal if you haven't set up enhanced detection. The tool will still work with static analysis.

### "Browserless API request failed"
- Check your API key is correct in `.env`
- Verify you have credits in your Browserless account
- Check your internet connection

### API key still being exposed
- Make sure `.env` is listed in `.gitignore`
- Run `git status` and verify `.env` is not tracked
- Never use `.env.example` for real keys

## Alternative: System Environment Variables

Instead of using `.env`, you can set environment variables in your system:

```bash
# Linux/Mac
export BROWSERLESS_API_KEY=your_key_here
node example.js

# Windows
set BROWSERLESS_API_KEY=your_key_here
node example.js
```

This is more secure for production environments.
