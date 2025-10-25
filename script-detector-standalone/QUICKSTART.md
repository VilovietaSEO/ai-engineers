# Quick Start Guide

## 🚀 Get Started in 30 Seconds

### 1. Copy the Folder
Copy the entire `script-detector-standalone` folder into your project.

### 2. Run Your First Analysis

```javascript
const { analyzeAndSave } = require('./script-detector-standalone/src/index');

// Analyze a website and save markdown report
await analyzeAndSave('https://yourwebsite.com');

// Report saved to: ./reports/yourwebsite.com-2025-01-15.md
```

### 3. Check the Output

```bash
cat reports/yourwebsite.com-*.md
```

## Common Use Cases

### Backend Script
```javascript
// analyze.js
const { analyzeAndSave } = require('./script-detector-standalone/src/index');

async function main() {
  const url = process.argv[2] || 'https://example.com';

  try {
    await analyzeAndSave(url, {
      outputDir: './reports',
      includeJson: true
    });
    console.log('✓ Analysis complete!');
  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
```

Run it:
```bash
node analyze.js https://github.com
```

### CronJob / Scheduled Task
```javascript
const { analyzeBatch } = require('./script-detector-standalone/src/index');

async function dailyAudit() {
  const competitors = [
    'https://competitor1.com',
    'https://competitor2.com',
    'https://competitor3.com'
  ];

  await analyzeBatch(competitors, {
    outputDir: './daily-reports',
    includeJson: true
  });
}

// Run daily at 2am
dailyAudit();
```

### API Integration
```javascript
const express = require('express');
const { analyzeWebsite } = require('./script-detector-standalone/src/index');

const app = express();

app.get('/analyze', async (req, res) => {
  try {
    const result = await analyzeWebsite(req.query.url);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000);
```

### Lead Enrichment
```javascript
const { analyzeWebsite } = require('./script-detector-standalone/src/index');

async function enrichLead(leadEmail, leadWebsite) {
  const techStack = await analyzeWebsite(leadWebsite);

  const leadData = {
    email: leadEmail,
    website: leadWebsite,
    hasGA4: techStack.analytics.ga4.found,
    hasCRM: techStack.marketing.crm.length > 0,
    cms: techStack.infrastructure.cms[0] || 'Unknown',
    totalTech: techStack.summary.totalToolsFound
  };

  // Save to your CRM
  await saveToCRM(leadData);
}
```

## That's It!

No dependencies, no complex setup. Just copy, import, and run.

## Need Help?

- See `README.md` for full documentation
- Run `node example.js` for more examples
- Check `example.js` source code for usage patterns
