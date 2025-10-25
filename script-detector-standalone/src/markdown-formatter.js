/**
 * Markdown Formatter for Script Detector Results
 * Converts detection results into a formatted markdown report
 */

/**
 * Format analysis results as markdown
 * @param {Object} result - Analysis result from analyzeWebsite()
 * @returns {string} Formatted markdown report
 */
function formatAsMarkdown(result) {
  const sections = [];

  // Header
  sections.push(`# Website Technology Analysis Report`);
  sections.push('');
  sections.push(`**Website:** ${result.url}`);
  sections.push(`**Domain:** ${result.domain}`);
  sections.push(`**Analysis Date:** ${new Date(result.timestamp).toLocaleString()}`);
  if (result.pageTitle) {
    sections.push(`**Page Title:** ${result.pageTitle}`);
  }
  sections.push('');
  sections.push('---');
  sections.push('');

  // Executive Summary
  sections.push('## Executive Summary');
  sections.push('');
  sections.push(`**Total Technologies Detected:** ${result.summary.totalToolsFound}`);
  sections.push('');
  sections.push('| Category | Count |');
  sections.push('|----------|-------|');
  sections.push(`| Analytics & Tracking | ${result.summary.categories.analytics} |`);
  sections.push(`| Marketing Tools | ${result.summary.categories.marketing} |`);
  sections.push(`| Infrastructure | ${result.summary.categories.infrastructure} |`);
  sections.push(`| SEO Features | ${result.summary.categories.seo} |`);
  sections.push('');

  // Analytics Section
  sections.push('## Analytics & Tracking');
  sections.push('');

  if (result.analytics.ga4.found) {
    sections.push('### ✅ Google Analytics 4');
    if (result.analytics.ga4.measurementIds.length > 0) {
      sections.push(`**Measurement IDs:**`);
      result.analytics.ga4.measurementIds.forEach(id => {
        sections.push(`- \`${id}\``);
      });
    }
    sections.push('');
  }

  if (result.analytics.gtm.found) {
    sections.push('### ✅ Google Tag Manager');
    if (result.analytics.gtm.containerIds.length > 0) {
      sections.push(`**Container IDs:**`);
      result.analytics.gtm.containerIds.forEach(id => {
        sections.push(`- \`${id}\``);
      });
    }
    sections.push('');
  }

  if (result.analytics.microsoftClarity.found) {
    sections.push('### ✅ Microsoft Clarity');
    if (result.analytics.microsoftClarity.projectId) {
      sections.push(`**Project ID:** \`${result.analytics.microsoftClarity.projectId}\``);
    }
    sections.push('');
  }

  if (result.analytics.searchConsole.found) {
    sections.push('### ✅ Google Search Console');
    if (result.analytics.searchConsole.verificationCode) {
      sections.push(`**Verification Code:** \`${result.analytics.searchConsole.verificationCode}\``);
    }
    sections.push('');
  }

  if (result.analytics.bingWebmaster.found) {
    sections.push('### ✅ Bing Webmaster Tools');
    if (result.analytics.bingWebmaster.verificationCode) {
      sections.push(`**Verification Code:** \`${result.analytics.bingWebmaster.verificationCode}\``);
    }
    sections.push('');
  }

  if (result.analytics.seoPlugin.found && result.analytics.seoPlugin.plugins.length > 0) {
    sections.push('### ✅ SEO Plugins');
    result.analytics.seoPlugin.plugins.forEach(plugin => {
      sections.push(`- ${plugin}`);
    });
    sections.push('');
  }

  // Marketing Tools Section
  sections.push('## Marketing Tools');
  sections.push('');

  if (result.marketing.crm.length > 0) {
    sections.push('### CRM Platforms');
    result.marketing.crm.forEach(crm => {
      sections.push(`- ${crm}`);
    });
    sections.push('');
  }

  if (result.marketing.emailMarketing.length > 0) {
    sections.push('### Email Marketing');
    result.marketing.emailMarketing.forEach(tool => {
      sections.push(`- ${tool}`);
    });
    sections.push('');
  }

  if (result.marketing.adPlatforms.length > 0) {
    sections.push('### Advertising & Tracking Pixels');
    result.marketing.adPlatforms.forEach(platform => {
      sections.push(`- ${platform}`);
    });
    sections.push('');

    if (result.marketing.pixelIds.length > 0) {
      sections.push('**Pixel IDs Detected:**');
      result.marketing.pixelIds.forEach(id => {
        sections.push(`- \`${id}\``);
      });
      sections.push('');
    }
  }

  if (result.marketing.conversionTools.length > 0) {
    sections.push('### Conversion Optimization Tools');
    result.marketing.conversionTools.forEach(tool => {
      sections.push(`- ${tool}`);
    });
    sections.push('');
  }

  if (result.marketing.widgets.length > 0) {
    sections.push('### Chat Widgets & Forms');
    result.marketing.widgets.forEach(widget => {
      sections.push(`- ${widget}`);
    });
    sections.push('');
  }

  // Infrastructure Section
  sections.push('## Infrastructure & Technology Stack');
  sections.push('');

  if (result.infrastructure.cms.length > 0) {
    sections.push('### Content Management System (CMS)');
    result.infrastructure.cms.forEach(cms => {
      sections.push(`- ${cms}`);
    });
    sections.push('');
  }

  if (result.infrastructure.ecommerce) {
    sections.push('### E-commerce Platform');
    sections.push(`- ${result.infrastructure.ecommerce}`);
    sections.push('');
  }

  if (result.infrastructure.cdn.length > 0) {
    sections.push('### Content Delivery Network (CDN)');
    result.infrastructure.cdn.forEach(cdn => {
      sections.push(`- ${cdn}`);
    });
    sections.push('');
  }

  if (result.infrastructure.hosting) {
    sections.push('### Hosting');
    sections.push(`- ${result.infrastructure.hosting}`);
    sections.push('');
  }

  // SEO Section
  sections.push('## SEO & Metadata');
  sections.push('');

  if (result.seo.hasSchema) {
    sections.push('### ✅ Structured Data (Schema.org)');
    if (result.seo.schemaTypes.length > 0) {
      sections.push('**Schema Types:**');
      result.seo.schemaTypes.forEach(type => {
        sections.push(`- ${type}`);
      });
    }
    sections.push('');
  } else {
    sections.push('### ❌ Structured Data (Schema.org)');
    sections.push('No structured data detected. Consider adding Schema.org markup.');
    sections.push('');
  }

  sections.push('### Meta Tags');
  sections.push('');

  const metaDesc = result.seo.metaTags?.basic?.description;
  if (metaDesc) {
    sections.push(`**Meta Description:** ${metaDesc}`);
  } else {
    sections.push(`**Meta Description:** ❌ Not found`);
  }
  sections.push('');

  if (result.seo.canonical) {
    sections.push(`**Canonical URL:** \`${result.seo.canonical}\``);
  } else {
    sections.push(`**Canonical URL:** Not set`);
  }
  sections.push('');

  if (result.seo.robots) {
    sections.push(`**Robots Meta Tag:** \`${result.seo.robots}\``);
  } else {
    sections.push(`**Robots Meta Tag:** Not set (defaults to index, follow)`);
  }
  sections.push('');

  // Performance Metrics
  sections.push('## Performance Metrics');
  sections.push('');
  sections.push(`- **HTTP Status Code:** ${result.statusCode}`);
  sections.push(`- **Page Load Time:** ${result.fetchTimeMs}ms`);
  sections.push(`- **HTML Size:** ${(result.htmlSize / 1024).toFixed(2)} KB`);
  sections.push('');

  // Enhanced Detection Note
  if (result.enhancedDetection) {
    sections.push('> **Note:** This report includes enhanced JavaScript-based detection using Browserless.');
  } else {
    sections.push('> **Note:** This report is based on static HTML analysis. Some dynamically loaded tools may not be detected.');
  }
  sections.push('');

  // Footer
  sections.push('---');
  sections.push('');
  sections.push('*Report generated by Script Detector*');
  sections.push('');

  return sections.join('\n');
}

