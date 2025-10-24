#!/usr/bin/env python3

import argparse
import json
import re
import sys
from collections import deque
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class WebsiteScraper:
    def __init__(self, base_url, max_depth=2, timeout=10):
        self.base_url = base_url
        self.max_depth = max_depth
        self.timeout = timeout
        self.domain = urlparse(base_url).netloc
        self.visited = set()
        self.pages_data = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; WebsiteScraper/1.0)'
        })
    
    def is_same_domain(self, url):
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ''
    
    def normalize_url(self, url, current_url):
        url = urljoin(current_url, url)
        
        parsed = urlparse(url)
        url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        if url.endswith('/'):
            url = url[:-1]
        
        return url
    
    def extract_metadata(self, soup, url):
        title = None
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        meta_description = None
        
        # Try standard meta description (case-insensitive)
        meta_tag = soup.find('meta', attrs={'name': re.compile('^description$', re.I)})
        if meta_tag:
            meta_description = meta_tag.get('content', '').strip()
        
        # Fallback to og:description
        if not meta_description:
            og_tag = soup.find('meta', attrs={'property': 'og:description'})
            if og_tag:
                meta_description = og_tag.get('content', '').strip()
        
        # Fallback to twitter:description
        if not meta_description:
            twitter_tag = soup.find('meta', attrs={'property': 'twitter:description'})
            if not twitter_tag:
                twitter_tag = soup.find('meta', attrs={'name': 'twitter:description'})
            if twitter_tag:
                meta_description = twitter_tag.get('content', '').strip()
        
        # Additional fallback for itemprop description
        if not meta_description:
            itemprop_tag = soup.find('meta', attrs={'itemprop': 'description'})
            if itemprop_tag:
                meta_description = itemprop_tag.get('content', '').strip()
        
        return {
            'url': url,
            'title': title or 'No title found',
            'meta_description': meta_description or 'No description found'
        }
    
    def extract_links(self, soup, current_url):
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            
            normalized_url = self.normalize_url(href, current_url)
            
            if self.is_same_domain(normalized_url):
                links.add(normalized_url)
        
        return links
    
    def crawl(self):
        queue = deque([(self.base_url, 0)])
        self.visited.add(self.base_url)
        
        while queue:
            current_url, depth = queue.popleft()
            
            if depth > self.max_depth:
                continue
            
            print(f"Crawling: {current_url} (depth: {depth})")
            
            try:
                response = self.session.get(current_url, timeout=self.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'lxml')
                
                metadata = self.extract_metadata(soup, current_url)
                self.pages_data.append(metadata)
                
                if depth < self.max_depth:
                    links = self.extract_links(soup, current_url)
                    
                    for link in links:
                        if link not in self.visited:
                            self.visited.add(link)
                            queue.append((link, depth + 1))
            
            except requests.RequestException as e:
                print(f"Error crawling {current_url}: {e}")
                self.pages_data.append({
                    'url': current_url,
                    'title': 'Error: Could not fetch page',
                    'meta_description': str(e)
                })
            except Exception as e:
                print(f"Unexpected error with {current_url}: {e}")
    
    def save_results(self, output_dir):
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        safe_domain = re.sub(r'[^\w\-]', '-', self.domain)
        timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        filename = f"{safe_domain}-{timestamp}.json"
        
        filepath = output_path / filename
        
        result = {
            'domain': self.domain,
            'base_url': self.base_url,
            'scraped_at': datetime.now().isoformat(),
            'total_pages': len(self.pages_data),
            'max_depth': self.max_depth,
            'pages': self.pages_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to: {filepath}")
        print(f"Total pages scraped: {len(self.pages_data)}")
        
        return filepath


def main():
    parser = argparse.ArgumentParser(
        description='Scrape a website and extract URLs with their titles and meta descriptions'
    )
    parser.add_argument(
        'url',
        help='The URL of the website to scrape'
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        default=2,
        help='Maximum depth to crawl (default: 2)'
    )
    parser.add_argument(
        '--output-dir',
        default='/Users/andrewansley/Desktop/skool-example/analysis',
        help='Directory to save the output JSON file'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
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
    
    print(f"Starting scrape of {args.url}")
    print(f"Max depth: {args.max_depth}")
    print(f"Output directory: {args.output_dir}")
    print("-" * 50)
    
    scraper = WebsiteScraper(
        base_url=args.url,
        max_depth=args.max_depth,
        timeout=args.timeout
    )
    
    try:
        scraper.crawl()
        scraper.save_results(args.output_dir)
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
        if scraper.pages_data:
            print("Saving partial results...")
            scraper.save_results(args.output_dir)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()