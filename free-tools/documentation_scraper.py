#!/usr/bin/env python3

import argparse
import json
import re
import sys
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


class DocumentationScraper:
    def __init__(self, base_url, max_depth=10, timeout=30, delay=0.5):
        self.base_url = base_url
        self.max_depth = max_depth
        self.timeout = timeout
        self.delay = delay
        self.domain = urlparse(base_url).netloc
        self.visited = set()
        self.pages_data = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def is_valid_doc_url(self, url):
        parsed = urlparse(url)
        
        # Skip non-documentation URLs
        skip_patterns = [
            '/api/', '/auth/', '/login', '/signup', '/search',
            '.pdf', '.zip', '.tar', '.gz', '#', 'mailto:', 'tel:',
            'javascript:', 'github.com', 'discord.com', 'twitter.com'
        ]
        
        for pattern in skip_patterns:
            if pattern in url.lower():
                return False
        
        # Check if it's the same domain or a subdomain
        if self.domain in parsed.netloc:
            return True
        
        return False
    
    def normalize_url(self, url, current_url):
        url = urljoin(current_url, url)
        
        # Remove fragments
        if '#' in url:
            url = url.split('#')[0]
        
        parsed = urlparse(url)
        url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        # Remove trailing slash
        if url.endswith('/') and url != self.base_url:
            url = url[:-1]
        
        return url
    
    def clean_text(self, text):
        # Remove extra whitespace and newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()
    
    def extract_content_as_markdown(self, soup, url):
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()
        
        # Try to find the main content area
        main_content = None
        
        # Common content selectors for documentation sites
        content_selectors = [
            'main',
            'article',
            '.content',
            '.documentation',
            '.docs-content',
            '.markdown-body',
            '#content',
            '[role="main"]',
            '.doc-content',
            '.page-content'
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        # If no main content found, use body
        if not main_content:
            main_content = soup.find('body')
        
        if not main_content:
            return None
        
        # Convert to markdown with better options
        markdown_content = md(
            str(main_content),
            heading_style="ATX",
            bullets="-",
            code_language="python",
            strip=['nav', 'footer', 'header'],
            escape_misc=False,
            escape_underscores=False
        )
        
        # Clean up the markdown
        markdown_content = self.clean_text(markdown_content)
        
        # Remove excessive blank lines
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        return markdown_content
    
    def extract_metadata(self, soup, url):
        # Extract title
        title = None
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Try to find h1 as fallback
        if not title:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text(strip=True)
        
        # Extract description
        meta_description = None
        meta_tag = soup.find('meta', attrs={'name': re.compile('^description$', re.I)})
        if meta_tag:
            meta_description = meta_tag.get('content', '').strip()
        
        # Fallback to og:description
        if not meta_description:
            og_tag = soup.find('meta', attrs={'property': 'og:description'})
            if og_tag:
                meta_description = og_tag.get('content', '').strip()
        
        return {
            'url': url,
            'title': title or 'Untitled',
            'description': meta_description or '',
            'scraped_at': datetime.now().isoformat()
        }
    
    def extract_links(self, soup, current_url):
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Skip invalid links
            if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            
            normalized_url = self.normalize_url(href, current_url)
            
            if self.is_valid_doc_url(normalized_url):
                links.add(normalized_url)
        
        return links
    
    def save_page_as_markdown(self, metadata, content, output_dir):
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create filename from URL path
        parsed = urlparse(metadata['url'])
        path_parts = [p for p in parsed.path.split('/') if p]
        
        if not path_parts:
            filename = 'index.md'
        else:
            # Create nested directory structure
            if len(path_parts) > 1:
                subdir = output_path / '/'.join(path_parts[:-1])
                subdir.mkdir(parents=True, exist_ok=True)
                filename = subdir / f"{path_parts[-1]}.md"
            else:
                filename = output_path / f"{path_parts[0]}.md"
        
        # Add metadata header
        markdown_with_header = f"""---
title: {metadata['title']}
url: {metadata['url']}
description: {metadata['description']}
scraped_at: {metadata['scraped_at']}
---

# {metadata['title']}

{content}
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_with_header)
        
        return filename
    
    def crawl(self, output_dir):
        queue = deque([(self.base_url, 0)])
        self.visited.add(self.base_url)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create index file
        index_file = output_path / 'INDEX.md'
        index_content = f"# Documentation Index\n\nScraped from: {self.base_url}\nDate: {datetime.now().isoformat()}\n\n## Pages\n\n"
        
        scraped_count = 0
        
        while queue:
            current_url, depth = queue.popleft()
            
            if depth > self.max_depth:
                continue
            
            print(f"Scraping: {current_url} (depth: {depth})")
            
            try:
                response = self.session.get(current_url, timeout=self.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract metadata
                metadata = self.extract_metadata(soup, current_url)
                
                # Extract content as markdown
                content = self.extract_content_as_markdown(soup, current_url)
                
                if content:
                    # Save the page
                    saved_file = self.save_page_as_markdown(metadata, content, output_dir)
                    scraped_count += 1
                    
                    # Add to index
                    relative_path = saved_file.relative_to(output_path)
                    index_content += f"- [{metadata['title']}]({relative_path}) - {metadata['url']}\n"
                    
                    print(f"  ✓ Saved: {saved_file}")
                
                # Extract links and add to queue
                if depth < self.max_depth:
                    links = self.extract_links(soup, current_url)
                    
                    for link in links:
                        if link not in self.visited:
                            self.visited.add(link)
                            queue.append((link, depth + 1))
                
                # Be polite with rate limiting
                time.sleep(self.delay)
            
            except requests.RequestException as e:
                print(f"  ✗ Error: {e}")
            except Exception as e:
                print(f"  ✗ Unexpected error: {e}")
        
        # Save index file
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"\n{'='*50}")
        print(f"Scraping complete!")
        print(f"Total pages scraped: {scraped_count}")
        print(f"Documentation saved to: {output_path}")
        print(f"Index file: {index_file}")
        
        return scraped_count


def main():
    parser = argparse.ArgumentParser(
        description='Scrape documentation websites and convert to markdown'
    )
    parser.add_argument(
        'url',
        help='The URL of the documentation to scrape'
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        default=10,
        help='Maximum depth to crawl (default: 10)'
    )
    parser.add_argument(
        '--output-dir',
        default='/Users/andrewansley/Desktop/skool-example/.claude/documentation',
        help='Directory to save the markdown files'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=0.5,
        help='Delay between requests in seconds (default: 0.5)'
    )
    
    args = parser.parse_args()
    
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    try:
        parsed_url = urlparse(args.url)
        if not parsed_url.netloc:
            print(f"Error: Invalid URL format: {args.url}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: Invalid URL: {e}")
        sys.exit(1)
    
    print(f"Documentation Scraper")
    print(f"{'='*50}")
    print(f"Target URL: {args.url}")
    print(f"Max depth: {args.max_depth}")
    print(f"Output directory: {args.output_dir}")
    print(f"Request delay: {args.delay}s")
    print(f"{'='*50}\n")
    
    scraper = DocumentationScraper(
        base_url=args.url,
        max_depth=args.max_depth,
        timeout=args.timeout,
        delay=args.delay
    )
    
    try:
        scraper.crawl(args.output_dir)
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()