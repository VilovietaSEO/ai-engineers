/**
 * Example usage of Script Detector
 * This shows different ways to use the script detector in your backend
 */

const { analyzeAndSave, analyzeBatch, analyzeWebsite, formatAsMarkdown } = require('./src/index');

// Example 1: Analyze a single website and save to markdown
async function example1() {
  console.log('Example 1: Analyze single website\n');

  try {
    const result = await analyzeAndSave('https://example.com', {
      outputDir: './reports',
      includeJson: true // Also save JSON output
    });

    console.log('\n✅ Success!');
    console.log('Markdown report:', result.files.markdown);
    console.log('JSON data:', result.files.json);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Example 2: Analyze with custom filename
async function example2() {
  console.log('Example 2: Custom filename\n');

  await analyzeAndSave('https://github.com', {
    outputDir: './reports',
    filename: 'github-analysis',
    includeJson: false
  });
}

// Example 3: Analyze with Browserless for enhanced detection
async function example3() {
  console.log('Example 3: Enhanced detection with Browserless\n');

  // Set your Browserless API key
  const BROWSERLESS_API_KEY = process.env.BROWSERLESS_API_KEY;

  if (!BROWSERLESS_API_KEY) {
    console.log('⚠️  No Browserless API key found. Skipping enhanced detection.');
    console.log('Set BROWSERLESS_API_KEY environment variable to enable.');
    return;
  }

  await analyzeAndSave('https://example.com', {
    browserlessApiKey: BROWSERLESS_API_KEY,
    outputDir: './reports',
    includeJson: true
  });
}

// Example 4: Batch analysis of multiple websites
async function example4() {
  console.log('Example 4: Batch analysis\n');

  const urls = [
    'https://github.com',
    'https://stackoverflow.com',
    'https://reddit.com'
  ];

  const results = await analyzeBatch(urls, {
    outputDir: './reports',
    includeJson: false
  });

  console.log('\n=== Batch Summary ===');
  results.forEach(r => {
    console.log(`${r.success ? '✓' : '✗'} ${r.url}`);
  });
}

// Example 5: Programmatic usage (no file saving)
async function example5() {
  console.log('Example 5: Programmatic usage\n');

  try {
    const result = await analyzeWebsite('https://example.com');

    console.log('Technologies found:');
    console.log('- GA4:', result.analytics.ga4.found ? '✓' : '✗');
    console.log('- GTM:', result.analytics.gtm.found ? '✓' : '✗');
    console.log('- CMS:', result.infrastructure.cms.join(', ') || 'None detected');
    console.log('- Ad Platforms:', result.marketing.adPlatforms.length);

    // You can process the result however you want
    if (result.analytics.ga4.found) {
      console.log('\nGA4 Measurement IDs:', result.analytics.ga4.measurementIds);
    }

  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Example 6: Custom markdown formatting
async function example6() {
  console.log('Example 6: Custom processing\n');

  const result = await analyzeWebsite('https://example.com');

  // Generate markdown
  const markdown = formatAsMarkdown(result);

  // You could send this via email, post to an API, etc.
  console.log('Markdown length:', markdown.length, 'characters');
  console.log('\nFirst 200 characters:');
  console.log(markdown.substring(0, 200) + '...');
}

// Run examples
async function main() {
  const exampleNumber = process.argv[2] || '1';

  console.log('='.repeat(60));
  console.log('Script Detector - Example Usage');
  console.log('='.repeat(60));
  console.log('');

  switch (exampleNumber) {
    case '1':
      await example1();
      break;
    case '2':
      await example2();
      break;
    case '3':
      await example3();
      break;
    case '4':
      await example4();
      break;
    case '5':
      await example5();
      break;
    case '6':
      await example6();
      break;
    case 'all':
      await example1();
      console.log('\n' + '='.repeat(60) + '\n');
      await example2();
      console.log('\n' + '='.repeat(60) + '\n');
      await example5();
      break;
    default:
      console.log('Usage: node example.js [1-6|all]');
      console.log('');
      console.log('Examples:');
      console.log('  1 - Analyze single website');
      console.log('  2 - Custom filename');
      console.log('  3 - Enhanced detection (requires Browserless)');
      console.log('  4 - Batch analysis');
      console.log('  5 - Programmatic usage');
      console.log('  6 - Custom formatting');
      console.log('  all - Run multiple examples');
  }
}

// Only run if called directly (not required as module)
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { example1, example2, example3, example4, example5, example6 };
