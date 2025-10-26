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

### [Script Detector](./free-tools/script-detector-standalone/)

Backend-only Node.js tool for detecting website technology stacks and marketing tools:

- Detects 100+ technologies: Analytics, CRM, ad pixels, CMS, tracking tools
- Generates professional markdown reports
- Zero dependencies - pure Node.js
- Supports batch analysis of multiple websites
- Extracts pixel IDs, tracking codes, and implementation details
- [Learn more →](./free-tools/README-script-detector.md)

### [YouTube Transcriber](./free-tools/youtube-transcriber-standalone/)

Python command-line tool for transcribing YouTube videos using OpenAI Whisper API:

- Downloads YouTube audio automatically
- Generates transcripts in TXT, JSON, and SRT formats
- Parallel processing for long videos
- Cost estimation before processing (~$0.006 per minute)
- Secure API key management
- [Learn more →](./free-tools/README-youtube-transcriber.md)

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

# For Script Detector (Node.js)
cd free-tools/script-detector-standalone
node example.js
# Analyzes websites and generates markdown reports

# For YouTube Transcriber
cd free-tools/youtube-transcriber-standalone
pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI API key
python transcribe.py https://www.youtube.com/watch?v=VIDEO_ID
```

## 📋 Requirements

### Python Tools
- **Python 3.7+** (for scrapers, screenshot tool, YouTube transcriber)

### Node.js Tools
- **Node.js 18+** (for script detector)

### Scraping Tools (Python)
- requests==2.31.0
- beautifulsoup4==4.12.3
- lxml==5.1.0
- urllib3==2.2.0
- markdownify==3.12.0

### Screenshot Tool (Python)
- playwright==1.55.0 (+ Chromium browser)

### Script Detector (Node.js)
- No dependencies! Pure Node.js

### YouTube Transcriber (Python)
- openai>=1.3.5
- yt-dlp>=2023.11.16
- pydub>=0.25.1
- FFmpeg (system requirement)

## 📚 Documentation

Full documentation for each tool:

### Python Tools
- [Website Scraping Tools](./free-tools/README.md) - Scraper and documentation tools
- [Screenshot Capture](./free-tools/README-screenshots.md) - Visual capture tool
- [YouTube Transcriber](./free-tools/README-youtube-transcriber.md) - Video transcription

### Node.js Tools
- [Script Detector](./free-tools/README-script-detector.md) - Website tech stack analyzer

Each includes:
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
