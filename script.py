import requests
from bs4 import BeautifulSoup
import check_link
import argparse
import subprocess
import os
import shutil
def find_md_files(repo_url, user, repo, branch):
    base_url = f"https://github.com/{user}/{repo}/tree/{branch}/"
    cmd = f"git clone {repo_url}.git"
    subprocess.run(cmd, shell=True)
    md_files = set()
    for dirpath, dirnames, filenames in os.walk(repo):
        for filename in filenames:
            if filename.endswith('.md') and all(substring not in filename.lower() for substring in ["releas", "updat", "chang"]):
                relative_path = os.path.relpath(os.path.join(dirpath, filename), repo)
                final_url = base_url + relative_path
                md_files.add(final_url)
    return md_files
def extract_text_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the specified tag and extract text within it
        tag = soup.find('span', class_='Text-sc-17v1xeu-0 bOMzPg')
        if tag:
            return tag.get_text()
        else:
            print("Tag not found on the page.")
            return None
    else:
        print(f"Failed to fetch page: {response.status_code}")
        return None
parser = argparse.ArgumentParser(description="Check links in an HTML article")
parser.add_argument("--url", help="URL to check links in", required=True)
parser.add_argument("--time-out", type=int, help="Timeout for each request in seconds", default=5)
parser.add_argument("--max-search", type=int, help="Maximum .md file searches. When reached, force exit", default=0)
args = parser.parse_args()
url = args.url
time_out = args.time_out
max_search = args.max_search
if time_out < 0:
    raise ValueError("time_out cannot be less than 0")
elif time_out == 0:
    time_out = None
if max_search < 0:
    raise ValueError("max_search cannot be less than 0")
parts = url.split('/')
user, repo = parts[3], parts[4]
branch = extract_text_from_github(url)[1:]
base_url = f"https://github.com/{user}/{repo}/tree/{branch}/"
md_files = find_md_files(url, user, repo, branch)
if md_files and max_search == 0:
    for md_file in md_files:
        print(f"Checking: {md_file}")
        check_link.check_links_in_article(md_file, time_out)
elif md_files and max_search != 0:
    current_search = 0
    for md_file in md_files:
        if current_search != max_search:
            print(f"Checking: {md_file}")
            check_link.check_links_in_article(md_file, time_out)
            current_search+=1
        else:
            break
shutil.rmtree(repo)
