/**
 * Script Detector - Main Entry Point
 * Backend-only website technology detection and analysis
 */

const { analyzeWebsite } = require('./detector');
const { formatAsMarkdown, formatAsText } = require('./markdown-formatter');
const fs = require('fs').promises;
const path = require('path');

/**
 * Analyze a website and save results to markdown file
 * @param {string} url - The URL to analyze
 * @param {Object} options - Configuration options
 * @param {string} options.outputDir - Directory to save the report (default: './reports')
 * @param {string} options.filename - Custom filename (default: auto-generated from domain)
 * @param {string} options.browserlessApiKey - Browserless API key for enhanced detection
 * @param {boolean} options.includeJson - Also save JSON output (default: false)
 * @returns {Promise<Object>} Analysis result and file paths
 */
async function analyzeAndSave(url, options = {}) {
  const {
    outputDir = './reports',
    filename = null,
    browserlessApiKey = null,
    includeJson = false
  } = options;

  console.log(`Analyzing ${url}...`);

  // Run analysis
  const result = await analyzeWebsite(url, {
    browserlessApiKey,
    timeout: 30000
  });

  console.log(`✓ Analysis complete. Found ${result.summary.totalToolsFound} technologies.`);

  // Create output directory if it doesn't exist
  try {
    await fs.mkdir(outputDir, { recursive: true });
  } catch (error) {
    // Directory might already exist
  }

  // Generate filenames
  const timestamp = new Date().toISOString().split('T')[0];
  const baseFilename = filename || `${result.domain}-${timestamp}`;
  const mdPath = path.join(outputDir, `${baseFilename}.md`);
  const jsonPath = path.join(outputDir, `${baseFilename}.json`);

  // Save markdown report
  const markdown = formatAsMarkdown(result);
  await fs.writeFile(mdPath, markdown, 'utf8');
  console.log(`✓ Markdown report saved: ${mdPath}`);

  // Optionally save JSON
  let savedJsonPath = null;
  if (includeJson) {
    await fs.writeFile(jsonPath, JSON.stringify(result, null, 2), 'utf8');
    console.log(`✓ JSON data saved: ${jsonPath}`);
    savedJsonPath = jsonPath;
  }

  return {
    result,
    files: {
      markdown: mdPath,
      json: savedJsonPath
    }
  };
}

/**
 * Analyze multiple websites in batch
 * @param {string[]} urls - Array of URLs to analyze
 * @param {Object} options - Configuration options (same as analyzeAndSave)
 * @returns {Promise<Object[]>} Array of analysis results
 */
async function analyzeBatch(urls, options = {}) {
  console.log(`Starting batch analysis of ${urls.length} websites...`);

  const results = [];

  for (let i = 0; i < urls.length; i++) {
    const url = urls[i];
    console.log(`\n[${i + 1}/${urls.length}] Processing ${url}`);

    try {
      const result = await analyzeAndSave(url, options);
      results.push({ url, success: true, ...result });
    } catch (error) {
      console.error(`✗ Failed to analyze ${url}: ${error.message}`);
      results.push({ url, success: false, error: error.message });
    }

    // Small delay between requests to be polite
    if (i < urls.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  console.log(`\nBatch analysis complete. ${results.filter(r => r.success).length}/${urls.length} successful.`);

  return results;
}

module.exports = {
  analyzeWebsite,
  analyzeAndSave,
  analyzeBatch,
  formatAsMarkdown,
  formatAsText
};
