import time
import requests
import nbformat
import os
import re
import sys
from bs4 import BeautifulSoup

# Optional: GitHub Personal Access Token (PAT) for private repo access
PAT_TOKEN = os.getenv("PAT_TOKEN")
directory = os.getenv("directory", ".")


def fetch_url(url):
    headers = {"Authorization": f"token {PAT_TOKEN}"} if PAT_TOKEN else {}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return "Valid"
        elif response.status_code == 403 and "sciencedirect.com" in url:
            # Bypass 403 for sciencedirect.com
            return "Valid - Additional Check may required"
        elif response.status_code == 403 and "platform.openai.com" in url:
            # Bypass 403 for platform.openai.com
            return "Valid - Additional Check may required"
        elif response.status_code == 403 and "niaid.nih.gov" in url:
            # Bypass 403 for niaid.nih.gov
            return "Valid - Additional Check may required"
        else:
            return f"Failed (Status Code: {response.status_code})"
        time.sleep(1)
    except requests.exceptions.RequestException as e:
        return f"Failed (Exception: {str(e)})"


def extract_markdown_links(md_content):
    # Regex pattern to find Markdown links
    pattern = r'\[([^\]]+)\]\((http[s]?://[^\)]+)\)'
    return re.findall(pattern, md_content)


def extract_html_links(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return [(a.text, a['href']) for a in soup.find_all('a', href=True)]


def check_links_in_markdown(md_content):
    markdown_links = extract_markdown_links(md_content)
    html_links = extract_html_links(md_content)
    return markdown_links + html_links


def check_links_in_notebook(notebook_content):
    nb = nbformat.reads(notebook_content, as_version=4)
    links = []
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            # Check links in markdown format
            markdown_links = extract_markdown_links(cell.source)
            # Check links in HTML format within markdown cells
            html_links = extract_html_links(cell.source)
            links.extend(markdown_links + html_links)
    return links


def check_links_in_file(file_path):
    failed = False
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith(".ipynb"):
            links = check_links_in_notebook(file.read())
        else:
            links = check_links_in_markdown(file.read())

    for text, link in links:
        status = fetch_url(link)
        print(f"{file_path}, {link}, {status}")
        if "Failed" in status:
            failed = True

    return failed


def find_markdown_and_notebooks(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith((".md", ".ipynb")):
                files.append(os.path.join(root, filename))
    return files


if __name__ == "__main__":
    # Directory to search for markdown and notebook files
    directory = os.getenv("directory", ".")

    # Find all markdown and notebook files in the directory
    files_to_check = find_markdown_and_notebooks(directory)

    # Output header
    print("Filename, Link, Status")

    # Track if any links failed
    any_failed = False

    # Check links in each file
    for file_path in files_to_check:
        if check_links_in_file(file_path):
            any_failed = True

    # Exit with code 1 if any link failed
    if any_failed:
        sys.exit(1)
