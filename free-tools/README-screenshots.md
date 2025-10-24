# URL Screenshot Capture Tool

A powerful Python tool that captures both full-page screenshots and rolling section screenshots from any URL using Playwright.

## 🎯 What It Does

This tool captures websites in two ways:
1. **Full-page screenshot** - The entire webpage in a single image
2. **Rolling section screenshots** - Viewport-sized sections as it scrolls down the page

Perfect for:
- ✅ Documenting website designs
- ✅ Creating visual archives
- ✅ SEO audits and reporting
- ✅ Competitor analysis
- ✅ Portfolio documentation
- ✅ Quality assurance testing

---

## 📋 Requirements

### Required Libraries

```bash
playwright==1.55.0        # Browser automation
```

### Python Version
- **Python 3.7+** required

---

## 🚀 Installation

### 1. Install Playwright

```bash
pip install playwright
```

### 2. Install Chromium Browser

```bash
playwright install chromium
```

That's it! You're ready to capture screenshots.

---

## 📖 Usage

### Basic Usage

Capture any website with default settings (1920x1080 viewport):

```bash
python3 capture-screenshots.py https://example.com
```

### Command-Line Options

```bash
python3 capture-screenshots.py <url> [options]

Required:
  url                    URL to capture (must include http:// or https://)

Options:
  --output, -o PATH      Output directory (default: auto-generated)
  --width, -w WIDTH      Viewport width in pixels (default: 1920)
  --height HEIGHT        Viewport height in pixels (default: 1080)
  -h, --help            Show help message
```

---

## 💡 Examples

### Example 1: Basic Capture
```bash
python3 capture-screenshots.py https://example.com
```
**Output:** `screenshots/example_com_20251024_121519/`
- Creates timestamped directory
- Captures with 1920x1080 viewport

### Example 2: Custom Output Directory
```bash
python3 capture-screenshots.py https://example.com --output my-screenshots
```
**Output:** `my-screenshots/`
- Saves to your specified directory

### Example 3: Desktop HD Viewport
```bash
python3 capture-screenshots.py https://example.com --width 1440 --height 900
```
**Output:** Screenshots with 1440x900 viewport

### Example 4: Mobile Viewport (iPhone 14)
```bash
python3 capture-screenshots.py https://example.com --width 390 --height 844
```
**Output:** Mobile-sized screenshots

### Example 5: Tablet Viewport (iPad)
```bash
python3 capture-screenshots.py https://example.com --width 1024 --height 768
```
**Output:** Tablet-sized screenshots

### Example 6: Ultra-wide Desktop
```bash
python3 capture-screenshots.py https://example.com --width 2560 --height 1440
```
**Output:** 2K resolution screenshots

---

## 📁 Output Structure

The tool creates a directory with the following structure:

```
screenshots/example_com_20251024_121519/
├── full_page.png          # Complete webpage in one image
├── section_001.png        # First viewport section (0px - 1080px)
├── section_002.png        # Second section (1080px - 2160px)
├── section_003.png        # Third section (2160px - 3240px)
└── ...                    # Additional sections as needed
```

### File Naming

- **Auto-generated directory:** `{domain}_{timestamp}/`
  - Example: `plumberseo_net_20251024_121519/`
- **Full page screenshot:** `full_page.png`
- **Section screenshots:** `section_001.png`, `section_002.png`, etc.

---

## 🎨 Common Viewport Sizes

### Desktop Sizes
```bash
# Full HD (1920x1080)
python3 capture-screenshots.py URL --width 1920 --height 1080

# HD (1366x768) - Most common laptop
python3 capture-screenshots.py URL --width 1366 --height 768

# MacBook Pro 13" (1440x900)
python3 capture-screenshots.py URL --width 1440 --height 900

# 2K (2560x1440)
python3 capture-screenshots.py URL --width 2560 --height 1440

# 4K (3840x2160)
python3 capture-screenshots.py URL --width 3840 --height 2160
```

