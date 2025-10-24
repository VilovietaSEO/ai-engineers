#!/usr/bin/env python3
"""
Simple URL Screenshot Capture Tool

Captures both full-page and rolling section screenshots from any URL.

Usage:
    python3 tools/capture_url.py https://example.com
    python3 tools/capture_url.py https://example.com --output screenshots/example
    python3 tools/capture_url.py https://example.com --width 1920 --height 1080
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Tuple

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Missing dependency: playwright")
    print("Install with: pip install playwright && playwright install chromium")
    sys.exit(1)


class URLScreenshotCapture:
    """Captures full-page and rolling section screenshots from any URL"""

    def __init__(self, url: str, output_dir: str = None, viewport_width: int = 1920, viewport_height: int = 1080):
        self.url = url
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        # Create output directory
        if output_dir is None:
            # Generate directory name from URL and timestamp
            domain = url.replace('https://', '').replace('http://', '').split('/')[0].replace('.', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = f"screenshots/{domain}_{timestamp}"

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print(f"📸 Screenshot Capture Tool")
        print(f"URL: {url}")
        print(f"Viewport: {viewport_width}x{viewport_height}")
        print(f"Output: {self.output_dir}\n")

    def capture(self) -> dict:
        """Capture all screenshots and return paths"""
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': self.viewport_width, 'height': self.viewport_height})

            try:
                # Navigate to URL
                print(f"Loading {self.url}...")
                page.goto(self.url, wait_until='networkidle', timeout=60000)
                time.sleep(2)  # Wait for any animations

                # Get page dimensions
                page_height = page.evaluate("document.documentElement.scrollHeight")
                print(f"Page height: {page_height}px\n")

                results = {}

                # 1. Capture full page screenshot
                print("📸 Capturing full page screenshot...")
                full_page_path = self.output_dir / "full_page.png"
                page.screenshot(path=str(full_page_path), full_page=True)
                results['full_page'] = str(full_page_path)
                print(f"✅ Saved: {full_page_path}\n")

                # 2. Capture rolling section screenshots
                print("📸 Capturing rolling section screenshots...")
                section_paths = self._capture_sections(page, page_height)
                results['sections'] = section_paths

                print(f"\n✅ Complete! Captured {len(section_paths)} sections")
                print(f"📁 All screenshots saved to: {self.output_dir}")

                return results

            finally:
                browser.close()

    def _capture_sections(self, page, page_height: int) -> list:
        """Capture viewport-sized sections as we scroll down the page"""
        section_paths = []
        current_scroll = 0
        section_num = 1

        while current_scroll < page_height:
            # Scroll to position
            page.evaluate(f"window.scrollTo(0, {current_scroll})")
            time.sleep(0.5)  # Wait for scroll to settle

            # Capture screenshot
            section_path = self.output_dir / f"section_{section_num:03d}.png"
            page.screenshot(path=str(section_path))
            section_paths.append(str(section_path))

            print(f"  Section {section_num}: {current_scroll}px - {min(current_scroll + self.viewport_height, page_height)}px → {section_path.name}")

            # Move to next section
            current_scroll += self.viewport_height
            section_num += 1

        return section_paths


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Capture full-page and rolling section screenshots from any URL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python3 tools/capture_url.py https://example.com

  # Custom output directory
  python3 tools/capture_url.py https://example.com --output my_screenshots

  # Custom viewport size
  python3 tools/capture_url.py https://example.com --width 1440 --height 900

  # Desktop and mobile captures
  python3 tools/capture_url.py https://example.com --width 375 --height 812
        """
    )

    parser.add_argument('url', help='URL to capture (must include http:// or https://)')
    parser.add_argument('--output', '-o', help='Output directory (default: auto-generated)')
    parser.add_argument('--width', '-w', type=int, default=1920, help='Viewport width (default: 1920)')
    parser.add_argument('--height', type=int, default=1080, help='Viewport height (default: 1080)')

    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)

    # Create capturer and run
    capturer = URLScreenshotCapture(
        url=args.url,
        output_dir=args.output,
        viewport_width=args.width,
        viewport_height=args.height
    )

    try:
        results = capturer.capture()
        print(f"\n{'='*60}")
        print(f"SUMMARY")
        print(f"{'='*60}")
        print(f"Full page: {results['full_page']}")
        print(f"Sections: {len(results['sections'])} screenshots")
        print(f"Directory: {capturer.output_dir}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
