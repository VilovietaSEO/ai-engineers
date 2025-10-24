# AI Engineers - Free Tools Collection

A curated collection of free, open-source tools for AI engineers, developers, and SEO professionals.

## 🛠️ Available Tools

### [Free Website Scraping Tools](./free-tools/)

Three powerful Python utilities for website scraping, documentation archiving, and visual capture:

#### 1. **website_scraper.py** - Basic Metadata Scraper
- Extracts page titles, meta descriptions, and URLs
- Outputs structured JSON data
- Perfect for SEO audits and site mapping
- [Learn more →](./free-tools/README.md#tool-1-website_scraperpy)

#### 2. **documentation_scraper.py** - Advanced Documentation Scraper
- Converts entire documentation sites to clean Markdown
- Creates organized directory structure matching the website
- Ideal for offline documentation and knowledge bases
- [Learn more →](./free-tools/README.md#tool-2-documentation_scraperpy)

#### 3. **capture-screenshots.py** - URL Screenshot Capture Tool
- Captures full-page and rolling section screenshots from any URL
- Supports custom viewport sizes (desktop, mobile, tablet)
- Perfect for design documentation, SEO audits, and visual archives
- [Learn more →](./free-tools/README-screenshots.md)

## 🚀 Quick Start

```bash
# Clone this repository
git clone https://github.com/VilovietaSEO/ai-engineers.git
cd ai-engineers

# Install dependencies for scrapers
pip install requests==2.31.0 beautifulsoup4==4.12.3 lxml==5.1.0 urllib3==2.2.0 markdownify==3.12.0

# Run the basic scraper
python free-tools/website_scraper.py https://example.com

# Or run the documentation scraper
python free-tools/documentation_scraper.py https://docs.example.com

# For screenshot capture, install Playwright
pip install playwright
playwright install chromium

# Capture screenshots
python3 free-tools/capture-screenshots.py https://example.com
```

## 📋 Requirements

- **Python 3.7+**

### Scraping Tools
- requests==2.31.0
- beautifulsoup4==4.12.3
- lxml==5.1.0
- urllib3==2.2.0
- markdownify==3.12.0

### Screenshot Tool
- playwright==1.55.0 (+ Chromium browser)

## 📚 Documentation

Full documentation for each tool is available in the [free-tools directory](./free-tools/README.md), including:
- Detailed installation instructions
- Complete usage examples
- Command-line options
- Output format specifications
- Troubleshooting guides

## 🤝 Contributing

Found a bug or want to contribute? Feel free to open an issue or submit a pull request!

## 📄 License

These tools are provided as-is for educational and professional use. Please use responsibly and ethically.

---

**Repository maintained by:** [VilovietaSEO](https://github.com/VilovietaSEO)
