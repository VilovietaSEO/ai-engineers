# Script Detector - Backend Website Technology Analyzer

A powerful, backend-only Node.js tool that analyzes websites to detect their marketing tools, analytics platforms, tracking pixels, CMS, and complete technology stack. Results are automatically saved as formatted markdown reports.

## 🎯 What It Does

Analyzes any website URL and generates a comprehensive technology report detecting **100+ tools** including:

- **Analytics**: Google Analytics 4, GTM, Microsoft Clarity, Search Console, Bing Webmaster
- **Ad Pixels**: Facebook/Meta, LinkedIn Insight, TikTok, Twitter, Pinterest, Snapchat, Reddit
- **CRM Platforms**: HubSpot, Salesforce, Marketo, Pipedrive, Zoho
- **Email Marketing**: Mailchimp, Klaviyo, ActiveCampaign, ConvertKit, Brevo
- **Conversion Tools**: Hotjar, Optimizely, VWO, FullStory, Segment, Mouseflow
- **CMS**: WordPress, Shopify, Webflow, Wix, Squarespace, Drupal
- **Chat Widgets**: Intercom, Drift, Zendesk, Tawk.to, Crisp, LiveChat
- **E-commerce**: WooCommerce, Shopify, Magento, BigCommerce
- **Infrastructure**: CDN detection, hosting providers, WordPress plugins
- **SEO**: Schema.org structured data, meta tags, canonical URLs

## 🚀 Quick Start

### 1. Navigate to the folder
```bash
cd script-detector-standalone
```

### 2. Run your first analysis
```javascript
const { analyzeAndSave } = require('./src/index');

await analyzeAndSave('https://example.com');
// Report saved to: ./reports/example.com-2025-10-25.md
```

### 3. View the results
```bash
cat reports/example.com-*.md
```

## 📋 Features

✅ **Zero Dependencies** - Pure Node.js, no npm packages required
✅ **Backend-Only** - Perfect for server-side automation
✅ **Markdown Reports** - Professional, readable output
✅ **Batch Processing** - Analyze multiple websites at once
✅ **JSON Export** - Optional structured data output
✅ **Pixel ID Detection** - Extracts actual tracking IDs
✅ **SEO Analysis** - Meta tags, schema markup, canonical URLs
✅ **Performance Metrics** - Load time, page size, HTTP status

## 💡 Use Cases

### 1. Lead Enrichment
```javascript
const { analyzeWebsite } = require('./script-detector-standalone/src/index');

async function enrichProspect(prospectWebsite) {
  const tech = await analyzeWebsite(prospectWebsite);

  return {
    hasGA4: tech.analytics.ga4.found,
    hasCRM: tech.marketing.crm.length > 0,
    cmsType: tech.infrastructure.cms[0] || 'Unknown',
    adPlatforms: tech.marketing.adPlatforms,
    techMaturity: tech.summary.totalToolsFound
  };
}
```

### 2. Competitive Intelligence
```javascript
const { analyzeBatch } = require('./script-detector-standalone/src/index');

const competitors = [
  'https://competitor1.com',
  'https://competitor2.com',
  'https://competitor3.com'
];

await analyzeBatch(competitors, {
  outputDir: './competitor-analysis',
  includeJson: true
});
```

### 3. Automated Audits
```javascript
const { analyzeAndSave } = require('./script-detector-standalone/src/index');

// Daily audit script
async function dailyAudit() {
  const clients = ['client1.com', 'client2.com', 'client3.com'];

  for (const client of clients) {
    await analyzeAndSave(`https://${client}`, {
      outputDir: `./audits/${new Date().toISOString().split('T')[0]}`,
      includeJson: true
    });
  }
}
```

### 4. API Integration
```javascript
const express = require('express');
const { analyzeWebsite } = require('./script-detector-standalone/src/index');

const app = express();

