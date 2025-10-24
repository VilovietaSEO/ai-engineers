# Free Website Scraping Tools

Two powerful Python tools for website scraping and documentation archiving.

## 🔧 Tools Included

### 1. **website_scraper.py** - Basic Website Metadata Scraper
Crawls websites and extracts metadata (titles, descriptions, URLs) into a structured JSON file.

### 2. **documentation_scraper.py** - Advanced Documentation Scraper
Converts entire documentation websites into well-organized Markdown files with proper directory structure.

---

## 📋 Requirements

### Required Libraries

```bash
requests==2.31.0          # HTTP requests
beautifulsoup4==4.12.3    # HTML parsing
lxml==5.1.0               # Fast XML/HTML parser
urllib3==2.2.0            # HTTP client library
markdownify==3.12.0       # HTML to Markdown conversion (documentation_scraper only)
```

### Python Version
- **Python 3.7+** required

---

## 🚀 Installation

### 1. Install Python Dependencies

```bash
# Install all required libraries
pip install requests==2.31.0 beautifulsoup4==4.12.3 lxml==5.1.0 urllib3==2.2.0 markdownify==3.12.0
```

Or create a `requirements.txt` file:

```txt
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
urllib3==2.2.0
markdownify==3.12.0
```

Then install:
```bash
pip install -r requirements.txt
```

### 2. Download the Scripts

```bash
# Clone this repository
git clone https://github.com/VilovietaSEO/ai-engineers.git
cd ai-engineers/free-tools
```

### 3. Make Scripts Executable (Optional)

```bash
chmod +x website_scraper.py
chmod +x documentation_scraper.py
```

---

## 📖 Tool 1: website_scraper.py

### What It Does
Crawls a website following internal links and extracts:
- Page titles
- Meta descriptions
- URLs

Outputs everything to a structured JSON file.

### Basic Usage

```bash
python website_scraper.py https://example.com
```

### Command-Line Options

```bash
python website_scraper.py <url> [options]

Options:
  --max-depth N         Maximum depth to crawl (default: 2)
  --output-dir PATH     Directory to save results (default: ./analysis)
  --timeout N           Request timeout in seconds (default: 10)
```

### Examples

**Basic scrape with default settings:**
```bash
python website_scraper.py https://example.com
```

**Custom depth and output directory:**
```bash
python website_scraper.py https://example.com --max-depth 3 --output-dir ./my-results
```

**With custom timeout:**
```bash
python website_scraper.py https://example.com --max-depth 2 --timeout 30
```

### Output Format

Creates a JSON file named: `{domain}-{timestamp}.json`

**Example output:**
```json
{
  "domain": "example.com",
  "base_url": "https://example.com",
  "scraped_at": "2025-10-24T11:55:32.123456",
  "total_pages": 15,
  "max_depth": 2,
  "pages": [
    {
      "url": "https://example.com",
      "title": "Example Domain",
      "meta_description": "Example site for documentation"
    },
    {
      "url": "https://example.com/about",
      "title": "About Us",
      "meta_description": "Learn more about our company"
    }
  ]
}
```

### Use Cases
- ✅ SEO analysis and site auditing
- ✅ Site mapping and structure analysis
- ✅ Quick metadata extraction
- ✅ Checking meta descriptions across pages

---

## 📚 Tool 2: documentation_scraper.py

### What It Does
Advanced scraper that converts entire documentation websites into clean Markdown files:
- Extracts main content (removes navigation, headers, footers)
- Converts HTML to Markdown
- Creates directory structure matching the website
- Generates an index file with all pages

### Basic Usage

```bash
python documentation_scraper.py https://docs.example.com
```

### Command-Line Options

```bash
python documentation_scraper.py <url> [options]

Options:
  --max-depth N         Maximum depth to crawl (default: 10)
  --output-dir PATH     Directory to save markdown files (default: ./documentation)
  --timeout N           Request timeout in seconds (default: 30)
  --delay N             Delay between requests in seconds (default: 0.5)
```

### Examples

**Basic documentation scrape:**
```bash
python documentation_scraper.py https://docs.example.com
```

**Custom depth and output:**
```bash
python documentation_scraper.py https://docs.example.com --max-depth 5 --output-dir ./my-docs
```

**With custom delays (be polite!):**
```bash
python documentation_scraper.py https://docs.example.com --delay 1.0
```

**High timeout for slow sites:**
```bash
python documentation_scraper.py https://docs.example.com --timeout 60 --delay 2.0
```

### Output Format

Creates a directory structure with Markdown files:

```
documentation/
├── INDEX.md                    # Master index of all pages
├── index.md                    # Homepage
├── getting-started.md          # Top-level pages
├── installation.md
└── guides/
    ├── quick-start.md          # Nested pages maintain structure
    ├── advanced-usage.md
    └── troubleshooting.md
```