/**
 * Format analysis results as a simple text summary
 * @param {Object} result - Analysis result from analyzeWebsite()
 * @returns {string} Simple text summary
 */
function formatAsText(result) {
  const lines = [];

  lines.push('='.repeat(60));
  lines.push(`WEBSITE TECHNOLOGY ANALYSIS`);
  lines.push('='.repeat(60));
  lines.push('');
  lines.push(`URL: ${result.url}`);
  lines.push(`Domain: ${result.domain}`);
  lines.push(`Analyzed: ${new Date(result.timestamp).toLocaleString()}`);
  lines.push('');
  lines.push(`Total Technologies: ${result.summary.totalToolsFound}`);
  lines.push('');

  if (result.analytics.ga4.found) {
    lines.push('✓ Google Analytics 4');
  }
  if (result.analytics.gtm.found) {
    lines.push('✓ Google Tag Manager');
  }
  if (result.analytics.microsoftClarity.found) {
    lines.push('✓ Microsoft Clarity');
  }

  result.marketing.adPlatforms.forEach(platform => {
    lines.push(`✓ ${platform}`);
  });

  result.marketing.crm.forEach(crm => {
    lines.push(`✓ ${crm}`);
  });

  result.infrastructure.cms.forEach(cms => {
    lines.push(`✓ CMS: ${cms}`);
  });

  lines.push('');
  lines.push('='.repeat(60));

  return lines.join('\n');
}

module.exports = {
  formatAsMarkdown,
  formatAsText
};