app.get('/api/analyze', async (req, res) => {
  try {
    const result = await analyzeWebsite(req.query.url);
    res.json({
      domain: result.domain,
      technologies: result.summary.totalToolsFound,
      analytics: result.analytics,
      marketing: result.marketing,
      cms: result.infrastructure.cms
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000);
```

## 📊 Example Output

### Markdown Report Sample
```markdown
# Website Technology Analysis Report

**Website:** https://example.com
**Domain:** example.com
**Analysis Date:** 2025-10-25
**Total Technologies Detected:** 15

## Executive Summary

| Category | Count |
|----------|-------|
| Analytics & Tracking | 4 |
| Marketing Tools | 7 |
| Infrastructure | 3 |
| SEO Features | 1 |

## Analytics & Tracking

### ✅ Google Analytics 4
**Measurement IDs:**
- `G-XXXXXXXXXX`

### ✅ Google Tag Manager
**Container IDs:**
- `GTM-XXXXXXX`

### ✅ Microsoft Clarity
**Project ID:** `abc123def`

## Marketing Tools

### Advertising & Tracking Pixels
- Facebook/Meta Pixel
- LinkedIn Insight Tag
- TikTok Pixel

**Pixel IDs Detected:**
- `Facebook: 1234567890`
- `LinkedIn: 98765`

### CRM Platforms
- HubSpot

### Email Marketing
- Mailchimp

[... continues with full details ...]
```

### JSON Output Sample
```json
{
  "url": "https://example.com",
  "domain": "example.com",
  "timestamp": "2025-10-25T10:30:00.000Z",
  "pageTitle": "Example Domain",
  "analytics": {
    "ga4": {
      "found": true,
      "measurementIds": ["G-XXXXXXXXXX"]
    },
    "gtm": {
      "found": true,
      "containerIds": ["GTM-XXXXXXX"]
    }
  },
  "marketing": {
    "crm": ["HubSpot"],
    "adPlatforms": ["Facebook/Meta Pixel", "LinkedIn Insight Tag"],
    "pixelIds": ["Facebook: 1234567890"]
  },
  "summary": {
    "totalToolsFound": 15
  }
}
```

## 🔧 Advanced Features

### Enhanced JavaScript Detection (Optional)

For detecting pixels loaded dynamically via Google Tag Manager, integrate with [Browserless](https://www.browserless.io/):

```javascript
await analyzeAndSave('https://example.com', {
  browserlessApiKey: process.env.BROWSERLESS_API_KEY,
  outputDir: './reports',
  includeJson: true
});
```

This uses a real Chrome browser to:
- Detect dynamically loaded pixels
- Capture network requests
- Analyze cookies
- Find GTM-deployed tracking

**Cost:** ~$0.003 per analysis (~300 analyses per $1)

### Batch Analysis with Delays

```javascript
const { analyzeWebsite, formatAsMarkdown } = require('./script-detector-standalone/src/index');
const fs = require('fs').promises;

async function analyzeBatchWithDelay(urls) {
  for (const url of urls) {
    try {
      const result = await analyzeWebsite(url);
      const markdown = formatAsMarkdown(result);

      await fs.writeFile(
        `./reports/${result.domain}.md`,
        markdown,
        'utf8'
      );

      console.log(`✓ ${url} - ${result.summary.totalToolsFound} technologies`);

      // Be polite - wait 2 seconds between requests
      await new Promise(resolve => setTimeout(resolve, 2000));
    } catch (error) {
      console.error(`✗ ${url} - ${error.message}`);
    }
  }
}
```

## 📚 Full Documentation

See the complete documentation in the `script-detector-standalone` folder:

- **[README.md](./script-detector-standalone/README.md)** - Full API reference
- **[QUICKSTART.md](./script-detector-standalone/QUICKSTART.md)** - Get started in 30 seconds
- **[example.js](./script-detector-standalone/example.js)** - 6 usage examples

## 🔍 How It Works

### Static Analysis (Free, Always Enabled)
1. Fetches HTML using Node.js native fetch
2. Extracts all `<script>` tags and inline JavaScript
3. Pattern matches against 100+ tool signatures
4. Detects tracking IDs, pixel IDs, container IDs
5. Analyzes meta tags and structured data
6. Checks HTTP headers for hosting/CDN clues

### Enhanced Detection (Optional)
1. Launches headless Chrome via Browserless
2. Renders JavaScript and waits for lazy-loaded scripts
3. Monitors network requests for tracking pixels
4. Captures cookies set by analytics tools
5. Executes browser context checks (window.gtag, window.fbq, etc.)
6. Merges results with static analysis

## 🎨 Integration Patterns

### CronJob / Scheduled Analysis
```bash
# Add to crontab
0 2 * * * cd /path/to/ai-engineers/script-detector-standalone && node -e "require('./src/index').analyzeBatch(['site1.com', 'site2.com'], {outputDir: './daily-reports'})"
```

### Lambda/Serverless Function
```javascript
// AWS Lambda handler
exports.handler = async (event) => {
  const { analyzeWebsite } = require('./script-detector-standalone/src/index');

  const url = event.queryStringParameters.url;
  const result = await analyzeWebsite(url);

  return {
    statusCode: 200,
    body: JSON.stringify(result)
  };
};
```

### Custom Markdown Formatting
```javascript
const { analyzeWebsite } = require('./script-detector-standalone/src/index');

const result = await analyzeWebsite('https://example.com');

// Build custom report
const customReport = `
# Tech Stack for ${result.domain}

**Marketing Maturity Score:** ${result.summary.totalToolsFound}/100

## Key Findings
- Analytics: ${result.analytics.ga4.found ? '✅' : '❌'} GA4
- CRM: ${result.marketing.crm.length > 0 ? '✅' : '❌'} ${result.marketing.crm[0] || 'None'}
- Tracking Pixels: ${result.marketing.adPlatforms.length}

${result.analytics.ga4.found ? '✅' : '⚠️'} Ready for analytics tracking
`;

console.log(customReport);
```

## 📦 Requirements

- **Node.js**: v18.0.0 or higher
- **No npm dependencies** - Uses native Node.js APIs
- **Optional**: Browserless API key for enhanced detection

## 🤝 Contributing

This tool is part of the [ai-engineers](https://github.com/VilovietaSEO/ai-engineers) collection. Contributions welcome!

## 📄 License

MIT

---

**Location:** `/script-detector-standalone/`
**Generated with:** [Claude Code](https://claude.com/claude-code)
**Repository:** https://github.com/VilovietaSEO/ai-engineers
