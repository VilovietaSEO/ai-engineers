# Script Detector - Standalone Backend Package

A powerful, backend-only website technology detection tool that analyzes websites to detect their analytics, marketing tools, CMS, tracking pixels, and tech stack. Results are automatically saved as formatted markdown reports.

## Features

- 🔍 **Comprehensive Detection**: Detects 100+ technologies including:
  - Analytics: Google Analytics 4, GTM, Microsoft Clarity, Search Console
  - Marketing: Facebook Pixel, LinkedIn Insight, TikTok, Twitter, Pinterest, etc.
  - CRM: HubSpot, Salesforce, Marketo, Zoho, Pipedrive
  - Email Marketing: Mailchimp, Klaviyo, ActiveCampaign, ConvertKit
  - CMS: WordPress, Shopify, Webflow, Wix, Squarespace
  - Conversion Tools: Hotjar, Optimizely, VWO, FullStory, Segment
  - Chat Widgets: Intercom, Drift, Zendesk, Tawk.to, Crisp

- 📝 **Automatic Markdown Reports**: Generates professional, readable reports
- 🚀 **Backend-Only**: No frontend dependencies, runs in Node.js
- 🔧 **Flexible**: Use as module in your code or run standalone
- 📊 **Batch Processing**: Analyze multiple websites at once
- ⚡ **Optional Enhanced Detection**: Integrate with Browserless for JavaScript-based pixel detection

## Installation

1. Copy the entire `script-detector-standalone` folder to your project
2. No dependencies required! Uses native Node.js (v18+)

```bash
# Optional: For enhanced detection with Browserless
npm install
# Then set BROWSERLESS_API_KEY environment variable
```

## Quick Start

### Basic Usage

```javascript
const { analyzeAndSave } = require('./script-detector-standalone/src/index');

// Analyze a website and save markdown report
await analyzeAndSave('https://example.com', {
  outputDir: './reports',
  includeJson: true  // Also save raw JSON data
});
```

### Run Example

```bash
node example.js
```

This will analyze example.com and save a markdown report to `./reports/`

## Usage Examples

### 1. Analyze Single Website

```javascript
const { analyzeAndSave } = require('./src/index');

const result = await analyzeAndSave('https://github.com', {
  outputDir: './reports',
  filename: 'github-analysis',  // Custom filename
  includeJson: true
});

console.log('Report saved to:', result.files.markdown);
```

### 2. Programmatic Usage (No File Output)

```javascript
const { analyzeWebsite } = require('./src/index');

const result = await analyzeWebsite('https://example.com');

console.log('GA4 detected:', result.analytics.ga4.found);
console.log('Measurement IDs:', result.analytics.ga4.measurementIds);
console.log('Ad platforms:', result.marketing.adPlatforms);
console.log('CMS:', result.infrastructure.cms);
```

### 3. Batch Analysis

```javascript
const { analyzeBatch } = require('./src/index');

const urls = [
  'https://github.com',
  'https://stackoverflow.com',
  'https://reddit.com'
];

const results = await analyzeBatch(urls, {
  outputDir: './reports',
  includeJson: false
});

// Check results
results.forEach(r => {
  console.log(`${r.success ? '✓' : '✗'} ${r.url}`);
});
```

### 4. Custom Markdown Formatting

```javascript
const { analyzeWebsite, formatAsMarkdown } = require('./src/index');
const fs = require('fs').promises;

const result = await analyzeWebsite('https://example.com');
const markdown = formatAsMarkdown(result);

// Send via email, post to API, etc.
await sendEmail({
  subject: `Tech Analysis for ${result.domain}`,
  body: markdown
});
```

### 5. Enhanced Detection with Browserless

```javascript
const { analyzeAndSave } = require('./src/index');

await analyzeAndSave('https://example.com', {
  browserlessApiKey: process.env.BROWSERLESS_API_KEY,
  outputDir: './reports',
  includeJson: true
});
```

## API Reference

### `analyzeWebsite(url, options)`

Analyzes a website and returns the raw result object.

**Parameters:**
- `url` (string): Website URL to analyze
- `options` (object):
  - `browserlessApiKey` (string): Optional Browserless API key
  - `timeout` (number): Request timeout in ms (default: 30000)

**Returns:** Promise<Object> - Analysis result

### `analyzeAndSave(url, options)`

Analyzes a website and saves results to markdown file.

**Parameters:**
- `url` (string): Website URL to analyze
- `options` (object):
  - `outputDir` (string): Directory for reports (default: './reports')
  - `filename` (string): Custom filename (default: auto-generated)
  - `browserlessApiKey` (string): Optional Browserless API key
  - `includeJson` (boolean): Also save JSON output (default: false)

**Returns:** Promise<Object> - Result with file paths

### `analyzeBatch(urls, options)`

Analyzes multiple websites in sequence.

**Parameters:**
- `urls` (string[]): Array of URLs to analyze
- `options` (object): Same as `analyzeAndSave`

**Returns:** Promise<Array> - Array of results

### `formatAsMarkdown(result)`

Formats an analysis result as markdown.

**Parameters:**
- `result` (object): Result from `analyzeWebsite()`

**Returns:** string - Formatted markdown

## Output Example

The markdown report includes:

```markdown
# Website Technology Analysis Report

**Website:** https://example.com
**Domain:** example.com
**Analysis Date:** 2025-01-15

## Executive Summary

**Total Technologies Detected:** 12

| Category | Count |
|----------|-------|
| Analytics & Tracking | 3 |
| Marketing Tools | 5 |
| Infrastructure | 2 |
| SEO Features | 2 |

## Analytics & Tracking

### ✅ Google Analytics 4
**Measurement IDs:**
- `G-XXXXXXXXXX`

### ✅ Google Tag Manager
**Container IDs:**
- `GTM-XXXXXXX`

...
```

## Configuration

### Environment Variables

```bash
# Optional: For enhanced JavaScript-based detection
BROWSERLESS_API_KEY=your_api_key_here
```

Get a Browserless API key at [browserless.io](https://www.browserless.io/) (starts at $5/month)

## How It Works

1. **Static Analysis** (Free, always enabled):
   - Fetches HTML with Node.js fetch
   - Regex pattern matching on HTML and script tags
   - Detects tools embedded in source code
   - No external dependencies required

2. **Enhanced Detection** (Optional, requires Browserless):
   - Renders page in real Chrome browser
   - Detects dynamically loaded pixels (GTM, etc.)
   - Captures network requests and cookies
   - Costs ~$0.003 per analysis

## Integration Ideas

- **Lead Enrichment**: Analyze prospect websites before sales calls
- **Competitive Analysis**: Track competitor tech stack changes
- **Automated Reports**: Schedule weekly tech audits
- **API Integration**: Add to your SaaS onboarding flow
- **Batch Processing**: Analyze entire lists of domains

## Limitations

- Static detection only catches tools loaded in initial HTML
- Some dynamically loaded tools require Browserless integration
- Rate limiting: Add delays between requests to be respectful
- JavaScript-heavy sites may need enhanced detection

## License

MIT

## Support

For issues or questions, please open an issue on GitHub.