**Each Markdown file includes frontmatter:**
```markdown
---
title: Getting Started Guide
url: https://docs.example.com/guides/getting-started
description: Learn how to get started with our platform
scraped_at: 2025-10-24T11:55:32.123456
---

# Getting Started Guide

[Converted markdown content here...]
```

### Use Cases
- ✅ Archive documentation for offline use
- ✅ Convert web docs to searchable Markdown
- ✅ Preserve documentation versions
- ✅ Create local knowledge bases
- ✅ Generate training datasets

---

## 🎯 Which Tool Should I Use?

| Feature | website_scraper.py | documentation_scraper.py |
|---------|-------------------|-------------------------|
| **Purpose** | Extract metadata | Archive full content |
| **Output** | Single JSON file | Multiple Markdown files |
| **Content** | Titles & descriptions only | Full page content |
| **Speed** | Fast | Slower (includes delays) |
| **Depth** | 2 levels (default) | 10 levels (default) |
| **Best For** | SEO, site mapping | Documentation archiving |

**Quick decision:**
- Need metadata only? → Use `website_scraper.py`
- Need full content in Markdown? → Use `documentation_scraper.py`

---

## ⚠️ Important Notes

### Rate Limiting
- `website_scraper.py` has no rate limiting (fast crawling)
- `documentation_scraper.py` includes 0.5s delay by default (be polite!)
- Always respect the website's `robots.txt` (these tools don't check automatically)

### Legal & Ethical Use
- ✅ Ensure you have permission to scrape target websites
- ✅ Check the website's Terms of Service
- ✅ Respect copyright and intellectual property
- ✅ Use reasonable delays to avoid overloading servers

### Error Handling
- Both tools continue if individual pages fail
- Errors are logged to console
- Partial results are saved even if scraping is interrupted (Ctrl+C)

### Performance Tips
- **Start with low depth** (1-2) to test before doing deep crawls
- **Use longer delays** (`--delay 1.0` or higher) for large documentation sites
- **Increase timeout** for slow websites
- **Monitor console output** to see progress

---

## 🔍 Advanced Usage

### Using as Python Libraries

Both tools can be imported and used in your own Python scripts:

**website_scraper.py:**
```python
from website_scraper import WebsiteScraper

scraper = WebsiteScraper(
    base_url='https://example.com',
    max_depth=2,
    timeout=10
)

scraper.crawl()
output_file = scraper.save_results('./results')
print(f"Saved to: {output_file}")
```

**documentation_scraper.py:**
```python
from documentation_scraper import DocumentationScraper

scraper = DocumentationScraper(
    base_url='https://docs.example.com',
    max_depth=10,
    timeout=30,
    delay=0.5
)

pages_count = scraper.crawl('./documentation')
print(f"Scraped {pages_count} pages")
```

---

## 🐛 Troubleshooting

### Common Issues

**Import errors:**
```bash
# Make sure all dependencies are installed
pip install requests beautifulsoup4 lxml urllib3 markdownify
```

**Timeout errors:**
```bash
# Increase timeout for slow websites
python website_scraper.py https://slow-site.com --timeout 60
```

**SSL certificate errors:**
```bash
# The scrapers handle this automatically, but if you see SSL errors,
# it may be a legitimate security concern with the target site
```

**Memory issues on large sites:**
```bash
# Reduce max-depth to crawl fewer pages
python documentation_scraper.py https://huge-docs.com --max-depth 3
```

---

## 📝 Examples

### Example 1: SEO Audit
```bash
# Quick SEO check of a website
python website_scraper.py https://mywebsite.com --max-depth 3 --output-dir ./seo-audit
```

### Example 2: Archive Documentation
```bash
# Save complete documentation for offline use
python documentation_scraper.py https://docs.framework.com --max-depth 10 --output-dir ./framework-docs
```

### Example 3: Competitor Analysis
```bash
# Analyze competitor's site structure
python website_scraper.py https://competitor.com --max-depth 4 --output-dir ./competitor-analysis
```

### Example 4: Create Knowledge Base
```bash
# Convert company knowledge base to Markdown
python documentation_scraper.py https://kb.company.com --delay 1.0 --output-dir ./knowledge-base
```

---

## 🤝 Contributing

Found a bug or want to add a feature? Feel free to open an issue or submit a pull request!

## 📄 License

These tools are provided as-is for educational and professional use. Please use responsibly and ethically.

---

## 🔗 Resources

- **Repository:** https://github.com/VilovietaSEO/ai-engineers
- **Issues:** https://github.com/VilovietaSEO/ai-engineers/issues

---

**Happy scraping!** 🚀
