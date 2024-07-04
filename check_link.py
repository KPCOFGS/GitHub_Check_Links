import re
import argparse
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import defaultdict

def check_link(link, timeout, value):
    try:
        response = requests.get(link, timeout=timeout, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
        if response.status_code not in range(200, 404) and response.status_code != 429 and response.status_code != 999:
            for i in range(value):
                print(f"Broken link: {link}")
    except requests.ConnectionError:
        for i in range(value):
            print(f"Connection Error: {link}")
    except requests.Timeout:
        for i in range(value):
            print(f"Timeout Error: {link}")
def is_downloadable(url):
    try:
        response = requests.head(url, allow_redirects=True)
        content_disposition = response.headers.get('Content-Disposition', '')

        # Check if Content-Disposition indicates a download attachment
        if content_disposition.lower().startswith('attachment'):
            return True

        return False

    except requests.RequestException:
        return False

def find_links_in_article(html_content, url):
    parsed_url = urlparse(url)
    root_url = parsed_url.scheme + "://" + parsed_url.netloc
    links_dict = defaultdict(int)
    soup = BeautifulSoup(html_content, 'html.parser')
    article = soup.find('article')

    if article:
        relative_paths = re.findall(r'href=[\'"]?(/[^\'" >]+)', str(article))
        if relative_paths:
            for path in relative_paths:
                full_url = root_url + path
                if not is_downloadable(full_url):
                    links_dict[full_url] += 1

        absolute_paths = re.findall(r'href=[\'"]?(https://[^\'" >]+)', str(article))
        for url in absolute_paths:
            if not is_downloadable(url):
                links_dict[url] += 1

    return links_dict
def check_links_in_article(url, timeout):
    response = requests.get(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
    links = find_links_in_article(response.text, url)
    for link in links:
        check_link(link, timeout, links[link])
