# GitHub_Check_Links

Inspired by [Check_Links](https://github.com/KPCOFGS/Check_Links)

A script that will clone a GitHub repo to local computer, and then find all .md files except for RELEASE.md or other similar files that would have too many links. Then, the script will use that .md file path and convert it to GitHub url and checks the URL links in `<article>` tags to see if they are valid

## Download

You can download the script using `git`
```bash
https://github.com/KPCOFGS/GitHub_Check_Links.git
cd GitHub_Check_Links
```
You can install the dependencies using pip:
```bash
pip install -r requirements.txt
```

## Parameters

`--url URL` Required. GitHub repository url

`--time-out TIME_OUT` Optional. Timeout for each request in seconds (default: 5)

`--max-search MAX_SEARCH` Optional. Maximum .md file searches. When reached, force exit (default: 0)

## Usage
To use the script, you need to specify the url of the GitHub repository you want to check using the `--url` parameter. For example:
```bash
python script.py --url URL
```

## Note
- This script only checks for `https` links and relative paths
- The script may take a while to clone the repository
- Make sure to have sufficient storage space for the repo
- This script may take a while when there are a lot of URLs to check
- `--time-out` sets to 0 means no timeout
- `--max-search` sets to 0 means no maximum
- Due to the nature of the internet, the script may produce false positive results

## License
This repository is licensed under the [Unlicense](LICENSE)
