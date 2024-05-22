# GitHub_Check_Links

A script that will clone a GitHub repo to local computer, and then find all .md files except for RELEASE.md or other similar files that have too many links. Then, the script will use that .md file path and convert it to GitHub url and checks the URL links in `<article>` tags to see if they are valid

## Download

You can download the script using `git`
```bash
git clone https://github.com/KPCOFGS/Check_Links.git
cd Check_Links
```
You can install the dependencies using pip:
```bash
pip install -r requirements.txt
```

## Usage
To use the script, you need to specify the url of the website you want to check using the `--url` parameter. For example:
```bash
python script.py --url URL [--time-out OPTIONAL-INTEGER]
```

## Note
- This script only checks for `https` links and relative paths
- This script may take a while when there are a lot of URLs to check
- `--time-out` sets to 0 means no timeout
- Due to the nature of the internet, the script may produce false positive results

## License
This repository is licensed under the [Unlicense](LICENSE)
