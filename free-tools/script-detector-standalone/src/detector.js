/**
 * Script Detector - Standalone Backend Module
 * Detects marketing tools, analytics, pixels, and tech stack from any website
 */

/**
 * Main function to analyze a website
 * @param {string} url - The URL to analyze
 * @param {Object} options - Optional configuration
 * @param {string} options.browserlessApiKey - Browserless API key for enhanced detection
 * @param {number} options.timeout - Request timeout in ms (default: 30000)
 * @returns {Promise<Object>} Analysis results
 */
async function analyzeWebsite(url, options = {}) {
  const {
    browserlessApiKey = null,
    timeout = 30000
  } = options;

  // Normalize URL
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url;
  }

  // Validate URL
  try {
    new URL(url);
  } catch (error) {
    throw new Error(`Invalid URL: ${url}`);
  }

  const startTime = Date.now();

  // Fetch the page
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  let response;
  try {
    response = await fetch(url, {
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
      },
      redirect: 'follow',
      signal: controller.signal
    });
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error('Request timed out');
    }
    throw new Error(`Failed to fetch ${url}: ${error.message}`);
  } finally {
    clearTimeout(timeoutId);
  }

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const html = await response.text();
  const headers = Object.fromEntries(response.headers.entries());
  const fetchTimeMs = Date.now() - startTime;

  // Extract domain
  const urlObj = new URL(url);
  const domain = urlObj.hostname.replace(/^www\./, '');

  // Run all detectors
  const detections = runDetectors(html, headers);

  // Build result object
  const result = {
    url,
    domain,
    timestamp: new Date().toISOString(),
    pageTitle: detections.pageTitle,
    fetchTimeMs,
    statusCode: response.status,
    htmlSize: html.length,
    analytics: detections.analytics,
    marketing: detections.marketing,
    infrastructure: {
      ...detections.infrastructure,
      hosting: detectHostingFromHeaders(headers, domain)
    },
    seo: detections.seo,
    enhancedDetection: false
  };

  // Enhanced detection with Browserless (optional)
  if (browserlessApiKey) {
    try {
      const enhancedData = await runBrowserlessDetection(url, browserlessApiKey);
      result.enhancedDetection = true;

      // Merge enhanced data
      if (enhancedData.pixels) {
        Object.entries(enhancedData.pixels).forEach(([platform, found]) => {
          if (found && !result.marketing.adPlatforms.includes(platform)) {
            result.marketing.adPlatforms.push(platform);
          }
        });
      }

      if (enhancedData.pixelIds) {
        result.marketing.pixelIds = [
          ...result.marketing.pixelIds,
          ...Object.entries(enhancedData.pixelIds).flatMap(([platform, ids]) =>
            Array.isArray(ids) ? ids.map(id => `${platform}: ${id}`) : []
          )
        ];
      }
    } catch (error) {
      console.warn('Enhanced detection failed:', error.message);
    }
  }

  // Calculate summary
  result.summary = calculateSummary(result);

  return result;
}

/**
 * Run all static detectors on HTML content
 */
function runDetectors(html, headers) {
  const scriptContents = extractScriptContents(html);
  const combined = `${html} ${scriptContents}`;

  return {
    pageTitle: extractPageTitle(html),
    analytics: {
      ga4: checkGA4(combined),
      gtm: checkGTM(combined),
      microsoftClarity: checkMicrosoftClarity(combined),
      searchConsole: checkSearchConsole(html),
      seoPlugin: checkSEOPlugins(html),
      bingWebmaster: checkBingWebmaster(html)
    },
    marketing: {
      crm: checkCRMPlatforms(combined),
      emailMarketing: checkEmailMarketingTools(combined),
      adPlatforms: checkAdPlatforms(combined).platforms,
      pixelIds: checkAdPlatforms(combined).pixelIds,
      conversionTools: checkConversionOptimizationTools(combined),
      widgets: checkWidgets(combined)
    },
    infrastructure: {
      cms: checkCMS(combined, html),
      ecommerce: checkEcommercePlatforms(combined, html),
      cdn: checkCDNProviders(combined, headers)
    },
    seo: {
      hasSchema: extractJSONLDSchema(html).found,
      schemaTypes: extractJSONLDSchema(html).types,
      metaTags: extractImportantMetaTags(html),
      canonical: extractImportantMetaTags(html).basic.canonical || null,
      robots: extractImportantMetaTags(html).basic.robots || null
    }
  };
}