### Mobile Sizes
```bash
# iPhone 14 Pro (390x844)
python3 capture-screenshots.py URL --width 390 --height 844

# iPhone 14 Pro Max (430x932)
python3 capture-screenshots.py URL --width 430 --height 932

# Samsung Galaxy S23 (360x800)
python3 capture-screenshots.py URL --width 360 --height 800

# Pixel 7 (412x915)
python3 capture-screenshots.py URL --width 412 --height 915
```

### Tablet Sizes
```bash
# iPad (1024x768)
python3 capture-screenshots.py URL --width 1024 --height 768

# iPad Pro 12.9" (1366x1024)
python3 capture-screenshots.py URL --width 1366 --height 1024

# Surface Pro (1368x912)
python3 capture-screenshots.py URL --width 1368 --height 912
```

---

## 📊 Real-World Example

### Capturing plumberseo.net

```bash
python3 capture-screenshots.py https://plumberseo.net
```

**Output:**
```
📸 Screenshot Capture Tool
URL: https://plumberseo.net
Viewport: 1920x1080
Output: screenshots/plumberseo_net_20251024_121519

Loading https://plumberseo.net...
Page height: 19733px

📸 Capturing full page screenshot...
✅ Saved: screenshots/plumberseo_net_20251024_121519/full_page.png

📸 Capturing rolling section screenshots...
  Section 1: 0px - 1080px → section_001.png
  Section 2: 1080px - 2160px → section_002.png
  ...
  Section 19: 19440px - 19733px → section_019.png

✅ Complete! Captured 19 sections
📁 All screenshots saved to: screenshots/plumberseo_net_20251024_121519
```

**Results:**
- **Full page:** 5.1 MB PNG (entire 19,733px tall page)
- **19 sections:** Individual viewport screenshots
- **Total time:** ~30 seconds

---

## 🔧 How It Works

1. **Launches Headless Browser**
   - Uses Playwright's Chromium browser
   - Runs in headless mode (no visible window)

2. **Loads the Page**
   - Navigates to the URL
   - Waits for network idle (all resources loaded)
   - Waits 2 seconds for animations to settle

3. **Captures Full Page**
   - Takes a complete screenshot of the entire page
   - Handles pages of any height

4. **Captures Rolling Sections**
   - Scrolls down the page in viewport-sized increments
   - Captures a screenshot at each position
   - Waits 0.5 seconds between sections for smooth scrolling

5. **Saves All Images**
   - Creates organized directory
   - Saves all screenshots as PNG files

---

## ⚡ Performance Tips

### Speed Optimization
- **Use smaller viewports** for faster captures (e.g., 1366x768 instead of 4K)
- **Reduce wait times** if the site loads quickly (edit the script)
- **Skip sections** if you only need the full-page screenshot

### Quality Optimization
- **Use larger viewports** for higher quality (e.g., 2560x1440)
- **Increase wait times** for slow-loading sites (edit the script)
- **Capture at 2x or 3x device pixel ratio** (requires script modification)

### Storage Optimization
- **Full-page screenshots** can be large (5-20 MB for long pages)
- **Section screenshots** are typically 200-1000 KB each
- **PNG format** ensures lossless quality but larger file sizes

---

## 🐛 Troubleshooting

### Common Issues

**Error: `ModuleNotFoundError: No module named 'playwright'`**
```bash
# Solution: Install Playwright
pip install playwright
playwright install chromium
```

**Error: Browser executable not found**
```bash
# Solution: Install Chromium browser
playwright install chromium
```

**Error: Timeout waiting for page**
```bash
# Solution: Increase timeout in the script (line 61)
# Change: page.goto(self.url, wait_until='networkidle', timeout=60000)
# To:     page.goto(self.url, wait_until='networkidle', timeout=120000)
```

