import re
import argparse
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
def check_link(link, timeout):
    try:
        response = requests.get(link, timeout=timeout, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
        if response.status_code not in range(200, 404) and response.status_code != 429 and response.status_code != 999:
            print(f"Broken link: {link}")
    except requests.ConnectionError:
        print(f"Connection Error: {link}")
    except requests.Timeout:
        print(f"Timeout Error: {link}")
def find_links_in_article(html_content, url):
    parsed_url = urlparse(url)
    root_url = parsed_url.scheme + "://" + parsed_url.netloc
    set_links =  set()
    soup = BeautifulSoup(html_content, 'html.parser')
    article = soup.find('article')
    relative_paths = re.findall(r'href=[\'"]?(/[^\'" >]+)', str(article))
    if relative_paths:
        for i in relative_paths:
            set_links.add(root_url+i)
    set_links.update(re.findall(r'href=[\'"]?(https://[^\'" >]+)', str(article)))
    return set_links
def check_links_in_article(url, timeout):
    response = requests.get(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
    links = find_links_in_article(response.text, url)
    for link in links:
        check_link(link, timeout)