function extractScriptContents(html) {
  const scriptPattern = /<script[^>]*>([\s\S]*?)<\/script>/gi;
  let allScripts = '';
  let match;

  while ((match = scriptPattern.exec(html)) !== null) {
    allScripts += ` ${match[1]} `;
  }

  return allScripts;
}

function extractPageTitle(html) {
  const match = html.match(/<title>([^<]*)<\/title>/i);
  return match ? match[1].trim() : null;
}

function checkGA4(content) {
  const found = /googletagmanager\.com\/gtag\/js/.test(content) ||
                /G-[A-Z0-9]{8,12}/.test(content);
  const ids = [];
  const idPattern = /(?:["'\s,;(]|^)(G-[A-Z0-9]{8,12})(?:["'\s,;)]|$)/gi;
  let match;

  while ((match = idPattern.exec(content)) !== null) {
    if (!ids.includes(match[1])) ids.push(match[1]);
  }

  return { found, measurementIds: ids };
}

function checkGTM(content) {
  const found = /googletagmanager\.com\/gtm\.js/.test(content);
  const ids = [];
  const idPattern = /(?:["'\s,;(?]|^)(GTM-[A-Z0-9]{5,8})(?:["'\s,;)?]|$)/gi;
  let match;

  while ((match = idPattern.exec(content)) !== null) {
    if (!ids.includes(match[1])) ids.push(match[1]);
  }

  return { found, containerIds: ids };
}

function checkMicrosoftClarity(content) {
  const found = /clarity\.ms/.test(content);
  const idMatch = content.match(/clarity\.ms\/tag\/([a-z0-9-]{6,40})/i);
  return { found, projectId: idMatch ? idMatch[1] : null };
}

function checkSearchConsole(html) {
  const metaMatch = html.match(/<meta\s+name=["']google-site-verification["']\s+content=["']([^"']+)["']/i);
  return { found: !!metaMatch, verificationCode: metaMatch ? metaMatch[1] : null };
}

function checkSEOPlugins(html) {
  const plugins = [];
  if (/yoast\.com|yoast\s+seo/gi.test(html)) plugins.push('Yoast SEO');
  if (/rankmath/gi.test(html)) plugins.push('Rank Math SEO');
  if (/all\s+in\s+one\s+seo|aioseo/gi.test(html)) plugins.push('All in One SEO');
  return { found: plugins.length > 0, plugins };
}

function checkBingWebmaster(html) {
  const metaMatch = html.match(/<meta\s+name=["']msvalidate\.01["']\s+content=["']([^"']+)["']/i);
  return { found: !!metaMatch, verificationCode: metaMatch ? metaMatch[1] : null };
}

function checkCRMPlatforms(content) {
  const platforms = [];
  if (/hs-scripts\.com|hsappstatic\.net|hubspot/gi.test(content)) platforms.push('HubSpot');
  if (/salesforce\.com|pardot\.com/gi.test(content)) platforms.push('Salesforce');
  if (/marketo\.net|mktoForms/gi.test(content)) platforms.push('Marketo');
  if (/pipedrive\.com/gi.test(content)) platforms.push('Pipedrive');
  if (/zoho\.com|zohostatic\.com/gi.test(content)) platforms.push('Zoho CRM');
  return platforms;
}

function checkEmailMarketingTools(content) {
  const tools = [];
  if (/list-manage\.com|mailchimp\.com/gi.test(content)) tools.push('Mailchimp');
  if (/klaviyo\.com/gi.test(content)) tools.push('Klaviyo');
  if (/activecampaign\.com/gi.test(content)) tools.push('ActiveCampaign');
  if (/constantcontact\.com/gi.test(content)) tools.push('Constant Contact');
  if (/convertkit\.com/gi.test(content)) tools.push('ConvertKit');
  if (/sendinblue\.com|brevo\.com/gi.test(content)) tools.push('Brevo/Sendinblue');
  return tools;
}

function checkAdPlatforms(content) {
  const platforms = [];
  const pixelIds = [];

  if (/googleadservices\.com|google_conversion/gi.test(content)) platforms.push('Google Ads');
  if (/facebook\.com\/tr|fbevents\.js|fbq\s*\(/gi.test(content)) platforms.push('Facebook/Meta Pixel');
  if (/snap\.licdn\.com|linkedin\.com\/px/gi.test(content)) platforms.push('LinkedIn Insight Tag');
  if (/analytics\.tiktok\.com|ttq\.load/gi.test(content)) platforms.push('TikTok Pixel');
  if (/static\.ads-twitter\.com|twq\s*\(/gi.test(content)) platforms.push('Twitter/X Pixel');
  if (/pintrk|ct\.pinterest\.com/gi.test(content)) platforms.push('Pinterest Tag');
  if (/sc-static\.net|snaptr/gi.test(content)) platforms.push('Snapchat Pixel');
  if (/reddit\.com\/pixel|rdt\s*\(/gi.test(content)) platforms.push('Reddit Pixel');

  // Extract Facebook Pixel IDs
  const fbPattern = /fbq\s*\(\s*['"]init['"]\s*,\s*['"](\d+)['"]\s*\)/gi;
  let match;
  while ((match = fbPattern.exec(content)) !== null) {
    pixelIds.push(`Facebook: ${match[1]}`);
  }

  return { platforms, pixelIds };
}

function checkConversionOptimizationTools(content) {
  const tools = [];
  if (/static\.hotjar\.com|hotjar\.js/gi.test(content)) tools.push('Hotjar');
  if (/optimizely\.com/gi.test(content)) tools.push('Optimizely');
  if (/visualwebsiteoptimizer\.com|vwo\.com/gi.test(content)) tools.push('VWO');
  if (/crazyegg\.com/gi.test(content)) tools.push('Crazy Egg');
  if (/mouseflow\.com/gi.test(content)) tools.push('Mouseflow');
  if (/fullstory\.com/gi.test(content)) tools.push('FullStory');
  if (/luckyorange\.com/gi.test(content)) tools.push('Lucky Orange');
  if (/cdn\.segment\.com/gi.test(content)) tools.push('Segment');
  return tools;
}

function checkWidgets(content) {
  const widgets = [];
  if (/intercom\.io|intercomcdn\.com/gi.test(content)) widgets.push('Intercom');
  if (/zendesk\.com|zdassets\.com/gi.test(content)) widgets.push('Zendesk Chat');
  if (/drift\.com|js\.driftt\.com/gi.test(content)) widgets.push('Drift');
  if (/tawk\.to/gi.test(content)) widgets.push('Tawk.to');
  if (/livechatinc\.com/gi.test(content)) widgets.push('LiveChat');
  if (/crisp\.chat/gi.test(content)) widgets.push('Crisp');
  if (/calendly\.com/gi.test(content)) widgets.push('Calendly');
  if (/typeform\.com/gi.test(content)) widgets.push('Typeform');
  return widgets;
}

function checkCMS(combined, html) {
  const cmsList = [];
  if (/wp-content\/|wp-includes\//gi.test(combined)) cmsList.push('WordPress');
  if (/webflow\.js|webflow\.io/gi.test(combined)) cmsList.push('Webflow');
  if (/squarespace\.com|squarespace-cdn\.com/gi.test(combined)) cmsList.push('Squarespace');
  if (/wix\.com|wixstatic\.com/gi.test(combined)) cmsList.push('Wix');
  if (/drupal-settings-json|drupalSettings/gi.test(html)) cmsList.push('Drupal');
  return cmsList;
}

function checkEcommercePlatforms(combined, html) {
  if (/cdn\.shopify\.com|myshopify\.com/gi.test(combined)) return 'Shopify';
  if (/woocommerce/gi.test(combined)) return 'WooCommerce';
  if (/magento/gi.test(combined)) return 'Magento';
  if (/bigcommerce\.com/gi.test(combined)) return 'BigCommerce';
  return null;
}

function checkCDNProviders(combined, headers) {
  const providers = [];
  const searchContent = `${combined} ${JSON.stringify(headers)}`;

  if (/cloudflare\.com|cf-ray/gi.test(searchContent)) providers.push('Cloudflare');
  if (/cloudfront\.net/gi.test(searchContent)) providers.push('Amazon CloudFront');
  if (/fastly\.net/gi.test(searchContent)) providers.push('Fastly');
  if (/akamai\.net/gi.test(searchContent)) providers.push('Akamai');

  return providers;
}

function detectHostingFromHeaders(headers, domain) {
  const serverHeader = (headers['server'] || '').toLowerCase();
  const cfRay = headers['cf-ray'];
  const xVercelId = headers['x-vercel-id'];
  const xNetlify = headers['x-nf-request-id'];

  if (cfRay) return 'Cloudflare';
  if (xVercelId) return 'Vercel';
  if (xNetlify) return 'Netlify';
  if (headers['x-github-request']) return 'GitHub Pages';
  if (serverHeader.includes('nginx')) return 'Nginx';
  if (serverHeader.includes('apache')) return 'Apache';

  return 'Unknown';
}

function extractJSONLDSchema(html) {
  const types = [];
  const pattern = /<script\s+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  let match;

  while ((match = pattern.exec(html)) !== null) {
    try {
      const schema = JSON.parse(match[1].trim());
      if (schema['@type']) {
        const type = Array.isArray(schema['@type']) ? schema['@type'][0] : schema['@type'];
        if (!types.includes(type)) types.push(type);
      }
    } catch (e) {
      // Invalid JSON, skip
    }
  }

  return { found: types.length > 0, types };
}

function extractImportantMetaTags(html) {
  const basic = {};

  const descMatch = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']*)/i);
  if (descMatch) basic.description = descMatch[1];

  const robotsMatch = html.match(/<meta\s+name=["']robots["']\s+content=["']([^"']*)/i);
  if (robotsMatch) basic.robots = robotsMatch[1];

  const canonicalMatch = html.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']*)/i);
  if (canonicalMatch) basic.canonical = canonicalMatch[1];

  return { basic };
}

function calculateSummary(result) {
  const analyticsCount = [
    result.analytics.ga4.found,
    result.analytics.gtm.found,
    result.analytics.microsoftClarity.found,
    result.analytics.searchConsole.found,
    result.analytics.seoPlugin.found,
    result.analytics.bingWebmaster.found
  ].filter(Boolean).length;

  const marketingCount =
    result.marketing.crm.length +
    result.marketing.emailMarketing.length +
    result.marketing.adPlatforms.length +
    result.marketing.conversionTools.length +
    result.marketing.widgets.length;

  const infrastructureCount =
    result.infrastructure.cms.length +
    (result.infrastructure.ecommerce ? 1 : 0) +
    result.infrastructure.cdn.length;

  const seoCount =
    (result.seo.hasSchema ? 1 : 0) +
    (result.seo.metaTags.basic.description ? 1 : 0);

  return {
    totalToolsFound: analyticsCount + marketingCount + infrastructureCount + seoCount,
    categories: {
      analytics: analyticsCount,
      marketing: marketingCount,
      infrastructure: infrastructureCount,
      seo: seoCount
    }
  };
}

async function runBrowserlessDetection(url, apiKey) {
  // Simplified browserless detection - you can expand this
  const functionCode = `
    export default async function ({ page }) {
      await page.goto('${url}', { waitUntil: 'networkidle2', timeout: 30000 });
      await new Promise(resolve => setTimeout(resolve, 3000));

      return await page.evaluate(() => {
        return {
          pixels: {
            ga4: typeof window.gtag !== 'undefined',
            facebook: typeof window.fbq !== 'undefined',
            clarity: typeof window.clarity !== 'undefined',
            linkedin: typeof window._linkedin_data_partner_ids !== 'undefined',
            tiktok: typeof window.ttq !== 'undefined'
          },
          pixelIds: {}
        };
      });
    }
  `;

  const response = await fetch(
    `https://production-sfo.browserless.io/function?token=${apiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/javascript' },
      body: functionCode
    }
  );

  if (!response.ok) {
    throw new Error('Browserless API request failed');
  }

  return await response.json();
}

module.exports = { analyzeWebsite };