**Page appears blank or incomplete**
```bash
# Solution: Increase wait time after page load
# Edit line 62 in the script:
# Change: time.sleep(2)
# To:     time.sleep(5)
```

**SSL Certificate Errors**
```bash
# The tool should handle SSL errors automatically
# If issues persist, the target site may have security issues
```

**Viewport size too large**
```bash
# Some sites may not render properly at very large sizes
# Try reducing to standard sizes (1920x1080 or smaller)
```

---

## 🎯 Use Cases

### 1. SEO Audits
Capture competitor websites to analyze:
- Layout and design patterns
- Content structure
- Visual hierarchy
- Call-to-action placement

### 2. Design Documentation
Archive your own designs:
- Before/after comparisons
- Version history
- Client presentations
- Portfolio pieces

### 3. Quality Assurance
Test responsive designs:
- Capture at multiple viewport sizes
- Document layout issues
- Cross-browser testing results

### 4. Client Reporting
Create visual reports:
- Website analysis
- Competitor research
- Design proposals
- Progress updates

### 5. Legal/Compliance
Document websites for:
- Terms of service snapshots
- Privacy policy archives
- Regulatory compliance
- Evidence collection

---

## 🔒 Privacy & Ethics

### Best Practices
- ✅ Only capture publicly accessible websites
- ✅ Respect website terms of service
- ✅ Don't capture login-protected content without permission
- ✅ Use responsibly for legitimate purposes
- ✅ Don't overload servers with excessive requests

### Rate Limiting
The tool includes built-in delays:
- 2 seconds initial page load wait
- 0.5 seconds between section captures
- These delays are respectful to web servers

---

## 🚀 Advanced Usage

### Using as a Python Library

You can import and use the tool in your own scripts:

```python
from capture_screenshots import URLScreenshotCapture

# Create capturer
capturer = URLScreenshotCapture(
    url='https://example.com',
    output_dir='my-screenshots',
    viewport_width=1920,
    viewport_height=1080
)

# Capture screenshots
results = capturer.capture()

# Access results
print(f"Full page: {results['full_page']}")
print(f"Sections: {len(results['sections'])} screenshots")
```

### Batch Processing Multiple URLs

```python
from capture_screenshots import URLScreenshotCapture

urls = [
    'https://example.com',
    'https://competitor1.com',
    'https://competitor2.com'
]

for url in urls:
    capturer = URLScreenshotCapture(url=url)
    capturer.capture()
```

---

## 📝 Technical Details

### Dependencies
- **Playwright** - Browser automation framework
- **Chromium** - Headless browser (installed via Playwright)

### Browser Settings
- Headless mode enabled
- Network idle wait (ensures all resources loaded)
- JavaScript enabled
- Cookies enabled
- User agent: Chrome on macOS

### Screenshot Format
- **Format:** PNG (lossless)
- **Color depth:** 24-bit RGB
- **Compression:** PNG default compression

---

## 🆚 Comparison with Other Tools

| Feature | This Tool | Browser DevTools | Cloud Services |
|---------|-----------|-----------------|----------------|
| **Full Page** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Rolling Sections** | ✅ Yes | ❌ No | ⚠️ Sometimes |
| **Automation** | ✅ Yes | ❌ Manual | ✅ Yes |
| **Custom Viewports** | ✅ Yes | ✅ Yes | ⚠️ Limited |
| **Free** | ✅ Yes | ✅ Yes | ⚠️ Freemium |
| **No Account** | ✅ Yes | ✅ Yes | ❌ No |
| **Batch Processing** | ✅ Yes | ❌ No | ✅ Yes |
| **Local Storage** | ✅ Yes | ✅ Yes | ❌ Cloud only |

---

## 🤝 Contributing

Found a bug or want to add a feature? Contributions are welcome!

---

## 📄 License

This tool is provided as-is for educational and professional use. Please use responsibly and ethically.

---

**Happy screenshotting!** 📸
